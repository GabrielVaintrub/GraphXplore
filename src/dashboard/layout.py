# src/dashboard/layout.py
# Définition de la mise en page et des composants graphiques
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from config import __version__

# Créer une barre de navigation (Navbar) avec Dash Bootstrap Components
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Fichier", href="#")),
        dbc.NavItem(dbc.NavLink("Préférences", href="#")),
        dbc.NavItem(dbc.NavLink("Données", href="#")),
        dbc.NavItem(dbc.NavLink("Aide", href="#")),
    ],
    brand="GraphXplore",
    brand_href="#",
    color="primary",
    dark=True,
    fluid=True,
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
    navbar,
    html.Div([
        html.H1("Contenu de l'app"),
        html.P("Exemple simple d'une application Dash avec Bootstrap dans une fenêtre native via PyWebView."),
        dcc.Graph(id="graph-iris", figure=fig)
    ], style={'padding': '20px'}),
    html.Footer([
        html.P(f"Version {__version__}", style={'textAlign': 'center', 'fontSize': 'small'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '10px'})
])
