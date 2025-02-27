@echo off
REM Ce script desactive l'environnement virtuel sous Windows.
if exist "virtual_env\venv\" (
    if NOT "%VIRTUAL_ENV%"=="" (
        deactivate
    )
)