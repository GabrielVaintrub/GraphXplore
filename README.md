# GraphXplore

Une application d'affichage interactive pour l'analyse des données de mesures et de simulations électromagnétiques.

---

## Contexte et Objectifs

Dans le cadre de ma thèse en électromagnétisme, je traite un grand volume de données issues de mesures (fichiers S2P, simulations HFSS, etc.). L'objectif principal de ce projet est de développer une application en Python permettant d'importer, traiter et visualiser ces données de manière interactive afin d'extraire des informations clés (perméabilité, permittivité, paramètres S, matrices ABCD/T, etc.).

Les objectifs du projet sont :
- **Optimiser l'analyse des données :** Faciliter l'interprétation des mesures et simulations.
- **Offrir une visualisation interactive :** Permettre le filtrage, la superposition et la comparaison de différentes séries de données.
- **Assurer la reproductibilité et l'évolutivité :** Utiliser une architecture modulaire et containerisée (via Docker).

---

## Fonctionnalités

- **Importation des données :**
  - Chargement de fichiers exportés depuis MATLAB (CSV, HDF5, JSON, ou .mat).
  - Gestion des données hétérogènes (vecteurs de tailles variables, données manquantes).

- **Traitement et Prévisualisation :**
  - Nettoyage, filtrage et transformation des données.
  - Calcul de paramètres spécifiques (exposant de propagation, matrices ABCD/T, etc.).

- **Visualisation Interactive :**
  - Dashboard interactif développé avec Dash ou Streamlit.
  - Outils de filtrage, zoom, et superposition de courbes (expérimentales vs théoriques).

- **Exportation et Partage :**
  - Possibilité d'exporter les graphiques et les données filtrées en formats standards (CSV, PNG, PDF).

- **Déploiement et Containerisation :**
  - Conteneurisation de l'application avec Docker pour une reproductibilité sur différents environnements.

---

## Architecture du Projet

Pour une description détaillée de l'architecture du projet, veuillez consulter le fichier [docs/architecture.md](docs/architecture.md).

---

## Gestion de l'Environnement Virtuel

Le projet utilise `venv` pour isoler ses dépendances. Des scripts utiles se trouvent dans le dossier `virtual_env/` :

- `init_virtual_env` : Crée l'environnement virtuel (doit être exécuté une seule fois).
- `open_virtual_env` : Active l'environnement virtuel (à "sourcer" dans votre terminal).
- `close_virtual_env` : Rappel pour désactiver l'environnement (utilisez la commande `deactivate`).
- `delete_virtual_env` : Supprime l'environnement virtuel.

---

## Installation

---

## Licence

Ce projet est sous licence [Nom de la Licence] - voir le fichier [LICENSE](LICENSE) pour plus de détails.