@echo off
REM Ce script supprime l'environnement virtuel sous Windows.
if exist "virtual_env\venv\" (
    deactivate
    del virtual_env\venv\
)