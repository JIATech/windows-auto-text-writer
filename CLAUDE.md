# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Windows Auto Text Writer**, a Python automation tool for sending predetermined text commands to Windows applications at configurable intervals. The project has two main versions:

- **v0.1 (Console)**: `auto_text_writer.py` - Command-line interface with interactive configuration
- **v0.3 (GUI)**: `auto_text_writer_gui.py` - Full tkinter GUI with dark/light themes, advanced text management, and complete English translation

## Core Architecture

### Main Components

1. **WindowTextWriter Class** (`auto_text_writer.py`): Core automation engine
   - Window detection and focus management
   - Character-by-character text writing with configurable timing
   - Multi-threaded execution with independent command timers
   - Immediate execution on startup + scheduled intervals

2. **AutoTextWriterGUI Class** (`auto_text_writer_gui.py`): Complete GUI implementation
   - Advanced theming system (dark/light modes)
   - Real-time command management (add/edit/delete/enable/disable)
   - Global hotkey support ('¡' key for start/stop)
   - Live activity logging with timestamps
   - Persistent configuration during session

### Key Technical Patterns

- **Threading**: GUI uses separate execution thread to prevent UI blocking
- **Window Management**: Uses `pygetwindow` for window detection, `pyautogui` for automation
- **Theme System**: Comprehensive ttk.Style configuration for both themes with hover effect removal
- **Text Execution**: Character-by-character typing with configurable speed for any text application

## Build Commands

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run console version
python auto_text_writer.py

# Run GUI version  
python auto_text_writer_gui.py
```

### Build Executables
```bash
# Build console version (.exe with terminal)
python build_exe.py

# Build GUI version (.exe without console window)
python build_gui_exe.py

# Build with size optimization (safe exclusions only)
python build_optimized.py
```

### Build Outputs
- `dist/WindowsAutoText_v0.1.exe` - Console version (~67MB)
- `dist/WindowsAutoText_GUI.exe` - GUI version (~67MB)
- `dist_safe/WindowsAutoText_*_Safe.exe` - Size-optimized builds

## Configuration

### Default Text Examples
The application ships with sample text messages as defaults:
- "Hello, this is a test message." - 5 minute intervals
- "Reminder: check email." - 10 minute intervals  
- "Important note for later." - 15 minute intervals

### Key Configuration Parameters
- **Window Title**: Target application window (default: "Notepad")
- **Typing Speed**: Character delay in seconds (default: 0.2s)
- **Text States**: Each text can be individually enabled/disabled

## Development Notes

### GUI Theme System
The GUI implements a sophisticated theming system that requires careful handling:
- Theme changes affect all ttk widgets and custom styling
- Hover effects are systematically disabled using `ttk.Style.map()`
- LabelFrames require special background handling in dark mode
- Dialog windows need separate theme application

### PyInstaller Considerations
- Standard optimization excludes large libraries (matplotlib, numpy, pandas, etc.)
- Aggressive optimization causes Python DLL errors - use `build_optimized.py` for safe builds
- Both versions produce ~67MB executables due to Python runtime requirements

### Global Hotkey Implementation
Uses `pynput` for system-wide '¡' key detection with proper thread safety via `root.after(0, callback)`.

## File Structure Context
- `requirements.txt`: Minimal dependencies (pyautogui, pygetwindow, pynput)
- `build_*.py`: PyInstaller automation scripts with different optimization levels
- `.gitignore`: Comprehensive exclusions for Python builds, IDEs, and temporary files