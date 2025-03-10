# src/dashboard/tabs_callbacks.py
# Gestion des interactions et mises à jour dynamiques avec un onglet
from .app import app
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash import html
import json

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

@app.callback(
    Output({'type': 'selected-display-data-table', 'index': MATCH}, 'data'),
    Input({'type': 'display-vector-dropdown', 'index': MATCH}, 'value')
)
def update_display_datas_options(selected_value):
    return ''

