@echo off
SET "ENV_DIR=venv"

REM IF NOT EXIST "%ENV_DIR%\Scripts\activate.bat" (
call virtual_env\create_virtual_env.bat
REM ) ELSE (
   REM  echo L'environnement virtuel existe déjà.
REM )

REM Activer l'environnement virtuel
if "%~1"=="--safe-mode" (
   call virtual_env\open_virtual_env.bat --safe-mode
) else (
   call virtual_env\open_virtual_env.bat
)
REM TODO Vérifier la version de Python
REM python --version

REM Lancer l'application
python src\main.py
REM echo
REM echo Press any key to exit . . .
REM pause>nul
