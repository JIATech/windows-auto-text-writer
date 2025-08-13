import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Installs PyInstaller if not available"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing PyInstaller: {e}")
            return False

def build_executable():
    """Builds the executable using PyInstaller"""
    script_path = "auto_text_writer.py"
    
    if not os.path.exists(script_path):
        print(f"Error: File {script_path} not found")
        return False
    
    print(f"Building executable from {script_path}...")
    
    # PyInstaller command with options to keep terminal visible
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--console",                    # Keep console window
        "--name", "MU_AutoText",        # Executable name
        "--distpath", "dist",           # Output folder
        "--workpath", "build",          # Temporary folder
        "--specpath", ".",              # .spec file in current directory
        script_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Executable created successfully")
            exe_path = Path("dist/WindowsAutoText_v0.1.exe")
            if exe_path.exists():
                print(f"✓ Executable file: {exe_path.absolute()}")
                print(f"✓ Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print("✗ Executable file not found in expected location")
                return False
        else:
            print("✗ Error during build:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error running PyInstaller: {e}")
        return False

def create_test_batch():
    """Creates a batch file to run the .exe easily"""
    batch_content = '''@echo off
echo ==========================================
echo    MU Auto Text Writer - Executable
echo ==========================================
echo.
echo Starting the program...
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
if exist "dist\\WindowsAutoText_v0.1.exe" (
    "dist\\WindowsAutoText_v0.1.exe"
) else (
    echo Error: WindowsAutoText_v0.1.exe not found in dist folder
    echo.
    echo Make sure you have run build_exe.py first
)

echo.
echo The program has finished.
pause
'''
    
    with open("run_mu_autotext.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✓ Batch file created: run_mu_autotext.bat")

def main():
    print("=" * 50)
    print("    EXECUTABLE BUILDER - MU AUTO TEXT")
    print("=" * 50)
    print()
    
    # Check that the main file exists
    if not os.path.exists("auto_text_writer.py"):
        print("✗ Error: auto_text_writer.py not found")
        print("  Make sure to run this script in the same folder")
        return
    
    # Check that requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("✗ Error: requirements.txt not found")
        print("  Make sure to have the dependencies installed")
        return
    
    # Install dependencies first
    print("1. Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return
    
    # Install PyInstaller
    print("\n2. Checking PyInstaller...")
    if not install_pyinstaller():
        return
    
    # Build executable
    print("\n3. Building executable...")
    if not build_executable():
        return
    
    # Create batch file
    print("\n4. Creating execution file...")
    create_test_batch()
    
    print("\n" + "=" * 50)
    print("    ✓ PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 50)
    print()
    print("Generated files:")
    print("  • dist/WindowsAutoText_v0.1.exe        - Main executable")
    print("  • run_mu_autotext.bat         - File to run easily")
    print()
    print("To test:")
    print("  1. Double-click on 'run_mu_autotext.bat'")
    print("  2. Or run directly 'dist/WindowsAutoText_v0.1.exe'")
    print()
    print("Note: The executable keeps the terminal open to")
    print("      display status messages in real time.")

if __name__ == "__main__":
    main()