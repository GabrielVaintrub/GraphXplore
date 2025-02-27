# src/dashboard/callbacks.py
# Gestion des interactions et mises à jour dynamiques
# import base64
# import io
# import scipy.io as sio
import dash
from dash.dependencies import Input, Output, State
from .app import app
import os
import webbrowser
from config import __project_github__, __user_guide_fr__
from dash import html

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



# # Variable globale pour stocker les données importées
# imported_data = {}  # Par exemple, un dictionnaire {fileName: data}

# # Callback pour l'item "Importer" 
# @app.callback(
#     Output("upload-status", "children"),
#     Input("upload-data", "contents"),
#     State("upload-data", "filename")
# )
# def process_uploaded_files(list_of_contents, list_of_names):
#     if list_of_contents is not None:
#         messages = []
#         for contents, name in zip(list_of_contents, list_of_names):
#             try:
#                 # Décodage du contenu uploadé
#                 content_type, content_string = contents.split(',')
#                 decoded = base64.b64decode(content_string)
#                 # Utiliser BytesIO pour lire le contenu
#                 mat_data = sio.loadmat(io.BytesIO(decoded), squeeze_me=True)
#                 # Vérifier la présence de la variable attendue
#                 if 'dataMap' in mat_data:
#                     # Stocker le contenu converti dans notre variable globale
#                     imported_data[name] = mat_data['dataMap']
#                     messages.append(f"Le fichier {name} a été importé avec succès.")
#                 else:
#                     messages.append(f"Le fichier {name} ne contient pas de variable 'dataMap'.")
#             except Exception as e:
#                 messages.append(f"Erreur lors du traitement du fichier {name} : {str(e)}")
#         return html.Ul([html.Li(msg) for msg in messages])
#     return ""

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