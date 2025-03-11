# src/dashboard/tabs.py
from dash import dcc, html#, dash_table
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from numpy import *
from config import __nb_rows_data_table__

display_vector_options =[{'label': "-", 'value': ''}]
display_datas_options = []

def creat_data_display_table(tab_id):
    return dag.AgGrid(
        id={'type': 'selected-display-data-table', 'index': tab_id},
        columnDefs = [
            {"field": "checkbox", "checkboxSelection": True},
            {"field": "data", "filter": "agTextColumnFilter"},  # pour le nom de la grandeur
            {"field": "file", "filter": "agTextColumnFilter"},  # pour le nom du fichier
        ],

        rowData=[],  # Ce tableau sera mis à jour via un callback
        columnSize="autoSize",
        defaultColDef={"filter": True, "sortable": True, "resizable": True},
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": __nb_rows_data_table__,
            "rowSelection":"multiple",

        }
    )       

def create_manage_tab_modal(tab_id, label):
    return dbc.Modal(
        [
            dbc.ModalHeader(
                [
                    html.Span(f"Gérer l'onglet {label}", style={'flex': '1'}),
                    
                    dbc.Button("X", id={'type': 'manage-tab-modal-close', 'index': tab_id}, color="red", className="ml-auto", style={'fontSize': '1.5rem'}) 
                ],
                close_button=False,
                style={'display': 'flex', 'alignItems': 'center'}
            ),
            dbc.ModalBody([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Nom de l'onglet : "),
                        ], width="auto"),
                        dbc.Col([
                            dbc.Input(
                                id={'type': 'tab-name', 'index': tab_id},
                                type="text",
                                value="",
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
                    dbc.Label("Grandeurs en axe X"),
                    dcc.Dropdown(
                        id={'type': 'display-vector-dropdown', 'index': tab_id},
                        clearable=False,
                        options=display_vector_options,
                        value=display_vector_options[0]['value'] if display_vector_options else None
                    )                  
                ], className="mb-3"),

                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Données à afficher"),
                        ], width="auto"),
                        dbc.Col([
                            dbc.Button(
                                "✓", 
                                id={'type': 'update-data-to-display-button', 'index': tab_id},
                                color="success", 
                                n_clicks=0,
                                style={'marginBottom': '10px'}
                            ),
                        ], width="auto"),  
                    ], align="center"),    
                    creat_data_display_table(tab_id)
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
    new_manage_tab_modal = create_manage_tab_modal(tab_id, label)

    tab_content = html.Div([
        new_manage_tab_modal,
        html.Div([
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

