# src/dashboard/layout.py
# Définition de la mise en page et des composants graphiques
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from config import __version__
import dash_table

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
        # dbc.DropdownMenuItem("_Importer", id="data-import-item", n_clicks=0, href="#"),
        dbc.DropdownMenuItem("Mettre à jour", id="data-reload-item", n_clicks=0, href="#"),
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
        fichier_menu, #dbc.NavItem(dbc.NavLink("Fichier", href="#")),
        preferences_menu, #dbc.NavItem(dbc.NavLink("Préférences", href="#")),
        donnees_menu, #dbc.NavItem(dbc.NavLink("Données", href="#")),
        # dbc.NavItem(dbc.NavLink("Infos", href="#")),
        aide_menu, #dbc.NavItem(dbc.NavLink("Aide", href="#")),
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
# Composant Upload pour l'import des fichiers .mat
upload_component = dcc.Upload(
    id='upload-data',
    children=html.Div(['Drag and drop or click to select .mat files']),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=True,
    accept='.mat'
)

# Modal de gestion des données
data_modal_header = dbc.ModalHeader(
    [
        html.Span("Gestion des données", style={'flex': '1'}),
        
        dbc.Button("X", id="data-modal-close", color="link", className="ml-auto", style={'fontSize': '1.5rem'}) 
    ],
    close_button=False,
    style={'display': 'flex', 'alignItems': 'center'}
)
data_modal = dbc.Modal(
    [
        data_modal_header, 
        upload_component,
        dbc.ModalBody([
            html.P("Liste des données importées:"),
            dash_table.DataTable(
                id='imported-data-table',
                columns=[{"name": "Nom du fichier", "id": "fileName"}],
                data=[],  # Ce tableau sera mis à jour via un callback
                row_selectable="multi",
                selected_rows=[]
            ),
            html.Br(),
            dbc.Button("Importer", id="btn-import", color="primary", className="mr-2"),
            dbc.Button("Supprimer", id="btn-delete", color="danger", className="mr-2"),
            # dbc.Button("Recharger", id="btn-reload", color="secondary")
        ]),
        # dbc.ModalFooter(
        #     dbc.Button("Fermer", id="close-data-modal", className="ml-auto")
        # ),
    ],
    id="data-modal",
    size="lg",
    is_open=False
)

# Exemple de graphique avec Plotly Express
df = px.data.iris()
fig = px.scatter(
    df, 
    x="sepal_width", 
    y="sepal_length", 
    color="species", 
    title="Graphique de dispersion de l'Iris"
)

############################
###### LAYOUT COMPLET ######
############################
# Définir le layout de l'application
layout = html.Div([
    menu,
    html.Div([
        html.H1("Contenu de l'app"),
        html.P("Exemple simple d'une application Dash avec Bootstrap dans une fenêtre native via PyWebView."),
        dcc.Graph(id="graph-iris", figure=fig),
        # # Zone de sortie pour l'importation des données
        # html.Div(id="data-import-output", children="Sélectionnez des fichiers .mat pour importer les données."),
        # # Composant d'upload
        # upload_component,
        # # Zone d'affichage des messages d'état de l'upload
        # html.Div(id="upload-status"),

        # Zone de sortie pour l'item _Ouvrir
        # html.Div(id="file-open-output", children="Cliquez sur _Ouvrir pour démarrer l'ouverture.")

    ], style={'padding': '20px'}),
    html.Footer([
        html.P(f"Version {__version__}", style={'textAlign': 'right', 'fontSize': 'small'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '10px'}),

    # Composants cachés ou d'état
    dcc.Store(id="imported-data-store", data=[]),
    # Intégrer la modal pour la gestion des données
    data_modal,
    # Composant caché pour le callback GitHub
    html.Div(id="dummy-github", style={"display": "none"}),
    # Composant caché pour le callback Documentation
    html.Div(id="dummy-documentation", style={"display": "none"}),

])
