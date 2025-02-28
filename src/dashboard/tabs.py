# src/dashboard/tabs.py
from dash import dcc, html
import dash_bootstrap_components as dbc

# src/dashboard/tabs.py
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_tab(tab_id, label):
    """
    Crée un onglet (dcc.Tab) avec un contenu standard.
    
    Arguments:
        tab_id (str): L'identifiant unique de l'onglet (sera utilisé pour les callbacks).
        label (str): Le texte qui apparaît dans l'en-tête de l'onglet.
    
    Retourne:
        dcc.Tab: Un onglet contenant les contrôles standard.
    """
    tab_content = html.Div([
        dbc.Button(
            "Supprimer cet onglet", 
            id={'type': 'delete-tab-button', 'index': tab_id},
            color="danger", 
            n_clicks=0,
            style={'marginBottom': '10px'}
        ),
        html.Div([
            dbc.Label("Grandeurs à afficher"),
            dcc.Dropdown(
                id={'type': 'display-dropdown', 'index': tab_id},
                options=[
                    {'label': 'Grandeur 1', 'value': 'g1'},
                    {'label': 'Grandeur 2', 'value': 'g2'},
                ],
                value='g1'
            )
        ], className="mb-3"),
        html.Br(),
        dcc.Graph(id={'type': 'tab-graph', 'index': tab_id}),
        html.Br(),
        html.Div([
            dbc.Label("Vecteur d'affichage"),
            dcc.Dropdown(
                id={'type': 'vector-dropdown', 'index': tab_id},
                options=[
                    {'label': 'Vecteur 1', 'value': 'v1'},
                    {'label': 'Vecteur 2', 'value': 'v2'},
                ],
                value='v1'
            )
        ], className="mb-3")
    ], style={'padding': '20px'})

    return dcc.Tab(
        label=label,
        value=tab_id,
        children=tab_content
    )
