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
        return ({', '.join(parts)})
    else:
        return ""
    
def get_trace_for_main_vector(data_item, trace_name, selected_vector, parameters):
    """
    Pour le cas où le vecteur d’affichage sélectionné est le vecteur principal.
    On concatène les séries (y-values) de toutes les cellules et on utilise la liste
    mdv['values'] pour l'axe x.
    """
    data_table = data_item.get("dataTable", [])
    if not data_table:
        return None
    cell0 = data_table[0]
    mdv = cell0.get("main_display_vector", {})
    if not (isinstance(mdv, dict) and mdv.get("name", "").strip() == selected_vector):
        return None

    x_values = mdv.get("values", [])
    y_values = []
    for cell in data_table:
        if isinstance(cell, dict):
            values = cell.get("values", {})
            if isinstance(values, dict):
                series = values.get(measure, [])
                y_values.extend(series)
    if len(x_values) == 1 and len(y_values) > 1:
        x_values = [x_values[0]] * len(y_values)
    return go.Scatter(
        x=x_values,
        y=y_values,
        mode="lines+markers",
        name=f"{trace_name}"
    )

def get_trace_for_parameter_group(data_item, trace_name, selected_vector, parameters):
    """
    Pour le cas où le vecteur d’affichage sélectionné est un paramètre.
    Parcourt toutes les cellules du fichier pour ce measure et collecte les points
    où la valeur du paramètre (selected_vector) est présente.
    Les points sont triés par cette valeur et regroupés en une trace.
    """
    points = []
    for cell in data_item.get("dataTable", []):
        if isinstance(cell, dict):
            # Chercher la valeur du paramètre dans la cellule
            params = cell.get("parameters", [])
            param_value = None
            for p in params:
                if isinstance(p, dict) and p.get("name", "").strip() == selected_vector:
                    param_value = p.get("value")
                    break
            if param_value is None:
                continue

            # Récupérer la série associée à la grandeur dans cette cellule
            values = cell.get("values", {})
            if isinstance(values, dict):
                series = values.get(measure, [])
                # Ici, on suppose que la série est une liste. Pour chaque cellule, nous
                # prenons par exemple le premier élément (à adapter selon votre logique)
                if isinstance(series, list) and series:
                    y_val = series[0]
                elif series:
                    y_val = series
                else:
                    continue
                points.append((param_value, y_val))
    if not points:
        return None
    try:
        # Tenter de convertir en float pour trier par ordre numérique
        points = sorted(points, key=lambda p: float(p[0]))
    except Exception:
        points = sorted(points, key=lambda p: p[0])
    x_values, y_values = zip(*points)
    return go.Scatter(
        x=list(x_values),
        y=list(y_values),
        mode="lines+markers",
        name=f"{trace_name}"
    )

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
    # Détermine si le vecteur sélectionné est le vecteur principal
    first_item = imported_data[0]
    if first_item.get("dataTable") and first_item["dataTable"]:
        first_cell = first_item["dataTable"][0]
        mdv = first_cell.get("main_display_vector", {})
        is_main = (isinstance(mdv, dict) and mdv.get("name", "").strip() == selected_vector)
    else:
        is_main = False

    for row in selected_rows:
        trace_name = build_legend_from_row(row, column_defs)
        print(trace_name)
        # if is_main:
        #     trace = get_trace_for_main_vector(imported_data, trace_name, selected_vector, row)
        #     if trace:
        #         traces.append(trace)
        # else:
        #     trace = get_trace_for_parameter_group(imported_data, trace_name, selected_vector, row)
        #     if trace:
        #         traces.append(trace)

    fig = go.Figure(data=traces)
    fig.update_layout(
        xaxis_title=selected_vector,
        yaxis_title="Valeurs",
        title="Graphique des mesures"
    )
    return fig
