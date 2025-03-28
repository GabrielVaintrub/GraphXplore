import dash
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, MATCH
from .app import app

def build_legend_from_row(row, column_defs):
    """
    Construit la légende pour une trace à partir d'une ligne de données.
    """
    parts = []
    for key, value in row.items():
        if value not in (None, ""):
            for col in column_defs:
                if col.get('field') == key:
                    if col.get('hide') == False :
                        parts.append(f"{key}: {value}")
    if parts:
        return ', '.join(parts)
    else:
        return ""

def get_trace_for_main_vector(data_item, trace_name, selected_vector, measure):
    """
    Pour le cas où le vecteur d’affichage sélectionné est le vecteur principal.
    On utilise la liste 'values' du main_display_vector comme axe x et on concatène
    les séries de mesure (y-values) de toutes les cellules.
    
    Attention : la variable 'measure' doit être définie ou extraite de 'row'
    """
    # Recherche du main_display_vector correspondant dans l'une des cellules
    mdv = data_item['main_display_vector']

    # Extraction de l'axe x à partir du vecteur principal
    x_values = mdv.get("values", [])
    y_values = values = data_item.get("values", {}).get(measure, [])
    if not x_values or not y_values:
        return None     
    if len(x_values) != len(y_values):
        # TODO Ajouter une logique de correction
        print(f"Incohérence dans la longueur des séries pour la mesure {measure}")
    return go.Scatter(
        x=x_values,
        y=y_values,
        mode="lines+markers",
        name=trace_name
    )

def is_vector_mdv(data, selected_vector):
    dv_is_mdv = False
    # Si l'élément possède un champ 'main_display_vector'
    if isinstance(data, dict) and 'main_display_vector' in data:
        mdv = data['main_display_vector']
        # mdv devrait être un dictionnaire (si exporté en JSON)
        if isinstance(mdv, dict):
            # Extraire le nom et éventuellement les unités
            name = mdv.get('name', '').strip()
            if name == selected_vector:
                dv_is_mdv = True
    return dv_is_mdv

def is_data_selected_by_user(data, row):
    params = data.get('parameters', [])
    # On considère que data est sélectionnée si pour tous les items de row (qui représentent des paramètres),
    # la valeur correspondante dans params est égale.
    for item in row:
        matching_param = next((param for param in params if param.get("name", "").strip() == item), None)
        if matching_param is not None:
            if row.get(item) != matching_param.get("value"):
                return False
    return True

@app.callback(
    Output({'type': 'tab-graph', 'index': MATCH}, 'figure'),
    [Input({'type': 'update-data-to-display-button', 'index': MATCH}, 'n_clicks')],
    [State('imported-data-store', 'data'),
     State({'type': 'display-vector-dropdown', 'index': MATCH}, 'value'),
     State({'type': 'selected-display-data-table', 'index': MATCH}, 'selectedRows'),
     State({'type': 'selected-display-data-table', 'index': MATCH}, 'columnDefs')]
)
def update_graph(n_clicks, imported_data, selected_vector, selected_rows, column_defs):
    if not n_clicks or imported_data is None or not selected_vector or not selected_rows:
        raise PreventUpdate
    traces = []
    param_traces = {}  
    for row in selected_rows:
        trace_name = build_legend_from_row(row, column_defs)
        for item in imported_data:
            dataTable = item.get('dataTable', {})
            for data in dataTable:
                trace = None
                if row['data'] in data['values']:
                    if is_data_selected_by_user(data, row):
                        if is_vector_mdv(data, selected_vector):
                            trace = get_trace_for_main_vector(data, trace_name, selected_vector, row['data'])
                            # Ajouter la trace si elle est valide
                            if trace:
                                traces.append(trace)
                        else:
                            # Cas où le vecteur sélectionné est un paramètre          
                            # On cherche le paramètre dans data['parameters'] dont le nom correspond à selected_vector
                            params = data.get('parameters', [])
                            matching_param = next((param for param in params if param.get("name", "").strip() == selected_vector), None)
                            if matching_param is not None:
                                # Récupérer la valeur du paramètre pour cet item (sera notre coordonnée x)
                                param_val = matching_param.get("value")
                                # Récupérer la grandeur (mesure) à tracer qui est dans row["data"]
                                measure = row.get("data")
                                # Vérifier que la grandeur existe dans data['values']
                                values_dict = data.get("values", {})
                                if measure in values_dict:
                                    y_val = values_dict[measure]
                                    mdv = data.get("main_display_vector", {}) 
                                    mdv_name = mdv.get("name", "").strip() # par exemple "Fréquence" 
                                    if mdv_name: # Récupérer la valeur du vecteur principal dans row 
                                        mdv_value = row.get(mdv_name) 
                                        mdv_values = mdv.get("values", []) 
                                        idx = None 
                                        if mdv_value is not None and mdv_values: 
                                            try: # On utilise une tolérance pour la comparaison de nombres flottants 
                                                idx = next(i for i, val in enumerate(mdv_values) if val == mdv_value) 
                                            except StopIteration: 
                                                idx = None 
                                        if idx is not None: # Récupérer la série de données correspondant à la grandeur (ex. "absS11") 
                                            y_series = data.get("values", {}).get(measure, []) 
                                            if isinstance(y_series, list) and idx < len(y_series): 
                                                y_val = y_series[idx] 
                                            else: 
                                                y_val = None
                                            if y_val is not None:
                                                # Accumuler ce point dans le dictionnaire param_traces
                                                if trace_name not in param_traces:
                                                    param_traces[trace_name] = {"x": [], "y": []}
                                                param_traces[trace_name]["x"].append(param_val)
                                                param_traces[trace_name]["y"].append(y_val)

    # Créer une trace Plotly pour chaque ensemble de points accumulés pour le cas paramétrique
    print(param_traces.items())
    for tname, points in param_traces.items():
        # Trier les points par la valeur de x (si ces valeurs sont numériques)
        try:
            combined = sorted(zip(points["x"], points["y"]), key=lambda pair: float(pair[0]))
        except Exception:
            combined = sorted(zip(points["x"], points["y"]), key=lambda pair: pair[0])
        if combined:
            xs, ys = zip(*combined)
            trace = go.Scatter(
                x=list(xs),
                y=list(ys),
                mode="lines+markers",
                name=tname
            )
            traces.append(trace)


    fig = go.Figure(data=traces)
    fig.update_layout(
        xaxis_title=selected_vector,
        yaxis_title="Valeurs",
        title="Graphique des mesures"
    )
    return fig
