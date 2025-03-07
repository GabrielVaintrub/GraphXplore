# src/dashboard/callbacks.py
# Gestion des interactions et mises à jour dynamiques
import base64
import io
import scipy.io as sio
import dash
import json
from dash import exceptions, html
from dash.dependencies import Input, Output, State, ALL, MATCH
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
    Output("dynamic-tabs", "data", allow_duplicate=True),
    Input("add-tab", "n_clicks"),
    State("dynamic-tabs", "data"),
    prevent_initial_call=True
)
def add_tab_click(n_clicks, current_tabs):
    # Si aucun clic n'a été enregistré, ne pas mettre à jour
    if not n_clicks:
        raise exceptions.PreventUpdate

    # Si current_tabs n'est pas encore défini, initialiser comme une liste vide
    if current_tabs is None:
        current_tabs = []

    # Calculer le nombre d'onglets existants (vous pouvez utiliser len(current_tabs))
    tab_count = len(current_tabs)
    new_tab_id = f"tab-{tab_count+1}"
    new_label = f"Onglet {tab_count+1}"

    # Créer le nouvel onglet via votre fonction factory
    new_tab = create_tab(new_tab_id, new_label)
    
    # Ajouter le nouvel onglet à la liste existante
    current_tabs.append(new_tab)
    return current_tabs


############################
#### GESTION DES ONGLETS ###
############################

@app.callback(
    [
        Output("tab-selector", "options"),
        Output("tab-selector", "value"),
        Output("prev-tab", "disabled"),
        Output("next-tab", "disabled"),
        Output("tab-content", "children"),
        Output("tab-index", "data"),
        Output("dynamic-tabs", "data"),
    ],
    [
        Input("dynamic-tabs", "data"),
        Input("tab-selector", "value"),
        Input("prev-tab", "n_clicks"),
        Input("next-tab", "n_clicks"),
        Input({'type': 'update-tab-name-button', 'index': ALL}, "n_clicks"),
    ],
    [   
        State({'type': 'tab-name', 'index': ALL}, "value"),
        State("tab-index", "data"),
    ],
    prevent_initial_call=True
)
def manage_tabs(tabs, tab_selector, prev_clicks, next_clicks, name_update_click, new_tab_name, tab_index):
    
    if not tabs:  # Aucun onglet disponible
        return [], None, True, True, html.Div("Aucun onglet disponible.", style={"color": "red", "font-weight": "bold"}), 0, None

    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "prev-tab" and tab_index > 0:
            tab_index -= 1
        elif button_id == "next-tab" and tab_index < len(tabs) - 1:
            tab_index += 1
        elif get_button_id_from_json(button_id, "type") == "update-tab-name-button":
            tabs[tab_index]["label"] = new_tab_name[0]
        elif tab_selector != f"tab-{tab_index+1}" and len(tabs) > 1:
            test = False
            tab_index = 0
            for tab in tabs :
                if tab["value"] != tab_selector and test == False:
                    tab_index += 1
                else:
                    test = True
    options = [{"label": tab["label"], "value": tab["value"]} for tab in tabs]
    selected_value = tabs[tab_index]["value"]
    selected_content = html.Div(tabs[tab_index]["content"])

    return options, selected_value, tab_index == 0, tab_index == len(tabs) - 1, selected_content, tab_index, tabs

# Permet de retourner l'id d'un bouton
# Si l'entrée n'est pas un json, ça retourne l'entrée
# Si l'entrée est un json, ça retourne la valeur à l'emplacement label
def get_button_id_from_json(input_string, label):
    """
    Permet de retourner l'id d'un bouton

    Arguments:
        input_string (str): Un string qui potentiellement au format JSON
        label (str): Le label qui contient l'id dans le JSON
    
    Retourne:
        str: retourne l'identifiant du bouton dans je json ou input_string si ce dernier n'est pas un json
    """
    try:
        # Essayer de charger la chaîne en tant que JSON
        parsed_data = json.loads(input_string)
        
        # Si la chaîne est valide en JSON et contient la clé 'type', on la retourne
        if isinstance(parsed_data, dict) and label in parsed_data:
            return parsed_data[label]
        else:
            return None
    except json.JSONDecodeError:
        # Si la conversion échoue, cela signifie que c'est du texte classique
        return input_string
    

    