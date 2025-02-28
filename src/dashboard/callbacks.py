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

# Callback pour traiter l'upload de fichiers .mat et mettre à jour le dcc.Store
@app.callback(
    [Output("imported-data-table", "data"),
     Output("upload-status", "children"),
     Output("imported-data-store", "data")],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("imported-data-store", "data")
)
def process_uploaded_files(list_of_contents, list_of_names, current_data):
    if current_data is None:
        current_data = []
    messages = []
    if list_of_contents is not None:
        for contents, name in zip(list_of_contents, list_of_names):
            try:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                # Charger le fichier .mat à partir du contenu décodé
                mat_data = sio.loadmat(io.BytesIO(decoded), squeeze_me=True)
                # if 'dataMap' in mat_data:
                    # Ajouter les données sous forme de dictionnaire à la liste existante
                    # (Vous pouvez ajouter ici une conversion personnalisée si nécessaire)
                # current_data.append({'fileName': name, 'dataMap': mat_data['dataMap']})
                current_data.append({'fileName': name})
                messages.append(f"Le fichier {name} a été importé avec succès.")
                # else:
                #     messages.append(f"Le fichier {name} ne contient pas de variable 'dataMap'.")
            except Exception as e:
                messages.append(f"Erreur lors du traitement du fichier {name} : {str(e)}")
    return current_data, html.Ul([html.Li(msg) for msg in messages]), current_data

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