import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Installs PyInstaller if not available"""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing PyInstaller: {e}")
            return False

def build_gui_executable():
    """Builds the GUI executable using PyInstaller"""
    script_path = "auto_text_writer_gui.py"
    
    if not os.path.exists(script_path):
        print(f"✗ Error: File {script_path} not found")
        return False
    
    print(f"Building GUI executable from {script_path}...")
    
    # PyInstaller command with GUI-specific options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                       # Single executable file
        "--windowed",                      # No console window (for GUI)
        "--name", "WindowsAutoText_GUI",       # Executable name
        "--distpath", "dist",              # Output folder
        "--workpath", "build",             # Temporary folder
        "--specpath", ".",                 # .spec file in current directory
        "--icon", "NONE",                  # No custom icon
        "--add-data", "requirements.txt;.", # Include requirements.txt
        "--add-data", "i18n.py;.",          # Include internationalization system
        "--add-data", "config.py;.",        # Include configuration system
        "--add-data", "lang;lang",          # Include language files directory
        "--hidden-import", "json",          # Ensure JSON module is included
        "--hidden-import", "pathlib",       # Ensure pathlib is included
        script_path
    ]
    
    try:
        print("Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ GUI executable created successfully")
            exe_path = Path("dist/WindowsAutoText_GUI.exe")
            if exe_path.exists():
                print(f"✓ Executable file: {exe_path.absolute()}")
                print(f"✓ Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                return True
            else:
                print("✗ Executable file not found in expected location")
                return False
        else:
            print("✗ Error during build:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error running PyInstaller: {e}")
        return False

def create_gui_batch():
    """Creates a batch file to run the GUI .exe easily"""
    batch_content = '''@echo off
title Windows Auto Text Writer GUI v0.4
echo ==========================================
echo    Windows Auto Text Writer GUI - v0.4
echo ==========================================
echo.
echo Starting GUI application...
echo.

cd /d "%~dp0"
if exist "dist\\WindowsAutoText_GUI.exe" (
    echo Running WindowsAutoText_GUI.exe...
    "dist\\WindowsAutoText_GUI.exe"
) else (
    echo Error: WindowsAutoText_GUI.exe not found in dist folder
    echo.
    echo Make sure you have run build_gui_exe.py first
    echo.
    pause
)
'''
    
    with open("run_mu_gui.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("✓ GUI batch file created: run_mu_gui.bat")

def create_readme():
    """Creates a README file with instructions"""
    readme_content = '''# Windows Auto Text Writer v0.4 - GUI Executable

## Generated Files

- `dist/WindowsAutoText_GUI.exe` - Main GUI application executable
- `run_mu_gui.bat` - Batch file to run easily

## How to Use

### Option 1: Batch File (Recommended)
1. Double-click on `run_mu_gui.bat`

### Option 2: Direct Executable
1. Navigate to the `dist/` folder
2. Double-click on `WindowsAutoText_GUI.exe`

## v0.2 Features

### Hotkey Control
- Press the `¡` key from anywhere to start/stop

### Graphical Interface
- Visual configuration of window title and speed
- Complete command management (add, edit, delete)
- Visual command list with status (Active/Disabled)
- Real-time activity logging

### Functionality
- Default commands included
- Enable/disable commands individually
- Automatic data validation
- Next execution monitoring

## Default Commands

1. `/attack on` - every 91 minutes
2. `/pickjewel on` - every 31 minutes  
3. `/party on` - every 32 minutes

## Basic Usage

1. Open the application
2. Verify/configure window title (default: "MU La Plata 99B")
3. Adjust typing speed if necessary
4. Review commands in the list
5. Press `¡` or the "Start" button to begin
6. Press `¡` again to stop

## Important Notes

- The executable does NOT require Python installed
- Includes all necessary dependencies
- Completely standalone interface
- Logs are shown in real time
- Persistent configuration during session

## Troubleshooting

If the executable doesn't work:
1. Verify that the target window is open
2. Verify that the window title matches exactly
3. Check the logs in the application for error messages

---
Generated with MU Auto Text Writer Build System v0.2
'''
    
    with open("README_GUI.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ README file created: README_GUI.md")

def main():
    print("=" * 60)
    print("    GUI EXECUTABLE BUILDER - WINDOWS AUTO TEXT v0.4")
    print("=" * 60)
    print()
    
    # Check that the main file exists
    if not os.path.exists("auto_text_writer_gui.py"):
        print("✗ Error: auto_text_writer_gui.py not found")
        print("  Make sure to run this script in the same folder")
        return
    
    # Check that requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("✗ Error: requirements.txt not found")
        print("  Make sure to have the dependencies listed")
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
    
    # Build GUI executable
    print("\n3. Building GUI executable...")
    if not build_gui_executable():
        return
    
    # Create batch file
    print("\n4. Creating execution file...")
    create_gui_batch()
    
    # Create README
    print("\n5. Creating documentation...")
    create_readme()
    
    print("\n" + "=" * 60)
    print("    ✓ PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print()
    print("Generated files:")
    print("  • dist/WindowsAutoText_GUI.exe      - Main GUI executable")
    print("  • run_mu_gui.bat               - Application launcher")
    print("  • README_GUI.md                 - Usage documentation")
    print()
    print("To use the GUI application:")
    print("  1. Double-click on 'run_mu_gui.bat'")
    print("  2. Or run directly 'dist/WindowsAutoText_GUI.exe'")
    print()
    print("v0.2 Features:")
    print("  • Professional graphical interface")
    print("  • Control with '¡' key from anywhere")
    print("  • Complete command management")
    print("  • Real-time logging")
    print("  • No external dependencies (standalone executable)")
    print()
    print("The application is ready to use!")

if __name__ == "__main__":
    main()