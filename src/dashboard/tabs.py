# src/dashboard/tabs.py
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_manage_tab_modal(tab_id):
    return dbc.Modal(
        [
            dbc.ModalHeader(
                [
                    html.Span(f"Gérer l'onglet {tab_id}", style={'flex': '1'}),
                    
                    dbc.Button("X", id={'type': 'manage-tab-modal-close', 'index': tab_id}, color="red", className="ml-auto", style={'fontSize': '1.5rem'}) 
                ],
                close_button=False,
                style={'display': 'flex', 'alignItems': 'center'}
            ),
            dbc.ModalBody([
                # html.P(f"Gérer l'onglet {tab_id}"),

                html.Div([
                    dbc.Label("Grandeurs en axe X"),
                    dcc.Dropdown(
                        id={'type': 'display-dropdown', 'index': tab_id},
                        options=[
                            {'label': 'Grandeur 1', 'value': 'g1'},
                            {'label': 'Grandeur 2', 'value': 'g2'},
                        ],
                        value='g1'
                    )
                ], className="mb-3"),
                # files_table,
                # html.Br(),
                # dbc.Button("Importer", id="btn-import", color="primary", className="mr-2"),
                # dbc.Button("Supprimer", id="btn-delete", color="danger", className="mr-2"),
                # dbc.Button("Recharger", id="btn-reload", color="secondary")
            ]),
            # dbc.ModalFooter(
            #     html.Div(id="upload-status")
            # ),
        ],
        id={'type': 'manage-tab-modal', 'index': tab_id},          #id={'type': 'tab-graph', 'index': tab_id}
        size="lg",
        is_open=False
    )

def create_tab(tab_id, label):
    """
    Crée un onglet (dcc.Tab) avec un contenu standard.
    
    Arguments:
        tab_id (str): L'identifiant unique de l'onglet (sera utilisé pour les callbacks).
        label (str): Le texte qui apparaît dans l'en-tête de l'onglet.
    
    Retourne:
        dcc.Tab: Un onglet contenant les contrôles standard.
    """
    new_manage_tab_modal = create_manage_tab_modal(tab_id)

    tab_content = html.Div([
        # dbc.Button(
        #     "Supprimer cet onglet", 
        #     id={'type': 'delete-tab-button', 'index': tab_id},
        #     color="danger", 
        #     n_clicks=0,
        #     style={'marginBottom': '10px'}
        # ),
        new_manage_tab_modal,
        html.Div([
            # dbc.Label("Gestion de l'onglet"),
            dbc.Button(
                "Configuration onglet", 
                id={'type': 'manage-tab-button', 'index': tab_id},
                color="primary", 
                n_clicks=0,
                style={'marginBottom': '10px'}
            ),
            dbc.Button(
                "Supprimer cet onglet", 
                id={'type': 'delete-tab-button', 'index': tab_id},
                color="danger", 
                n_clicks=0,
                style={'marginBottom': '10px'}
            ),
        ], className="mb-3"),
        
        # html.Div([
        #     dbc.Label("Grandeurs à afficher"),
        #     dcc.Dropdown(
        #         id={'type': 'display-dropdown', 'index': tab_id},
        #         options=[
        #             {'label': 'Grandeur 1', 'value': 'g1'},
        #             {'label': 'Grandeur 2', 'value': 'g2'},
        #         ],
        #         value='g1'
        #     )
        # ], className="mb-3"),
        # html.Br(),
        dcc.Graph(
            id={'type': 'tab-graph', 'index': tab_id},
            # style={'config.responsive': 'true'}
            ),
        # html.Br(),
        # html.Div([
        #     dbc.Label("Vecteur d'affichage"),
        #     dcc.Dropdown(
        #         id={'type': 'vector-dropdown', 'index': tab_id},
        #         options=[
        #             {'label': 'Vecteur 1', 'value': 'v1'},
        #             {'label': 'Vecteur 2', 'value': 'v2'},
        #         ],
        #         value='v1'
        #     )
        # ], className="mb-3")
    ], style={'padding': '20px'})

    return dcc.Tab(
        label=label,
        value=tab_id,
        children=tab_content
    )
