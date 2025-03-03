# src/data/importer.py
import os
import scipy.io as sio

def import_mat_file(path, current_data, messages):
    """
    Charge un fichier .mat et vérifie qu'il contient une variable 'dataMap'.
    
    Arguments:
        path (str): Le chemin complet vers le fichier .mat.
        current_data (list): La liste des données importées existantes.
        messages (list): La liste des messages à afficher.
    
    Retourne:
        tuple: (current_data, messages) mis à jour.
    """
    file_name = os.path.basename(path)
    try:
        mat_data = sio.loadmat(path, squeeze_me=True)
        if 'dataMap' in mat_data:
            current_data.append({
                'fileName': file_name,
                'filePath': path,
                'dataMap': mat_data['dataMap']
            })
            messages.append(f"Fichier importé : {file_name}")
        else:
            messages.append(f"Le fichier {file_name} ne contient pas de variable 'dataMap'.")
    except Exception as e:
        messages.append(f"Erreur lors du chargement de {file_name} : {str(e)}")
    
    return current_data, messages
