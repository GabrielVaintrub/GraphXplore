import os
import shutil
import stat

# Définir le chemin du dossier temporaire
TEMP_DIR = "temp"

def remove_read_only(path):
    """Retire l'attribut lecture seule du dossier 'path' et de tous ses contenus."""
    for root, dirs, files in os.walk(path):
        for d in dirs:
            dir_path = os.path.join(root, d)
            os.chmod(dir_path, stat.S_IWRITE)
        for f in files:
            file_path = os.path.join(root, f)
            os.chmod(file_path, stat.S_IWRITE)

def create_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    remove_read_only(TEMP_DIR)

def clear_temp_dir():
    if os.path.exists(TEMP_DIR):
        try:
            shutil.rmtree(TEMP_DIR)
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier {TEMP_DIR}: {e}")


