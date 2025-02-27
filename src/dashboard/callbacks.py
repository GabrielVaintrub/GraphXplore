# src/dashboard/callbacks.py
# Gestion des interactions et mises à jour dynamiques
from dash.dependencies import Input, Output
from .app import app
from config import __project_github__
import webbrowser

# Callback pour l'item "_Importer" 
@app.callback(
    Output("data-import-output", "children"),
    [Input("data-import-item", "n_clicks")]
)
def handle_data_import_click(n_clicks_data_import):
    if n_clicks_data_import and n_clicks_data_import > 0:
        # Ici, vous pouvez ajouter la logique réelle d'importation de données
        return f"L'item _Importer a été cliqué {n_clicks_data_import} fois."
    return "Cliquez sur _Importer pour démarrer l'importation."

# Callback pour l'item "_Ouvrir"
@app.callback(
    Output("file-open-output", "children"),
    [Input("file-open-item", "n_clicks")]
)
def handle_file_open_click(n_clicks_file_open):
    if n_clicks_file_open and n_clicks_file_open > 0:
        # Ajoutez ici la logique d'ouverture, par exemple l'affichage d'une boîte de dialogue ou le chargement d'un fichier
        return f"L'item _Ouvrir a été cliqué {n_clicks_file_open} fois."
    return "Cliquez sur _Ouvrir pour démarrer l'ouverture."

# Callback pour l'item "_Github"
@app.callback(
    Output("dummy", "children"),
    [Input("github-link", "n_clicks")]
)
def open_github_link(n_clicks_github):
    if n_clicks_github and n_clicks_github > 0:
        # Ouvre l'URL dans le navigateur par défaut
        webbrowser.open(__project_github__)
    return ""