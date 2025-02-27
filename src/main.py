import dash
from dash import html, dcc
import plotly.express as px
import threading
import webview

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
    dcc.Graph(id="graph-iris", figure=fig)
])

# Fonction pour lancer l'application Dash
def run_dash():
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    # Démarrer Dash dans un thread séparé
    threading.Thread(target=run_dash).start()
    
    # Créer une fenêtre native qui charge l'application Dash
    webview.create_window("GraphXplore", "http://127.0.0.1:8050")
    webview.start()
