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
            data_map = mat_data['dataMap']
            if is_container_map(data_map):
                print("dataMap semble être une container map.")
            else:
                # Il se peut que la container map ait été convertie en un dictionnaire ou en un autre type.
                print("dataMap n'a pas les attributs attendus pour une container map.")
        else:
            print("La variable 'dataMap' n'est pas présente dans le fichier.")
        # if 'dataMap' in mat_data:
        #     current_data.append({
        #         'fileName': file_name,
        #         'filePath': path,
        #         'dataMap': mat_data['dataMap']
        #     })
        #     messages.append(f"Fichier importé : {file_name}")
        # else:
        #     messages.append(f"Le fichier {file_name} ne contient pas de variable 'dataMap'.")
    except Exception as e:
        messages.append(f"Erreur lors du chargement de {file_name} : {str(e)}")
    
    return current_data, messages

def is_container_map(obj):
    """
    Vérifie de manière heuristique si l'objet semble être une container map.
    On teste si l'objet a une méthode keys() et s'il contient certaines clés typiques.
    """
    try:
        # Essayer d'appeler keys(), au cas où l'objet se comporterait comme un dictionnaire
        k = obj.keys()
        # On peut vérifier qu'il contient des clés attendues, par exemple 'fileName' et 'frequences'
        expected_keys = ['fileName', 'frequences']
        if all(key in k for key in expected_keys):
            return True
    except Exception:
        pass
    return False
