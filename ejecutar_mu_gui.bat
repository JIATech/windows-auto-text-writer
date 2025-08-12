@echo off
title MU Auto Text Writer GUI v0.2
echo ==========================================
echo    MU Auto Text Writer GUI - v0.2
echo ==========================================
echo.
echo Iniciando la aplicación GUI...
echo.

cd /d "%~dp0"
if exist "dist\MU_AutoText_GUI.exe" (
    echo Ejecutando MU_AutoText_GUI.exe...
    "dist\MU_AutoText_GUI.exe"
) else (
    echo Error: No se encontró MU_AutoText_GUI.exe en la carpeta dist
    echo.
    echo Asegúrate de haber ejecutado build_gui_exe.py primero
    echo.
    pause
)
