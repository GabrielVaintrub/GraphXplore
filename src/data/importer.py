# src/data/importer.py
import os, pprint
import scipy.io as sio
from dashboard.tabs import display_vector_dropdown_options, generate_display_vector_dropdown_options
from utils.temp_dir import __TEMP_DIR__
from utils.data_processing import structured_to_serializable

def import_mat_file(path, current_data, messages):
    """
    Charge un fichier .mat et vérifie qu'il contient une table MATLAB.
    
    Arguments:
        path (str): Le chemin complet vers le fichier .mat.
        current_data (list): La liste des données importées existantes.
        messages (list): La liste des messages à afficher.
    
    Retourne:
        tuple: (current_data, messages) mis à jour.
    """
    global display_vector_dropdown_options
    file_name = os.path.basename(path)
    try:
        mat_data = sio.loadmat(path, squeeze_me=True)
        if 'datas' in mat_data:
            datas = mat_data['datas']
            current_data.append({
                    'fileName': file_name,
                    'filePath': path,
                    'dataTable': datas
            })
            # if len(datas) != 0:
            #     for data in datas:
            # temps_files.append(matfile_to_txt(datas, file_name))
            # TODO convert file content to python struct
            # TODO delete file?
            # display_vector_dropdown_options = generate_display_vector_dropdown_options(datas)

        else:
            messages.append(f"Le fichier {file_name} ne contient pas de variable 'datas'.")
    except Exception as e:
        messages.append(f"Erreur lors du chargement de {file_name} : {str(e)}")
    
    return current_data, messages


# CACHE_FILE = "temp/data_cache.pkl"
# # os.path.join(__TEMP_DIR__, f'temp_import_{fileName}.txt')
# cache_files = []

# def load_data_with_cache(mat_path):
#     # Si le fichier de cache existe, on le charge
#     if os.path.exists(CACHE_FILE):
#         print("Chargement des données depuis le cache.")
#         with open(CACHE_FILE, "rb") as f:
#             data = pickle.load(f)
#     else:
#         # Sinon, on charge le fichier .mat et on le convertit
#         print("Chargement du fichier .mat et création du cache.")
#         # Vous pouvez ajouter ici les options 'squeeze_me=True' et 'struct_as_record=False' selon vos besoins
#         data = sio.loadmat(mat_path, squeeze_me=True, struct_as_record=False)
#         # Convertir les données pour les rendre serializables
#         data_serializable = structured_to_serializable(data)
#         # Créer le dossier du cache s'il n'existe pas
#         os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
#         # Sauvegarder dans le cache
#         with open(CACHE_FILE, "wb") as f:
#             pickle.dump(data_serializable, f)
#         data = data_serializable
#     return data