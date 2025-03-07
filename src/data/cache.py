# src/data/cache.py

import os
import pickle
import scipy.io as sio
import time
from utils.data_processing import structured_to_serializable

# Dossier de cache (vous pouvez le configurer)
CACHE_DIR = "temp/cache"

def get_cache_file_path(mat_file_path):
    """
    Génère le chemin du fichier cache à partir du chemin du fichier .mat.
    Par exemple, "data/myfile.mat" deviendra "temp/cache/myfile.pkl"
    """
    base_name = os.path.basename(mat_file_path)
    # Remplacer l'extension .mat par .pkl
    cache_file_name = os.path.splitext(base_name)[0] + ".pkl"
    return os.path.join(CACHE_DIR, cache_file_name)

def is_cache_up_to_date(mat_file_path, cache_file_path):
    """
    Compare les dates de modification pour déterminer si le cache est à jour.
    Retourne True si le cache existe et a été modifié après le fichier .mat.
    """
    if not os.path.exists(cache_file_path):
        return False
    mat_mod_time = os.path.getmtime(mat_file_path)
    cache_mod_time = os.path.getmtime(cache_file_path)
    return cache_mod_time >= mat_mod_time

def load_data_with_cache(mat_file_path):
    """
    Charge les données depuis un fichier .mat en utilisant un cache.
    Si un cache existe et est à jour, il est chargé ; sinon,
    le fichier .mat est chargé, converti, et le cache est mis à jour.
    """
    # Créer le dossier de cache s'il n'existe pas
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file_path = get_cache_file_path(mat_file_path)
    
    if is_cache_up_to_date(mat_file_path, cache_file_path):
        print(f"Chargement du cache : {cache_file_path}")
        with open(cache_file_path, "rb") as f:
            data = pickle.load(f)
    else:
        print(f"Cache obsolète ou inexistant pour {mat_file_path}. Chargement du fichier .mat.")
        # Chargement du fichier .mat avec les options souhaitées
        data = sio.loadmat(mat_file_path, squeeze_me=True, struct_as_record=False)
        # Convertir la donnée en structure serializable (vous devez avoir défini structured_to_serializable)
        data_serializable = structured_to_serializable(data)
        with open(cache_file_path, "wb") as f:
            pickle.dump(data_serializable, f)
        data = data_serializable
        print(f"Chargement du fichier {mat_file_path} terminé.")
    return data

# Exemple d'utilisation
# mat_file = "chemin/vers/votre_fichier.mat"
# data = load_data_with_cache(mat_file)
