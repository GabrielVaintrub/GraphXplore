@echo off
REM Ce script supprime l'environnement virtuel sous Windows.
if exist "virtual_env\venv\" (
    call virtual_env\close_virtual_env.bat
    rmdir /s /q virtual_env\venv\
)