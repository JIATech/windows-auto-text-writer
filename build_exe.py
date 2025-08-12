import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("PyInstaller ya está instalado")
        return True
    except ImportError:
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller instalado exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error instalando PyInstaller: {e}")
            return False

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    script_path = "auto_text_writer.py"
    
    if not os.path.exists(script_path):
        print(f"Error: No se encontró el archivo {script_path}")
        return False
    
    print(f"Construyendo ejecutable de {script_path}...")
    
    # Comando PyInstaller con opciones para mantener terminal visible
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--console",                    # Mantener ventana de consola
        "--name", "MU_AutoText",        # Nombre del ejecutable
        "--distpath", "dist",           # Carpeta de salida
        "--workpath", "build",          # Carpeta temporal
        "--specpath", ".",              # Archivo .spec en directorio actual
        script_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Ejecutable creado exitosamente")
            exe_path = Path("dist/MU_AutoText.exe")
            if exe_path.exists():
                print(f"✓ Archivo ejecutable: {exe_path.absolute()}")
                print(f"✓ Tamaño: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print("✗ El archivo ejecutable no se encontró en la ubicación esperada")
                return False
        else:
            print("✗ Error durante la construcción:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error ejecutando PyInstaller: {e}")
        return False

def create_test_batch():
    """Crea un archivo batch para ejecutar el .exe fácilmente"""
    batch_content = '''@echo off
echo ==========================================
echo    MU Auto Text Writer - Ejecutable
echo ==========================================
echo.
echo Iniciando el programa...
echo Presiona Ctrl+C para detener
echo.

cd /d "%~dp0"
if exist "dist\\MU_AutoText.exe" (
    "dist\\MU_AutoText.exe"
) else (
    echo Error: No se encontró MU_AutoText.exe en la carpeta dist
    echo.
    echo Asegúrate de haber ejecutado build_exe.py primero
)

echo.
echo El programa ha terminado.
pause
'''
    
    with open("ejecutar_mu_autotext.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✓ Archivo batch creado: ejecutar_mu_autotext.bat")

def main():
    print("=" * 50)
    print("    GENERADOR DE EJECUTABLE - MU AUTO TEXT")
    print("=" * 50)
    print()
    
    # Verificar que el archivo principal existe
    if not os.path.exists("auto_text_writer.py"):
        print("✗ Error: No se encontró auto_text_writer.py")
        print("  Asegúrate de ejecutar este script en la misma carpeta")
        return
    
    # Verificar que requirements.txt existe
    if not os.path.exists("requirements.txt"):
        print("✗ Error: No se encontró requirements.txt")
        print("  Asegúrate de tener las dependencias instaladas")
        return
    
    # Instalar dependencias primero
    print("1. Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencias instaladas")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error instalando dependencias: {e}")
        return
    
    # Instalar PyInstaller
    print("\n2. Verificando PyInstaller...")
    if not install_pyinstaller():
        return
    
    # Construir ejecutable
    print("\n3. Construyendo ejecutable...")
    if not build_executable():
        return
    
    # Crear archivo batch
    print("\n4. Creando archivo de ejecución...")
    create_test_batch()
    
    print("\n" + "=" * 50)
    print("    ✓ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 50)
    print()
    print("Archivos generados:")
    print("  • dist/MU_AutoText.exe        - Ejecutable principal")
    print("  • ejecutar_mu_autotext.bat    - Archivo para ejecutar fácilmente")
    print()
    print("Para probar:")
    print("  1. Haz doble clic en 'ejecutar_mu_autotext.bat'")
    print("  2. O ejecuta directamente 'dist/MU_AutoText.exe'")
    print()
    print("Nota: El ejecutable mantiene la terminal abierta para")
    print("      mostrar los mensajes de estado en tiempo real.")

if __name__ == "__main__":
    main()