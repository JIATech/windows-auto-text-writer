@echo off
echo ==========================================
echo    MU Auto Text Writer - Ejecutable
echo ==========================================
echo.
echo Iniciando el programa...
echo Presiona Ctrl+C para detener
echo.

cd /d "%~dp0"
if exist "dist\MU_AutoText.exe" (
    "dist\MU_AutoText.exe"
) else (
    echo Error: No se encontró MU_AutoText.exe en la carpeta dist
    echo.
    echo Asegúrate de haber ejecutado build_exe.py primero
)

echo.
echo El programa ha terminado.
pause
