import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("✓ PyInstaller ya está instalado")
        return True
    except ImportError:
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller instalado exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error instalando PyInstaller: {e}")
            return False

def build_gui_executable():
    """Construye el ejecutable GUI usando PyInstaller"""
    script_path = "auto_text_writer_gui.py"
    
    if not os.path.exists(script_path):
        print(f"✗ Error: No se encontró el archivo {script_path}")
        return False
    
    print(f"Construyendo ejecutable GUI de {script_path}...")
    
    # Comando PyInstaller con opciones específicas para GUI
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                       # Un solo archivo ejecutable
        "--windowed",                      # Sin ventana de consola (para GUI)
        "--name", "MU_AutoText_GUI",       # Nombre del ejecutable
        "--distpath", "dist",              # Carpeta de salida
        "--workpath", "build",             # Carpeta temporal
        "--specpath", ".",                 # Archivo .spec en directorio actual
        "--icon", "NONE",                  # Sin icono personalizado
        "--add-data", "requirements.txt;.", # Incluir requirements.txt
        script_path
    ]
    
    try:
        print("Ejecutando PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Ejecutable GUI creado exitosamente")
            exe_path = Path("dist/MU_AutoText_GUI.exe")
            if exe_path.exists():
                print(f"✓ Archivo ejecutable: {exe_path.absolute()}")
                print(f"✓ Tamaño: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print("✗ El archivo ejecutable no se encontró en la ubicación esperada")
                return False
        else:
            print("✗ Error durante la construcción:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error ejecutando PyInstaller: {e}")
        return False

def create_gui_batch():
    """Crea un archivo batch para ejecutar el .exe GUI fácilmente"""
    batch_content = '''@echo off
title MU Auto Text Writer GUI v0.2
echo ==========================================
echo    MU Auto Text Writer GUI - v0.2
echo ==========================================
echo.
echo Iniciando la aplicación GUI...
echo.

cd /d "%~dp0"
if exist "dist\\MU_AutoText_GUI.exe" (
    echo Ejecutando MU_AutoText_GUI.exe...
    "dist\\MU_AutoText_GUI.exe"
) else (
    echo Error: No se encontró MU_AutoText_GUI.exe en la carpeta dist
    echo.
    echo Asegúrate de haber ejecutado build_gui_exe.py primero
    echo.
    pause
)
'''
    
    with open("ejecutar_mu_gui.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✓ Archivo batch GUI creado: ejecutar_mu_gui.bat")

def create_readme():
    """Crea un archivo README con instrucciones"""
    readme_content = '''# MU Auto Text Writer v0.2 - Ejecutable GUI

## Archivos Generados

- `dist/MU_AutoText_GUI.exe` - Ejecutable principal de la aplicación GUI
- `ejecutar_mu_gui.bat` - Archivo batch para ejecutar fácilmente

## Cómo usar

### Opción 1: Archivo Batch (Recomendado)
1. Haz doble clic en `ejecutar_mu_gui.bat`

### Opción 2: Ejecutable Directo
1. Navega a la carpeta `dist/`
2. Haz doble clic en `MU_AutoText_GUI.exe`

## Características de la v0.2

### Control por Tecla
- Presiona la tecla `¡` desde cualquier lugar para iniciar/detener

### Interfaz Gráfica
- Configuración visual del título de ventana y velocidad
- Gestión completa de comandos (agregar, editar, eliminar)
- Lista visual de comandos con estado (Activo/Desactivado)
- Log en tiempo real de la actividad

### Funcionalidades
- Comandos por defecto incluidos
- Activar/desactivar comandos individualmente
- Validación de datos automática
- Monitoreo de próximas ejecuciones

## Comandos por Defecto

1. `/attack on` - cada 91 minutos
2. `/pickjewel on` - cada 31 minutos  
3. `/party on` - cada 32 minutos

## Uso Básico

1. Abrir la aplicación
2. Verificar/configurar el título de ventana (default: "MU La Plata 99B")
3. Ajustar velocidad de escritura si es necesario
4. Revisar comandos en la lista
5. Presionar `¡` o el botón "Iniciar" para comenzar
6. Presionar `¡` nuevamente para detener

## Notas Importantes

- El ejecutable NO requiere Python instalado
- Incluye todas las dependencias necesarias
- Interfaz completamente autónoma
- Los logs se muestran en tiempo real
- Configuración persistente durante la sesión

## Solución de Problemas

Si el ejecutable no funciona:
1. Verificar que la ventana objetivo esté abierta
2. Verificar que el título de ventana coincida exactamente
3. Revisar los logs en la aplicación para mensajes de error

---
Generado con MU Auto Text Writer Build System v0.2
'''
    
    with open("README_GUI.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ Archivo README creado: README_GUI.md")

def main():
    print("=" * 60)
    print("    GENERADOR DE EJECUTABLE GUI - MU AUTO TEXT v0.2")
    print("=" * 60)
    print()
    
    # Verificar que el archivo principal existe
    if not os.path.exists("auto_text_writer_gui.py"):
        print("✗ Error: No se encontró auto_text_writer_gui.py")
        print("  Asegúrate de ejecutar este script en la misma carpeta")
        return
    
    # Verificar que requirements.txt existe
    if not os.path.exists("requirements.txt"):
        print("✗ Error: No se encontró requirements.txt")
        print("  Asegúrate de tener las dependencias listadas")
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
    
    # Construir ejecutable GUI
    print("\n3. Construyendo ejecutable GUI...")
    if not build_gui_executable():
        return
    
    # Crear archivo batch
    print("\n4. Creando archivo de ejecución...")
    create_gui_batch()
    
    # Crear README
    print("\n5. Creando documentación...")
    create_readme()
    
    print("\n" + "=" * 60)
    print("    ✓ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Archivos generados:")
    print("  • dist/MU_AutoText_GUI.exe      - Ejecutable GUI principal")
    print("  • ejecutar_mu_gui.bat           - Launcher de la aplicación")
    print("  • README_GUI.md                 - Documentación de uso")
    print()
    print("Para usar la aplicación GUI:")
    print("  1. Haz doble clic en 'ejecutar_mu_gui.bat'")
    print("  2. O ejecuta directamente 'dist/MU_AutoText_GUI.exe'")
    print()
    print("Características de la v0.2:")
    print("  • Interfaz gráfica profesional")
    print("  • Control con tecla '¡' desde cualquier lugar")
    print("  • Gestión completa de comandos")
    print("  • Log en tiempo real")
    print("  • Sin dependencias externas (ejecutable independiente)")
    print()
    print("¡La aplicación está lista para usar!")

if __name__ == "__main__":
    main()