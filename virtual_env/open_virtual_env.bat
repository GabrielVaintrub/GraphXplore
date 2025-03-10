@echo off
REM Ce script active l'environnement virtuel sous Windows.
if exist "virtual_env\venv\Scripts\activate.bat" (
    echo Verrification de l'etat de l'environement virtuel.
    if "%VIRTUAL_ENV%"=="" (
        echo Activation de l'environement virtuel.
        call virtual_env\venv\Scripts\activate.bat
    ) else (
        echo L'environement virtuel est deja active.
    )
    REM Installer les dépendances
    if "%~1"=="--safe-mode" (
            call pip install -r requirements.txt
    )
) else (
    call virtual_env\create_virtual_env.bat
)