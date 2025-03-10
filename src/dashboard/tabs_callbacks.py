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

def build_rows_for_parameters(data, file_name, selected_value, existing_rows):
    """
    Construit les lignes du tableau pour le cas où le paramètre sélectionné (dans 'parameters')
    est présent dans la donnée.
    
    Pour chaque grandeur dans "values" et pour chaque valeur du vecteur principal (main_display_vector),
    on crée une ligne qui inclut :
      - La grandeur (clé 'data'),
      - Le fichier source (clé 'file'),
      - Une colonne pour le vecteur principal (ex. 'Fréquence') contenant la valeur actuelle,
      - Et pour chaque autre paramètre (hors celui sélectionné), sa valeur.
    """
    rows = []
    params = data.get('parameters')
    # On vérifie d'abord que le paramètre sélectionné est présent
    if isinstance(params, list):
        selected_exists = any(
            isinstance(param, dict) and param.get('name', '').strip() == selected_value
            for param in params
        )
        if selected_exists:
            values = data.get('values', {})
            if isinstance(values, dict):
                # Récupérer le vecteur principal (par exemple, "Fréquence")
                mdv = data.get('main_display_vector')
                if isinstance(mdv, dict):
                    mdv_name = mdv.get('name', '').strip()  # par exemple "Fréquence"
                    mdv_values = mdv.get('values', [])
                else:
                    mdv_name = None
                    mdv_values = [None]  # Valeur par défaut si absent

                # Pour chaque grandeur (par exemple "absS11", "angleS11", etc.)
                for measure in values.keys():
                    # Pour chaque valeur du vecteur principal, créer une ligne
                    for freq in mdv_values:
                        row = {"data": measure, "file": file_name}
                        # Ajouter la valeur du vecteur principal dans une colonne
                        if mdv_name and mdv_name != selected_value:
                            row[mdv_name] = freq
                        # Ajouter toutes les autres colonnes de paramètres (hors le paramètre sélectionné)
                        for p in params:
                            if isinstance(p, dict):
                                p_name = p.get('name', '').strip()
                                if p_name and p_name != selected_value:
                                    row[p_name] = p.get('value', '')
                        if row not in existing_rows:
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
                rows_params = build_rows_for_parameters(data, file_name, selected_value, existing_rows=table_data)
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
        columns = [{"field": key, "headerName": key, "filter": True, "sortable": True} for key in sorted(all_keys)]
        return ([{"field": "checkbox", "checkboxSelection": True}] + columns)
    else:
        return [       
            {"field": "checkbox", "checkboxSelection": True},     
            {"field": "data", "headerName": "data", "filter": True},
            {"field": "file", "headerName": "file", "filter": True},
        ]

@app.callback(
    [Output({'type': 'selected-display-data-table', 'index': MATCH}, 'rowData'),
     Output({'type': 'selected-display-data-table', 'index': MATCH}, 'columnDefs')],
    Input({'type': 'display-vector-dropdown', 'index': MATCH}, 'value'),
    State('imported-data-store', 'data')
)
def update_display_datas_options(selected_value, imported_data):
    # from dash.exceptions import PreventUpdate
    if imported_data is None or not selected_value:
        raise PreventUpdate

    table_data = build_table_data(imported_data, selected_value)
    col_defs  = build_columns(table_data)
    # Parcourir chaque colonne (sauf celle de sélection) et vérifier si elle ne contient qu'une seule valeur unique
    for col in col_defs:
        field = col.get("field")
        if field and field != "checkbox":
            col["hide"] = False
            # On crée un ensemble des valeurs pour cette colonne, en utilisant une valeur par défaut si la clé n'existe pas
            unique_values = {row.get(field, None) for row in table_data}
            # Si l'ensemble contient une seule valeur (ou aucune), on masque la colonne
            if len(unique_values) <= 1:
                col["hide"] = True
    return table_data, col_defs 