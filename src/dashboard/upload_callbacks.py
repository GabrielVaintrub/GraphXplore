# src/dashboard/upload.py
import tkinter as tk
from tkinter import filedialog

# import base64
# import io
# import scipy.io as sio
import os
import dash
from dash import html
from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
from .app import app
# from data.importer import import_mat_file
from config import __default_import_Path__
from data.cache import load_data_with_cache

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

    # Préparer les données de la table d'affichage (par exemple, pour afficher le nom et le chemin)
    table_data = [{'fileName': item['fileName'], 'chemin': item.get('filePath', '')} for item in current_data]
    
    # Retourner current_data (pour le dcc.Store), la table, un composant Dash pour les messages, et le dernier dossier utilisé
    return current_data, table_data, html.Ul([html.Li(msg) for msg in messages]), new_last_dir