# src/dashboard/tabs_callbacks.py
# Gestion des interactions et mises à jour dynamiques avec un onglet
from .app import app
import dash, json, os
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from dash import html

@app.callback(
    # Output("output-config", "children"),
    Input({'type': 'manage-tab-button', 'index': ALL}, 'n_clicks'),
)
def manage_tabs(n_clicks_list):
    
    ctx = dash.callback_context
    if not ctx.triggered:
        print("Aucun clic détecté")
        raise dash.exceptions.PreventUpdate

    # ctx.triggered est une liste; on récupère le premier élément déclencheur
    triggered_prop = ctx.triggered[0]["prop_id"]  # par exemple : '{"type":"manage-tab-button","index":"tab-1"}.n_clicks'
    # Extraire la partie avant le point (qui correspond à l'id du composant)
    component_id_str = triggered_prop.split('.')[0]
    # Convertir la chaîne JSON en dictionnaire
    triggered_id = json.loads(component_id_str)
    tab_index = triggered_id.get("index", "inconnu")

    message = f"Clique détecté sur l'onglet {tab_index}"
    print(message)
    
    # return message

@app.callback(
    Output({'type': 'manage-tab-modal', 'index': MATCH}, "is_open"),
    [Input({'type': 'manage-tab-button', 'index': MATCH}, "n_clicks"),
     Input({'type': 'manage-tab-modal-close', 'index': MATCH}, "n_clicks")
     ],
    [State({'type': 'manage-tab-modal', 'index': MATCH}, "is_open")]
)
def toggle_manage_tabs_modal(n_open, n_close, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open
    return not is_open

def build_rows_for_main_display_vector(data, file_name, selected_value):
    """
    Construit les lignes du tableau pour le cas où le vecteur d'affichage principal 
    (main_display_vector) correspond à la sélection.
    Pour chaque grandeur dans "values", une ligne est créée, et pour chaque paramètre 
    présent dans "parameters" (sauf celui correspondant à la sélection), on ajoute une colonne.
    """
    rows = []
    mdv = data.get('main_display_vector')
    if isinstance(mdv, dict) and mdv.get('name', '').strip() == selected_value:
        values = data.get('values', {})
        if isinstance(values, dict):
            for measure in values.keys():
                row = {"data": measure, "file": file_name}
                # Ajout de colonnes pour chaque paramètre présent dans 'parameters' (sauf celui sélectionné)
                params = data.get('parameters')
                if isinstance(params, list):
                    for param in params:
                        if isinstance(param, dict):
                            param_name = param.get('name', '').strip()
                            if param_name and param_name != selected_value:
                                row[param_name] = param.get('value', '')
                rows.append(row)
    return rows


def build_rows_for_parameters(data, file_name, selected_value):
    rows = []
    params = data.get('parameters')
    if isinstance(params, list):
        for param in params:
            if isinstance(param, dict) and param.get('name', '').strip() == selected_value:
                # On a trouvé le paramètre sélectionné
                values = data.get('values', {})
                if isinstance(values, dict):
                    for measure in values.keys():
                        row = {"data": measure, "file": file_name}
                        
                        # Récupérer le vecteur principal (main_display_vector)
                        mdv = data.get('main_display_vector')
                        if isinstance(mdv, dict):
                            mdv_name = mdv.get('name', '').strip()
                            if mdv_name and mdv_name != selected_value:
                                # --> Convertir la liste en chaîne
                                freq_values = mdv.get('values', [])
                                if isinstance(freq_values, list):
                                    # On fabrique une chaîne "val1, val2, val3, ..."
                                    freq_string = ", ".join(str(v) for v in freq_values)
                                    row[mdv_name] = freq_string
                                else:
                                    # Au cas où ce n'est pas une liste, on le convertit quand même en str
                                    row[mdv_name] = str(freq_values)
                        
                        # Ajouter les autres paramètres (sauf le sélectionné)
                        for p in params:
                            if isinstance(p, dict):
                                p_name = p.get('name', '').strip()
                                if p_name and p_name != selected_value:
                                    row[p_name] = p.get('value', '')
                        rows.append(row)
    return rows


def build_table_data(imported_data, selected_value):
    """
    Parcourt l'ensemble des données importées et, pour chaque cellule (objet) de 
    "dataTable", rassemble les lignes issues du vecteur d'affichage principal et 
    des paramètres en fonction de la sélection.
    """
    table_data = []
    for item in imported_data:
        file_name = item.get('fileName', '')
        data_table = item.get('dataTable', [])
        for data in data_table:
            if isinstance(data, dict):
                rows_main = build_rows_for_main_display_vector(data, file_name, selected_value)
                rows_params = build_rows_for_parameters(data, file_name, selected_value)
                table_data.extend(rows_main)
                table_data.extend(rows_params)
    return table_data

def build_columns(table_data):
    """
    Construit dynamiquement la liste des colonnes à afficher dans la DataTable 
    à partir des clés présentes dans les lignes.
    """
    if table_data:
        all_keys = set()
        for row in table_data:
            all_keys.update(row.keys())
        # On trie pour garantir un ordre constant (vous pouvez personnaliser l'ordre ici)
        columns = [{"name": key, "id": key} for key in sorted(all_keys)]
        return columns
    else:
        return [{"name": "data", "id": "data"}, {"name": "file", "id": "file"}]

@app.callback(
    [Output({'type': 'selected-display-data-table', 'index': MATCH}, 'data'),
     Output({'type': 'selected-display-data-table', 'index': MATCH}, 'columns')],
    Input({'type': 'display-vector-dropdown', 'index': MATCH}, 'value'),
    State('imported-data-store', 'data')
)
def update_display_datas_options(selected_value, imported_data):
    # from dash.exceptions import PreventUpdate
    if imported_data is None or not selected_value:
        raise PreventUpdate

    table_data = build_table_data(imported_data, selected_value)
    columns = build_columns(table_data)
    return table_data, columns