import os
import shutil
import stat
from config import __TEMP_DIR__


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
    if not os.path.exists(__TEMP_DIR__):
        os.makedirs(__TEMP_DIR__)
    remove_read_only(__TEMP_DIR__)

def clear_temp_dir():
    if os.path.exists(__TEMP_DIR__):
        try:
            shutil.rmtree(__TEMP_DIR__)
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier {__TEMP_DIR__}: {e}")


