# src/dashboard/upload.py
import os
import dash
from dash import html
from dash.dependencies import Input, Output, State
from .app import app
import tkinter as tk
from tkinter import filedialog
from config import __default_import_Path__
from data.cache import load_data_with_cache
from dashboard.tabs import display_vector_options, display_datas_options

def tk_file_dialog(initialdir="."):
    """Ouvre une boîte de dialogue Tkinter pour sélectionner des fichiers .mat
    et retourne la liste des chemins complets sélectionnés."""
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    file_paths = filedialog.askopenfilenames(
        title="Sélectionnez des fichiers .json",
        initialdir=initialdir,
        filetypes=[("Json data Files", "*.json")]
    )
    root.destroy()
    return list(file_paths)


@app.callback(
    [Output("imported-data-store", "data"),
     Output("imported-data-table", "data"),
     Output("upload-status", "children"),
     Output("last-dir-store", "data")],
    [Input("btn-import", "n_clicks"),
     Input("data-reload-item", "n_clicks")],
    [State("imported-data-store", "data"),
     State("last-dir-store", "data")]
)
def manage_data(n_clicks_upload, n_reload, current_data, last_dir):
    global display_vector_options, display_datas_options
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    # Initialisation des variables si nécessaire
    if current_data is None:
        current_data = []
    if not last_dir:
        last_dir = __default_import_Path__  # Répertoire par défaut

    messages = []
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "btn-import":
        # Ouvre la boîte de dialogue Tkinter pour sélectionner un ou plusieurs fichiers JSON exportés
        file_paths = tk_file_dialog(initialdir=last_dir)
        if file_paths:
            for path in file_paths:
                try:
                    loaded_data = load_data_with_cache(path)
                    file_name = os.path.basename(path)
                    current_data.append({
                        'fileName': file_name,
                        'filePath': path,
                        'dataTable': loaded_data
                    })
                    messages.append(f"Fichier importé : {file_name}")
                except Exception as e:
                    messages.append(f"Erreur lors de l'import de {os.path.basename(path)} : {str(e)}")
            # Mettre à jour le dernier dossier utilisé avec celui du premier fichier sélectionné
            new_last_dir = os.path.dirname(file_paths[0])
        else:
            new_last_dir = last_dir

    elif trigger_id == "data-reload-item":
        updated_data = []
        for item in current_data:
            path = item.get('filePath')
            if path and os.path.exists(path):
                try:
                    loaded_data = load_data_with_cache(path)
                    item['dataTable'] = loaded_data
                    messages.append(f"Fichier rechargé : {item['fileName']}")
                    updated_data.append(item)
                except Exception as e:
                    messages.append(f"Erreur lors du rechargement de {item['fileName']} : {str(e)}")
            else:
                messages.append(f"Fichier introuvable : {item['fileName']}")
        current_data = updated_data
        new_last_dir = last_dir
    else:
        raise dash.exceptions.PreventUpdate
    
    display_vector_options = update_display_vector_options(current_data, display_vector_options)
    # display_datas_options = update_display_datas_options(current_data, display_datas_options)
    # Préparer les données de la table d'affichage (par exemple, pour afficher le nom et le chemin)
    table_data = [{'fileName': item['fileName'], 'chemin': item.get('filePath', '')} for item in current_data]
    
    # Retourner current_data (pour le dcc.Store), la table, un composant Dash pour les messages, et le dernier dossier utilisé
    return current_data, table_data, html.Ul([html.Li(msg) for msg in messages]), new_last_dir

def update_display_vector_options(current_data, current_options=None):
    """
    Parcourt la liste des données importées (current_data) pour extraire
    les vecteurs d'affichage disponibles et construit une liste d'options.
    
    Chaque élément de current_data est supposé être un dictionnaire contenant au
    moins la clé 'dataTable', qui est la structure (dictionnaire) obtenue depuis le fichier JSON.
    
    Dans cette structure, on s'attend à trouver une clé 'datas' (une liste d'objets),
    et pour chaque objet de cette liste, un champ 'main_display_vector' contenant au moins
    le nom du vecteur (par exemple dans le champ 'name') et éventuellement d'autres infos (par exemple 'units').
    
    Si un vecteur d’affichage (identifié ici par son nom) n’est pas déjà présent dans current_options,
    il est ajouté.
    
    Parameters:
        current_data (list): Liste de dictionnaires (un par fichier importé).
        current_options (list, optionnel): Liste d'options déjà présentes, chacune de la forme
            {'label': <texte à afficher>, 'value': <identifiant du vecteur>}. Par défaut, commence avec [].
    
    Returns:
        list: La liste mise à jour des options pour le dropdown.
    """
    if current_options is None:
        current_options = []
    # Pour éviter les doublons, on conserve un ensemble des "values" déjà ajoutées
    existing_values = {opt['value'] for opt in current_options if opt.get('value')}

    # Parcours de chaque fichier importé
    for item in current_data:
        dataTable = item.get('dataTable', {})
        for data in dataTable:
            # Si l'élément possède un champ 'main_display_vector'
            if isinstance(data, dict) and 'main_display_vector' in data:
                mdv = data['main_display_vector']
                # mdv devrait être un dictionnaire (si exporté en JSON)
                if isinstance(mdv, dict):
                    # Extraire le nom et éventuellement les unités
                    name = mdv.get('name', '').strip()
                    units = mdv.get('units', '').strip()
                    # Construire le label (par exemple "Nom (unités)")
                    label = f"{name} ({units})" if units else name
                    # Pour la valeur, on peut utiliser le nom (ou une autre clé unique)
                    value = name
                    if value and value not in existing_values:
                        current_options.append({'label': label, 'value': value})
                        existing_values.add(value)

            if isinstance(data, dict) and 'parameters' in data:
                params = data['parameters']
                # Vérifier que params est bien une liste
                if isinstance(params, list):
                    for param in params:
                        # param devrait être un dictionnaire (si exporté en JSON)
                        if isinstance(param, dict):
                            # Extraire le nom et éventuellement les unités
                            name = param.get('name', '').strip()
                            units = param.get('units', '').strip()
                            # Construire le label (par exemple "Nom (unités)")
                            label = f"{name} ({units})" if units else name
                            # Pour la valeur, on peut utiliser le nom (ou une autre clé unique)
                            value = name
                            if value and value not in existing_values:
                                current_options.append({'label': label, 'value': value})
                                existing_values.add(value)


        # TODO update dropboxs values of existing tabs

    return current_options

def update_display_datas_options(current_data, current_options=None):
    return current_options
