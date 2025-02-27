import dash
from dash import html, dcc
import plotly.express as px
import threading
import webview
import os
from config import __version__

# Créer l'application Dash
app = dash.Dash(__name__)

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
app.layout = html.Div([
    html.H1("Mon Application Dash"),
    html.P("Exemple simple d'une application Dash dans une fenêtre native via PyWebView."),
    dcc.Graph(id="graph-iris", figure=fig),
    html.Footer([
        html.P(f"Version {__version__}", style={'textAlign': 'center', 'fontSize': 'small'})
    ])
])


# Fonction pour lancer l'application Dash
def run_dash():
    app.run_server(debug=True, use_reloader=False)          # TODO attention au passage au mode debug=False :WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

def on_closing():
    print("La fenêtre a été fermée. Exécution des routines de nettoyage.")
    os._exit(0)  # Termine immédiatement le processus TODO, génère [0227/114209.296:ERROR:window_impl.cc(122)] Failed to unregister class Chrome_WidgetWin_0. Error = 1412 dans l'invite de commande
    # Ajouter du code pour :
    # - Libérer des threads (si vous ne les avez pas configurés comme daemon)
    # - Fermer proprement d'autres ressources ou connexions
    # - Effectuer d'autres opérations de nettoyage

if __name__ == '__main__':
    # Démarrer Dash dans un thread séparé
    dash_thread = threading.Thread(target=run_dash, daemon=True)
    dash_thread.start()

    # Créer une fenêtre native qui charge l'application Dash
    main_window = webview.create_window("GraphXplore", "http://127.0.0.1:8050")
    main_window.events.closing += on_closing
    webview.start()
