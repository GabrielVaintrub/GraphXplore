@echo off
REM Ce script active l'environnement virtuel sous Windows.
if exist "virtual_env\venv\Scripts\activate.bat" (
    if "%VIRTUAL_ENV%"=="" (
        call virtual_env\venv\Scripts\activate.bat
    )
) else (
    call virtual_env\create_virtual_env.bat
)