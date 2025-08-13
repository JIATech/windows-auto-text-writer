# Windows Auto Text Writer

Windows automation tool that sends predetermined text commands to applications at configurable intervals.

![Screenshot](https://img.shields.io/badge/Platform-Windows-blue)
![Python Version](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🚀 Features

- **Two versions available**: Console (v0.1) and GUI (v0.5)
- **Automatic writing**: Character-by-character text with configurable speed
- **Multiple commands**: Each command with its own independent timer
- **Global control**: Hotkey ('¡') from any application
- **Modern interface**: GUI with dark/light mode and multi-language support
- **Complete management**: Add, edit, delete and enable/disable commands
- **Session persistence**: All settings automatically saved between sessions
- **Real-time logging**: Activity log with timestamps
- **Standalone executables**: No Python installation required

## 📋 Requirements

### To run from source code:
- Python 3.7 or higher
- Windows (required for pygetwindow and pyautogui)

### Dependencies:
```
pyautogui==0.9.54
pygetwindow==0.0.9
pynput==1.7.6
```

## 🛠️ Installation

### Option 1: Executables (Recommended)
1. Download executables from the [Releases](../../releases) section
   - Complete standalone application with all languages included
   - No Python installation required
   - All translation files embedded automatically

### Option 2: From source code
```bash
# Clone repository
git clone https://github.com/JIATech/windows-auto-text-writer.git
cd windows-auto-text-writer

# Install dependencies
pip install -r requirements.txt

# Run
python auto_text_writer.py          # Console version
python auto_text_writer_gui.py      # GUI version
```

## 🎮 Usage

### GUI Version (v0.5) - Recommended

1. **Language selection**:
   - Choose between English and Spanish
   - Interface updates instantly
   - Preferences saved automatically

2. **Initial configuration**:
   - Target window title (partial matching supported)
   - Writing speed (seconds between characters, default: 0.2s)
   - Auto-save toggle (enabled by default)

3. **Text management**:
   - Add custom texts
   - Load default example texts (adapts to selected language)
   - Edit intervals and enable/disable individually

4. **Control**:
   - "Start" button or '¡' key to begin
   - Immediate execution of all texts at startup
   - Then continues with independent timers

5. **Additional features**:
   - Complete session persistence (all settings saved automatically)
   - Configurable auto-save (can be enabled/disabled by user)
   - Smart exit confirmation (asks to save unsaved changes when auto-save is off)
   - Manual save button for users who prefer manual control
   - Dark/light mode with toggle button
   - Real-time log with translated messages
   - Multi-language "About" dialog
   - Smart content localization (preserves custom window titles)

### Console Version (v0.1)

1. Run `auto_text_writer.py`
2. Follow the interactive configuration wizard
3. Press Ctrl+C to stop

## 🔨 Build executables

```bash
# Console version
python build_exe.py

# GUI version
python build_gui_exe.py

# Optimized version (smaller size)
python build_optimized.py
```

Executables are generated in `dist/` and `dist_safe/` folders.

## 📁 Project structure

```
├── auto_text_writer.py       # Console version (v0.1)
├── auto_text_writer_gui.py   # GUI version (v0.5)
├── i18n.py                  # Internationalization system
├── config.py                # Configuration management
├── lang/                    # Language files directory
│   ├── en.json             # English translations
│   └── es.json             # Spanish translations
├── build_exe.py             # Console build script
├── build_gui_exe.py         # GUI build script
├── build_optimized.py       # Size-optimized build
├── requirements.txt         # Dependencies
├── CLAUDE.md               # Development documentation
└── README.md               # This file
```

## ⚙️ Advanced configuration

### Main parameters:
- **Window title**: Partial match in target window name
- **Writing speed**: 0.1 (fast) to 2.0+ (slow) seconds per character
- **Intervals**: Time in minutes between command executions

### Global hotkey:
- **'¡'**: Start/stop from any application (GUI only)

## 🐛 Troubleshooting

### Application doesn't find the window:
- Use a distinctive part of the window title
- Make sure the window is open and visible
- If there are multiple windows with the same text, check the log to see which one it's using

### Commands don't type correctly:
- Adjust writing speed (try higher values)
- Verify that the target window has focus

### Python DLL error in executables:
- Use `build_optimized.py` instead of aggressive optimizations
- Standard executables (~67MB) include all necessary dependencies

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 👤 Author

**JIATech**
- Email: johndev@jiacode.dev

## 📋 Version history

### v0.5 (Current)
- ✅ **Complete session persistence**: All user settings, texts, and preferences saved automatically
- ✅ **Configurable auto-save**: Users can enable/disable automatic saving with toggle in Configuration
- ✅ **Smart exit confirmation**: Intelligent dialog asks to save unsaved changes (when auto-save disabled)
- ✅ **Manual save control**: Save button allows users to save changes manually when needed
- ✅ **Enhanced UI polish**: Fixed visual issues with checkbox display (no more confusing "1/0" values)
- ✅ **Complete multi-language support**: English/Spanish with intelligent language switching
- ✅ **Smart localization**: Default content adapts automatically, preserves custom user input
- ✅ **Enhanced configuration system**: Robust settings management with automatic migration
- ✅ **Intelligent UI updates**: Live language switching without losing user configuration
- ✅ **Enhanced window search**: Supports partial title matching with smart detection
- ✅ **Optimized performance**: Faster typing speed (0.2s) and universal text examples

### v0.4
- ✅ **Multi-language foundation**: English/Spanish interface implementation
- ✅ **Enhanced window search**: Supports partial title matching with smart detection
- ✅ **Improved logging**: Clear feedback on window detection and conflict warnings
- ✅ **Optimized performance**: Faster typing speed (0.2s) and universal text examples
- ✅ **Professional interface**: Clean English UI suitable for international users

### v0.3
- ✅ **English translation**: Complete english translation from spanish

### v0.2.1
- ✅ **Enhanced window search**: Partial matching in titles with smart detection
- ✅ **Smart detection**: Prioritizes visible windows when there are multiple matches
- ✅ **Improved logging**: Reports which window is being used and warns about multiple matches
- ✅ **Updated interface**: Label clarified as "Window title (partial)"
- ✅ **Universal examples**: Generic example texts instead of game-specific commands
- ✅ **Optimized speed**: Default speed reduced to 0.2s for better experience

### v0.2
- ✅ Complete graphical interface with tkinter
- ✅ Advanced text management (add, edit, delete)
- ✅ Dark/light mode
- ✅ Global control with '¡' key
- ✅ Real-time log
- ✅ Immediate execution + independent timers

### v0.1
- ✅ Basic console version
- ✅ Interactive configuration
- ✅ Character-by-character writing

## 🙏 Acknowledgments

- [PyAutoGUI](https://pyautogui.readthedocs.io/) - GUI automation
- [PyGetWindow](https://github.com/asweigart/PyGetWindow) - Window management
- [pynput](https://github.com/moses-palmer/pynput) - Global key detection

---

⭐ If this project was useful to you, consider giving it a star!