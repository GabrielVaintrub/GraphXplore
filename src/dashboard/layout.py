# src/dashboard/layout.py
# Définition de la mise en page et des composants graphiques
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from config import __version__

############################
########### MENU ###########
############################

####### MENU Fichier #######
fichier_menu = dbc.DropdownMenu(
    label="Fichier",
    children=[
        dbc.DropdownMenuItem("_Ouvrir", id="file-open-item", n_clicks=0, href="#"),
        dbc.DropdownMenuItem("_Sauvegarder", href="#"),
        dbc.DropdownMenuItem("_Exporter", href="#")
    ],
    nav=True,
    in_navbar=True,
)
##### MENU Préférences #####
preferences_menu = dbc.DropdownMenu(
    label="Préférences",
    children=[
        dbc.DropdownMenuItem("_", href="#"),
    ],
    nav=True,
    in_navbar=True,
)
####### MENU Données #######
donnees_menu = dbc.DropdownMenu(
    label="Données",
    children=[
        dbc.DropdownMenuItem("Gérer", id="data-open-modal", n_clicks=0, href="#"),
        dbc.DropdownMenuItem("_Mettre à jour", id="data-reload-item", n_clicks=0, href="#"),
    ],
    nav=True,
    in_navbar=True,
)

######## MENU AIDE #########
aide_menu = dbc.DropdownMenu(
    label="Aide",
    children=[
        dbc.DropdownMenuItem("Documentation", id="documentation-link", n_clicks=0, href="#"),
        dbc.DropdownMenuItem("Github", id="github-link", n_clicks=0, href="#"),
    ],
    nav=True,
    in_navbar=True,
)

menu = dbc.NavbarSimple(
    children=[
        fichier_menu,
        preferences_menu,
        donnees_menu,
        aide_menu,
    ],
    # brand="GraphXplore",
    # brand_href="#",
    color="primary",
    dark=True,
    fluid=True,
    links_left=True  # Aligne les items sur la gauche
)

############################
########## UPLOAD ##########
############################
# Modal de gestion des données
data_modal_header = dbc.ModalHeader(
    [
        html.Span("Gestion des données", style={'flex': '1'}),
        
        dbc.Button("X", id="data-modal-close", color="red", className="ml-auto", style={'fontSize': '1.5rem'}) 
    ],
    close_button=False,
    style={'display': 'flex', 'alignItems': 'center'}
)
files_table = dash_table.DataTable(
    id='imported-data-table',
    columns=[        
        {"name": "Nom du fichier", "id": "fileName"},
        {"name": "Chemin", "id": "chemin"}
    ],
    data=[],  # Ce tableau sera mis à jour via un callback
    style_cell={
        'maxWidth': '200px',         # largeur fixe (à ajuster selon vos besoins)
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'nowrap'
    },
    row_selectable="multi",
    selected_rows=[]
)
data_modal = dbc.Modal(
    [
        data_modal_header, 
        dbc.ModalBody([
            html.P("Liste des données importées:"),
            files_table,
            html.Br(),
            dbc.Button("Importer", id="btn-import", color="primary", className="mr-2"),
            dbc.Button("Supprimer", id="btn-delete", color="danger", className="mr-2"),
            # dbc.Button("Recharger", id="btn-reload", color="secondary")
        ]),
        dbc.ModalFooter(
            html.Div(id="upload-status")
        ),
    ],
    id="data-modal",
    size="lg",
    is_open=False
)

############################
#### BANDEAU DES ONGLETS ###
############################
#tabs_component = dcc.Tabs(
#    id="dynamic-tabs",
#    value="tab-0",
#    children=[],
#    persistence=True  # éventuellement pour conserver l'état des onglets
#)

tabs_component = html.Div([
    html.Div([
        dbc.Button("Précédent", id="prev-tab", n_clicks=0, disabled=True, color="primary", className="mr-2", style={"flex": "0 0 auto"}),
        dcc.Dropdown(id="tab-selector", clearable=False, placeholder="Aucun onglet disponible", style={"flex": "1 1 auto", "width": "100%"}),
        dbc.Button("Suivant", id="next-tab", n_clicks=0, disabled=True, color="primary", className="mr-2", style={"flex": "0 0 auto"})
    ], style={"display": "flex", "alignItems": "center", "width": "100%", "gap": "10px"}),

    html.Div(id="tab-content", style={"padding": "20px"})
])

# Zone contenant uniquement les onglets avec un style scrollable
tabs_scrollable = html.Div(
    tabs_component,
    style={
        "overflowX": "auto",
        "whiteSpace": "nowrap",
        "flexGrow": 1
    }
)


tabs_bandeau = html.Div([
    dbc.Button("+", id="add-tab", n_clicks=0, color="primary", style={"margin-right": "10px"}),
    tabs_scrollable
], style={"display": "flex", "alignItems": "start", "padding": "10px", "backgroundColor": "#eee"})
############################
###### LAYOUT COMPLET ######
############################
# Définir le layout de l'application
layout = html.Div([
    menu,
    tabs_bandeau,
    html.Footer([
        html.P(f"Version {__version__}", style={'textAlign': 'right', 'fontSize': 'small'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '10px'}),

    # Gestion des onglets
    dcc.Store(id="dynamic-tabs", data=[]),  # Stocke des onglets
    dcc.Store(id="tab-index", data=0),  # Stocke l'index de l'onglet actif
    # Composants cachés ou d'état
    dcc.Store(id="imported-data-store", data=[]),
    dcc.Store(id="last-dir-store", data=""),
    # Intégrer la modal pour la gestion des données
    data_modal,
    # Composant caché pour le callback GitHub
    html.Div(id="dummy-github", style={"display": "none"}),
    # Composant caché pour le callback Documentation
    html.Div(id="dummy-documentation", style={"display": "none"}),

])
