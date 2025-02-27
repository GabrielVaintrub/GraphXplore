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

## Données
Les données à impoter doivent être au format ".mat".
Le fichier dataMap.mat est généré par un script MATLAB et constitue le jeu de données de test pour l'application. Il contient une container map globale nommée dataMap qui stocke les données de simulation issues de fichiers s2p.

**Structure de dataMap**
dataMap est une container map où chaque clé correspond au nom d'un fichier s2p (par exemple, "Device_01.s2p", "Device_02.s2p", etc.).
La valeur associée à chaque clé est une autre container map qui contient les informations spécifiques à ce dispositif, notamment :
fileName : Nom du fichier s2p.
filePaths : Chemin d'accès au fichier s2p.
frequences : Vecteur des fréquences mesurées (en Hz).
absS11, absS21, absS12, absS22 : Amplitudes des paramètres S (pour différents ports).
angleS11, angleS21, angleS12, angleS22 : Angles (en radians) des paramètres S.
(Éventuellement, d'autres clés pourront être ajoutées, par exemple 'taille_dispositif' pour certains dispositifs.)

**Exemple MATLAB de création de dataMap**
Le fichier [CreateDataTest](tests/test_datas/CreateDataTest.m) permet de créer le fichier [dataMap](tests/test_datas/dataMap.mat), à partir des données de [1_NoDeembed_FacePortFree](tests/test_datas/1_NoDeembed_FacePortFree).

---
## Licence

Ce projet est sous licence [Nom de la Licence] - voir le fichier [LICENSE](LICENSE) pour plus de détails.