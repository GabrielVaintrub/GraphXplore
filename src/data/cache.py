# src/data/cache.py

import os, pickle, json
# import scipy.io as sio
# import time
from config import __TEMP_DIR__

# Dossier de cache 
CACHE_DIR = os.path.join(__TEMP_DIR__, "cache")             #"temp/cache"

def get_cache_file_path(json_file_path):
    """
    Renvoie le chemin du fichier cache (pickle) associé au fichier JSON.
    Par exemple, "dataTable.json" donnera "dataTable.pkl" dans le dossier CACHE_DIR.
    """
    base_name = os.path.basename(json_file_path)
    cache_file_name = os.path.splitext(base_name)[0] + ".pkl"
    return os.path.join(CACHE_DIR, cache_file_name)

def is_cache_up_to_date(json_file_path, cache_file_path):
    """
    Vérifie si le fichier cache existe et s'il est plus récent que le fichier JSON source.
    """
    if not os.path.exists(cache_file_path):
        return False
    return os.path.getmtime(cache_file_path) >= os.path.getmtime(json_file_path)

def load_data_with_cache(json_file_path):
    """
    Charge les données depuis un fichier JSON en utilisant un cache pickle.
    
    Si le cache existe et est à jour, il est chargé pour accélérer l'accès aux données.
    Sinon, le fichier JSON est lu, converti en objet Python et sauvegardé dans le cache.
    
    Retourne:
        Les données sous forme d'objet Python (typiquement un dictionnaire ou une liste).
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file_path = get_cache_file_path(json_file_path)
    
    if is_cache_up_to_date(json_file_path, cache_file_path):
        print(f"Chargement du cache : {cache_file_path}")
        with open(cache_file_path, "rb") as f:
            data = pickle.load(f)
    else:
        print(f"Cache obsolète ou inexistant pour {json_file_path}. Chargement du fichier JSON.")
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Sauvegarder le cache pour accélérer les futurs chargements
        with open(cache_file_path, "wb") as f:
            pickle.dump(data, f)
    return data
