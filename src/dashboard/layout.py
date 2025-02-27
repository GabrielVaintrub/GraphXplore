# src/dashboard/layout.py
# Définition de la mise en page et des composants graphiques
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from config import __version__

# Créer une barre de navigation (Navbar) avec Dash Bootstrap Components
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

preferences_menu = dbc.DropdownMenu(
    label="Préférences",
    children=[
        dbc.DropdownMenuItem("_", href="#"),
    ],
    nav=True,
    in_navbar=True,
)

donnees_menu = dbc.DropdownMenu(
    label="Données",
    children=[
        dbc.DropdownMenuItem("_Importer", id="data-import-item", n_clicks=0, href="#"),
        dbc.DropdownMenuItem("_Mettre à jour", href="#"),
    ],
    nav=True,
    in_navbar=True,
)


aide_menu = dbc.DropdownMenu(
    label="Aide",
    children=[
        dbc.DropdownMenuItem("_Documentation", href="#"),
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

# Exemple de graphique avec Plotly Express
df = px.data.iris()
fig = px.scatter(
    df, 
    x="sepal_width", 
    y="sepal_length", 
    color="species", 
    title="Graphique de dispersion de l'Iris"
)

# Définir le layout de l'application
layout = html.Div([
    menu,
    html.Div([
        html.H1("Contenu de l'app"),
        html.P("Exemple simple d'une application Dash avec Bootstrap dans une fenêtre native via PyWebView."),
        dcc.Graph(id="graph-iris", figure=fig),

        # Zone de sortie pour afficher le résultat du callback spécifique à l'item _Importer
        html.Div(id="data-import-output", children="Cliquez sur _Importer pour démarrer l'importation."),
        # Zone de sortie pour l'item _Ouvrir
        html.Div(id="file-open-output", children="Cliquez sur _Ouvrir pour démarrer l'ouverture.")

    ], style={'padding': '20px'}),
    html.Footer([
        html.P(f"Version {__version__}", style={'textAlign': 'center', 'fontSize': 'small'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '10px'}),

    # Composant caché pour le callback GitHub
    html.Div(id="dummy", style={"display": "none"})

])
