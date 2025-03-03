# src/dashboard/upload.py
import tkinter as tk
from tkinter import filedialog

def tk_file_dialog():
    """Ouvre une boîte de dialogue Tkinter pour sélectionner des fichiers .mat
    et retourne la liste des chemins complets sélectionnés."""
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    file_paths = filedialog.askopenfilenames(
        title="Sélectionnez des fichiers .mat",
        filetypes=[("MATLAB Files", "*.mat")]
    )
    root.destroy()
    return list(file_paths)
