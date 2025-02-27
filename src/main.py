# main.py
import threading
import os
import webview
from dashboard.app import app
from dashboard.layout import layout

# Importer les callbacks pour les enregistrer
import dashboard.callbacks

# Définir le layout de l'application
app.layout = layout

# Fonction pour lancer le serveur Dash
def run_mainwindow():
    app.run_server(debug=True, use_reloader=False)

# Callback appelé lors de la fermeture de la fenêtre
def on_closing_mainwindow():
    print("La fenêtre a été fermée. Exécution des routines de nettoyage.")
    os._exit(0)

if __name__ == '__main__':
    # Démarrer Dash dans un thread séparé en tant que daemon
    dash_thread = threading.Thread(target=run_mainwindow, daemon=True)
    dash_thread.start()

    # Créer une fenêtre native qui charge l'application Dash
    main_window = webview.create_window("GraphXplore", "http://127.0.0.1:8050")
    main_window.events.closing += on_closing_mainwindow
    webview.start()
