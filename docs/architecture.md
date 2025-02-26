# Structure du projet
```
GraphXplore/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt                # ou environment.yml pour Conda
├── docs/                           # Documentation du projet
│   ├── architecture.md             # Description de l'architecture globale
│   └── guide_utilisateur.md        # Manuel d'utilisation et tutoriels
├── virtual_env/
│   ├── init_virtual_env.bat        # Crée l'environnement virtuel
│   ├── open_virtual_env.bat        # Active l'environnement virtuel
│   ├── close_virtual_env.bat       # (Optionnel) Message pour rappeler la commande de désactivation
│   └── delete_virtual_env.bat      # Supprime l'environnement virtuel
├── src/                            # Code source de l'application
│   ├── __init__.py
│   ├── main.py                     # Point d'entrée principal de l'application
│   ├── config.py                   # Fichier de configuration (paramètres, chemins, etc.)
│   ├── data/                       # Modules de gestion des données
│   │   ├── __init__.py
│   │   ├── importer.py             # Importation des données (CSV, HDF5, JSON, etc.)
│   │   ├── preprocessor.py         # Traitement et nettoyage des données
│   │   └── exporter.py             # Exportation des données transformées
│   ├── dashboard/                  # Modules pour l'interface de visualisation
│   │   ├── __init__.py
│   │   ├── app.py                  # Initialisation et configuration de l'application web (Dash/Streamlit)
│   │   ├── layout.py               # Définition de la mise en page et des composants graphiques
│   │   └── callbacks.py            # Gestion des interactions et mises à jour dynamiques
│   ├── utils/                      # Fonctions utilitaires et aides diverses
│   │   ├── __init__.py
│   │   ├── logger.py               # Configuration et gestion du logging
│   │   └── helper.py               # Fonctions d'assistance (ex. transformations, validations)
├── tests/                          # Suite de tests unitaires et d'intégration
│   ├── __init__.py
│   ├── test_data.py                # Tests liés à l'import et au traitement des données
│   ├── test_dashboard.py           # Tests de l'interface et des interactions
│   └── test_utils.py               # Tests des fonctions utilitaires
└── notebooks/                      # Notebooks pour l'exploration et le prototypage
    ├── exploration.ipynb           # Analyse exploratoire des données et essais de visualisation
    └── prototype.ipynb             # Prototype de certaines fonctionnalités avant intégration
