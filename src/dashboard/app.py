# src/dashboard/app.py
# Initialisation et configuration de l'application web (Dash/Streamlit)
import dash
import dash_bootstrap_components as dbc

# Créer l'application Dash en utilisant un thème Bootstrap pour le responsive design
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
