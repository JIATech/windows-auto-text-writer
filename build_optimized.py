import subprocess
import sys
import os
from pathlib import Path

def build_safe_optimized():
    """Construye ejecutables con optimizaciones seguras que no rompen funcionalidad"""
    
    print("=" * 60)
    print("    GENERADOR DE EJECUTABLES OPTIMIZADOS SEGUROS")
    print("=" * 60)
    print()
    
    # Verificar que los archivos existen
    files_to_build = [
        ("auto_text_writer.py", "WindowsAutoText_Console_Safe"),
        ("auto_text_writer_gui.py", "WindowsAutoText_GUI_Safe")
    ]
    
    for script_file, output_name in files_to_build:
        if not os.path.exists(script_file):
            print(f"✗ Error: No se encontró {script_file}")
            continue
            
        print(f"Construyendo {output_name}...")
        
        # Comando PyInstaller con optimizaciones SEGURAS
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",                    # Un solo archivo
            "--windowed" if "GUI" in output_name else "--console",
            "--name", output_name,
            "--distpath", "dist_safe",      # Nueva carpeta para builds seguros
            "--workpath", "build_safe",
            "--specpath", ".",
            
            # SOLO optimizaciones seguras
            "--noupx",                      # No usar UPX
            
            # Excluir SOLO módulos que estamos seguros no se usan
            "--exclude-module", "matplotlib",
            "--exclude-module", "numpy", 
            "--exclude-module", "pandas",
            "--exclude-module", "scipy",
            "--exclude-module", "PIL",
            "--exclude-module", "cv2",
            "--exclude-module", "tensorflow",
            "--exclude-module", "torch",
            
            script_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                exe_path = Path(f"dist_optimized/{output_name}.exe")
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / 1024 / 1024
                    print(f"✓ {output_name}.exe creado: {size_mb:.1f} MB")
                else:
                    print(f"✗ {output_name}.exe no encontrado")
            else:
                print(f"✗ Error construyendo {output_name}:")
                print(result.stderr[:500])  # Primeros 500 caracteres del error
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("    COMPARACIÓN DE TAMAÑOS")
    print("=" * 60)
    
    # Comparar tamaños
    compare_sizes()

def build_minimal_size():
    """Construye con enfoque en tamaño mínimo pero funcional"""
    print("\n--- CONSTRUYENDO VERSIÓN TAMAÑO MÍNIMO ---")
    
    # Solo GUI ya que es la más usada
    script_file = "auto_text_writer_gui.py"
    output_name = "WindowsAutoText_GUI_Minimal"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", output_name,
        "--distpath", "dist_minimal",
        "--workpath", "build_minimal",
        "--specpath", ".",
        
        # Optimizaciones moderadas
        "--noupx",
        
        # Solo excluir bibliotecas pesadas que definitivamente no usamos
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas", 
        "--exclude-module", "scipy",
        "--exclude-module", "PIL",
        "--exclude-module", "pillow",
        "--exclude-module", "cv2",
        "--exclude-module", "tensorflow",
        "--exclude-module", "torch",
        "--exclude-module", "sklearn",
        "--exclude-module", "seaborn",
        "--exclude-module", "plotly",
        
        script_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            exe_path = Path(f"dist_minimal/{output_name}.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"✓ Versión mínima creada: {size_mb:.1f} MB")
                print("✓ Esta versión debería funcionar correctamente")
                return True
        else:
            print("✗ Error en construcción mínima:")
            print(result.stderr[:300])
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def compare_sizes():
    """Compara tamaños de todos los ejecutables"""
    print()
    
    # Archivos a comparar
    files_to_check = [
        ("dist/MU_AutoText_v0.1.exe", "Consola Original"),
        ("dist/MU_AutoText_GUI.exe", "GUI Original"),
        ("dist_safe/WindowsAutoText_Console_Safe.exe", "Consola Segura"),
        ("dist_safe/WindowsAutoText_GUI_Safe.exe", "GUI Segura"),
        ("dist_minimal/WindowsAutoText_GUI_Minimal.exe", "GUI Mínima"),
    ]
    
    print("Comparación de tamaños:")
    print("-" * 50)
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / 1024 / 1024
            print(f"{description:20} | {size_mb:6.1f} MB")
        else:
            print(f"{description:20} | No encontrado")

def main():
    print("🔧 DIAGNÓSTICO: El error de Python DLL indica que las optimizaciones")
    print("   anteriores fueron demasiado agresivas y rompieron dependencias.")
    print()
    print("Opciones de construcción SEGURAS:")
    print("1. 🛡️  Optimización segura (sin romper funcionalidad)")
    print("2. 📦 Tamaño mínimo (solo bibliotecas grandes excluidas)")
    print("3. 📊 Comparar tamaños existentes")
    print("4. 🧹 Limpiar builds problemáticos")
    
    choice = input("\nElige una opción (1-4): ").strip()
    
    if choice == "1":
        build_safe_optimized()
    elif choice == "2":
        success = build_minimal_size()
        if success:
            print("\n🎉 ¡Construcción exitosa! Prueba el ejecutable.")
    elif choice == "3":
        compare_sizes()
    elif choice == "4":
        clean_problematic_builds()
    else:
        print("Opción no válida")

def clean_problematic_builds():
    """Limpia builds que causan problemas"""
    import shutil
    
    dirs_to_clean = ["dist_optimized", "build_temp", "build_safe", "build_minimal"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Limpiado: {dir_name}")
            except Exception as e:
                print(f"✗ Error limpiando {dir_name}: {e}")
        else:
            print(f"- {dir_name} no existe")
    
    print("\n🧹 Limpieza completada. Ahora puedes intentar builds seguros.")

if __name__ == "__main__":
    main()