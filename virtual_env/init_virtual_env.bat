@echo off
REM Ce script crée un environnement virtuel nommé "venv" dans le dossier \virtual_env.
if not exist "virtual_env\venv\" (
    echo Creation de l'environnement virtuel...
    REM TODO verrifier la version de python et installer la bonne
    python -m venv virtual_env\venv
    echo Environnement virtuel cree dans ..\venv.
) else (
    echo L'environnement virtuel existe deja.
)
call virtual_env\open_virtual_env.bat