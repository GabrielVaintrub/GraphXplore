# src/dashboard/tabs.py
from dash import dcc, html
import dash_bootstrap_components as dbc
from numpy import *

display_vector_dropdown_options =[{'label': "-", 'value': ''}]

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
                html.Div([
                    dbc.Label("Grandeurs en axe X"),
                    dcc.Dropdown(
                        id={'type': 'display-dropdown', 'index': tab_id},
                        options=display_vector_dropdown_options,
                        value=display_vector_dropdown_options[0]['value'] if display_vector_dropdown_options else None
                    )
                ], className="mb-3"),
            ]),
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
            dbc.Row([
                dbc.Col([
                    dbc.Label("Nom : "),
                ], width="auto"),
                dbc.Col([
                    dbc.Input(
                        id={'type': 'tab-name', 'index': tab_id},
                        type="text",
                        value=label,
                        style={'marginBottom': '10px', 'with': '30%'},
                    ),
                ], width="auto"),
                dbc.Col([
                    dbc.Button(
                        "✓", 
                        id={'type': 'update-tab-name-button', 'index': tab_id},
                        color="success", 
                        n_clicks=0,
                        style={'marginBottom': '10px'}
                    ),
                ], width="auto"),
            ], align="center"),
        ]),
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
        
        dcc.Graph(
            id={'type': 'tab-graph', 'index': tab_id},
            ),
    ], style={'padding': '20px'})

    return {
        "label":label,
        "value":tab_id,
        "content":tab_content
    }

    #return dcc.Tab(
    #    label=label,
    #    value=tab_id,
    #    children=tab_content
    #)

def generate_display_vector_dropdown_options(datas):
    """
    Génère la liste d'options pour le dropdown d'affichage en parcourant la structure
    de 'datas' issue du fichier MATLAB.
    
    Pour chaque élément de datas, on cherche à extraire la valeur associée
    au vecteur principal d'affichage (par exemple, 'main_display_vector').
    
    Si le champ n'est pas trouvé, on l'ignore.
    
    Retourne:
        Une liste d'options sous forme de dictionnaires {'label': ..., 'value': ...}.
        Si aucune option n'est trouvée, retourne une option par défaut.
    """
    options = []
    display_fisrt_fait = False
    if len(datas) != 0:
        for data in datas:
            # data_dict = convert_tuple_to_dict(data)
            # if data_dict is None:
            #     print("data_dict is None")
            # Vecteur d'affichage principal
            if 'main_display_vector' in data.dtype.names:
                main_display_vector = data
                
                # main_display_vector_fields = main_display_vector.dtype.names
                # main_display_vector_fields = data[2].dtype.names
                 
                if not display_fisrt_fait:
                    print(main_display_vector)
                    # print(data.dtype)
                    # print(data.dtype.names)
                    # print(main_display_vector_fields)
                    # for i in range(0,len(data.dtype.names)):
                    #     print(f"index : {i}, donnée {data[data.dtype.names[i].dtype]}")
                    # print(f"serializable_data : {serializable_data}")

                    display_fisrt_fait = not display_fisrt_fait

    return options
