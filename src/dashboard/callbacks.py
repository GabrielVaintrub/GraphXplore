# src/dashboard/callbacks.py
# Gestion des interactions et mises à jour dynamiques
import base64
import io
import scipy.io as sio
import dash
from dash import exceptions, html
from dash.dependencies import Input, Output, State
from .app import app
import os
import webbrowser
from config import __project_github__, __user_guide_fr__
from dashboard.tabs import create_tab
from dash.exceptions import PreventUpdate
from dashboard.upload import tk_file_dialog

############################
####### MENU Fichier #######
############################

# Callback pour l'item "Ouvrir"
# @app.callback(
#     Output("file-open-output", "children"),
#     [Input("file-open-item", "n_clicks")]
# )
# def handle_file_open_click(n_clicks_file_open):
#     if n_clicks_file_open and n_clicks_file_open > 0:
#         # Ajoutez ici la logique d'ouverture, par exemple l'affichage d'une boîte de dialogue ou le chargement d'un fichier
#         return f"L'item _Ouvrir a été cliqué {n_clicks_file_open} fois."
#     return "Cliquez sur _Ouvrir pour démarrer l'ouverture."


############################
##### MENU Préférences #####
############################


############################
####### MENU Données #######
############################
@app.callback(
    Output("data-modal", "is_open"),
    [Input("data-open-modal", "n_clicks"),
     Input("data-modal-close", "n_clicks")],
    [State("data-modal", "is_open")]
)
def toggle_data_modal(n_open, n_close, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open
    return not is_open

# Callback pour traiter l'upload via Tkinter
# @app.callback(
#     [Output("imported-data-store", "data"),
#      Output("imported-data-table", "data"),
#      Output("upload-status", "children"),
#      Output("last-dir-store", "data")],
#     Input("tk-upload-button", "n_clicks"),
#     State("imported-data-store", "data"),
#     State("last-dir-store", "data")
# )
# def process_tk_upload(n_clicks, current_data, last_dir):
#     if not n_clicks:
#         raise PreventUpdate

#     # Si aucun état n'est défini, initialiser la liste
#     if current_data is None:
#         current_data = []
#     if last_dir is None:
#         last_dir = os.getcwd()  # ou un chemin par défaut

#     file_paths = tk_file_dialog(initialdir=last_dir)  # Ouvre la boîte de dialogue Tkinter et renvoie les chemins

#     messages = []
#     for path in file_paths:
#         file_name = os.path.basename(path)
#         # Essayez de charger le fichier .mat
#         try:
#             mat_data = sio.loadmat(path, squeeze_me=True)
#             if 'dataMap' in mat_data:
#                 current_data.append({
#                     'fileName': file_name,
#                     'chemin': path,
#                     'dataMap': mat_data['dataMap']
#                 })
#                 messages.append(f"Fichier importé : {file_name}")
#             else:
#                 messages.append(f"Le fichier {file_name} ne contient pas de variable 'dataMap'.")
#         except Exception as e:
#             messages.append(f"Erreur lors du chargement de {file_name} : {str(e)}")

#     # Mettre à jour la variable du dernier dossier utilisé
#     # Si l'utilisateur a sélectionné au moins un fichier, le dossier du premier fichier est utilisé
#     new_last_dir = os.path.dirname(file_paths[0]) if file_paths else last_dir

# @app.callback(
#     [Output("imported-data-store", "data"),
#      Output("upload-status", "children"),
#      Output("imported-data-table", "data")],
#     Input("data-reload-item", "n_clicks"),
#     State("imported-data-store", "data")
# )
# def update_files(n_clicks, current_data):
#     if not n_clicks or current_data is None:
#         raise PreventUpdate
#     messages = []
#     for item in current_data:
#         path = item.get('filePath')
#         file_name = item.get('fileName')
#         try:
#             mat_data = sio.loadmat(path, squeeze_me=True)
#             if 'dataMap' in mat_data:
#                 item['dataMap'] = mat_data['dataMap']
#                 messages.append(f"{file_name} rechargé avec succès.")
#             else:
#                 messages.append(f"{file_name} ne contient plus 'dataMap'.")
#         except Exception as e:
#             messages.append(f"Erreur lors du rechargement de {file_name}: {str(e)}")
#     # Mise à jour de la table
#     table_data = [{'fileName': item['fileName'], 'chemin': item['filePath']} for item in current_data]
#     return current_data, html.Ul([html.Li(msg) for msg in messages]), table_data

############################
######## MENU AIDE #########
############################

# Callback pour l'item "Github"
@app.callback(
    Output("dummy-github", "children"),
    [Input("github-link", "n_clicks")]
)
def open_github_link(n_clicks_github):
    if n_clicks_github and n_clicks_github > 0:
        # Ouvre l'URL dans le navigateur par défaut
        webbrowser.open(__project_github__)
    return ""
# Callback pour l'item "Documentation"
@app.callback(
    Output("dummy-documentation", "children"),
    [Input("documentation-link", "n_clicks")]
)
def open_documentation_link(n_clicks_doc):
    if n_clicks_doc and n_clicks_doc > 0:
        # Ouvre le PDF avec le lecteur par défaut sur Windows
        os.startfile(os.path.join("docs", __user_guide_fr__))
    return ""

############################
#### BANDEAU DES ONGLETS ###
############################
@app.callback(
    Output("dynamic-tabs", "children"),
    Input("add-tab", "n_clicks"),
    State("dynamic-tabs", "children")
)
def add_tab_click(n_clicks, current_tabs):
    # Si aucun clic n'a été enregistré, ne pas mettre à jour
    if not n_clicks:
        raise exceptions.PreventUpdate

    # Si current_tabs n'est pas encore défini, initialiser comme une liste vide
    if current_tabs is None:
        current_tabs = []

    # Calculer le nombre d'onglets existants (vous pouvez utiliser len(current_tabs))
    # On part du principe que l'on souhaite que le premier onglet ajouté soit numéroté 1.
    tab_count = len(current_tabs)
    new_tab_id = f"tab-{tab_count+1}"
    new_label = f"Onglet {tab_count+1}"

    # Créer le nouvel onglet via votre fonction factory
    new_tab = create_tab(new_tab_id, new_label)
    
    # Ajouter le nouvel onglet à la liste existante
    current_tabs.append(new_tab)
    
    return current_tabs