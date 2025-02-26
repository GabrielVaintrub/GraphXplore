@echo off
REM Ce script active l'environnement virtuel sous Windows.
if exist "virtual_env\venv\Scripts\activate.bat" (
    call virtual_env\venv\Scripts\activate.bat
    call pip install -r requirements.txt
) else (
    call virtual_env\init_virtual_env.bat
)