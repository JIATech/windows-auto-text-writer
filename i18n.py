import json
import os
from pathlib import Path

class I18n:
    """Internationalization manager for multi-language support"""
    
    def __init__(self, default_language='en'):
        self.current_language = default_language
        self.languages = {}
        self.available_languages = {
            'en': 'English',
            'es': 'Español'
        }
        self.load_languages()
        
    def load_languages(self):
        """Load all available language files"""
        lang_dir = Path(__file__).parent / 'lang'
        
        if not lang_dir.exists():
            # If lang directory doesn't exist, create it and use fallback
            lang_dir.mkdir(exist_ok=True)
            self.languages = self._get_fallback_languages()
            return
            
        for lang_code in self.available_languages.keys():
            lang_file = lang_dir / f"{lang_code}.json"
            
            try:
                if lang_file.exists():
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                else:
                    # Use fallback if file doesn't exist
                    self.languages[lang_code] = self._get_fallback_language(lang_code)
                    
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading language {lang_code}: {e}")
                self.languages[lang_code] = self._get_fallback_language(lang_code)
    
    def _get_fallback_languages(self):
        """Fallback languages if files are not available"""
        return {
            'en': self._get_fallback_language('en'),
            'es': self._get_fallback_language('es')
        }
    
    def _get_fallback_language(self, lang_code):
        """Get fallback language data"""
        if lang_code == 'en':
            return {
                "app": {"title": "Windows Auto Text Writer v0.4", "version": "Version 0.4"},
                "ui": {"configuration": "Configuration", "window_title": "Window title (partial):", "typing_speed": "Speed (sec/char):", "commands": "Commands", "control": "Control", "activity_log": "Activity Log", "language": "Language:", "auto_save": "Auto-save changes:", "about": "About"},
                "buttons": {"add_command": "Add Command", "edit_command": "Edit Command", "delete_command": "Delete Command", "load_defaults": "Load Defaults", "start": "Start (¡)", "stop": "Stop (¡)", "save": "Save", "cancel": "Cancel", "close": "Close"},
                "defaults": {"window_title": "Notepad", "test_message": "Hello, this is a test message.", "reminder_message": "Reminder: check email.", "note_message": "Important note for later."},
                "messages": {"status_stopped": "Stopped - Press '¡' to start", "status_running": "Running - Press '¡' to stop"},
                "log": {"language_changed": "Language changed to English"}
            }
        else:  # Spanish
            return {
                "app": {"title": "Windows Auto Text Writer v0.4", "version": "Versión 0.4"},
                "ui": {"configuration": "Configuración", "window_title": "Título de ventana (parcial):", "typing_speed": "Velocidad (seg/char):", "commands": "Comandos", "control": "Control", "activity_log": "Registro de Actividad", "language": "Idioma:", "auto_save": "Guardar automáticamente:", "about": "Acerca de"},
                "buttons": {"add_command": "Agregar Comando", "edit_command": "Editar Comando", "delete_command": "Eliminar Comando", "load_defaults": "Cargar Defaults", "start": "Iniciar (¡)", "stop": "Detener (¡)", "save": "Guardar", "cancel": "Cancelar", "close": "Cerrar"},
                "defaults": {"window_title": "Bloc de notas", "test_message": "Hola, este es un mensaje de prueba.", "reminder_message": "Recordatorio: revisar el correo electrónico.", "note_message": "Nota importante para más tarde."},
                "messages": {"status_stopped": "Detenido - Presiona '¡' para iniciar", "status_running": "Ejecutándose - Presiona '¡' para detener"},
                "log": {"language_changed": "Idioma cambiado a Español"}
            }
    
    def set_language(self, language_code):
        """Set the current language"""
        if language_code in self.available_languages:
            self.current_language = language_code
            return True
        return False
    
    def get_language(self):
        """Get current language code"""
        return self.current_language
    
    def get_available_languages(self):
        """Get dictionary of available languages"""
        return self.available_languages
    
    def t(self, key_path, *args):
        """
        Translate a key path to current language
        
        Args:
            key_path (str): Dot-separated path to the translation key (e.g., 'ui.window_title')
            *args: Arguments for string formatting
            
        Returns:
            str: Translated string or key_path if not found
        """
        try:
            # Get the current language data
            lang_data = self.languages.get(self.current_language, {})
            
            # Navigate through the nested dictionary
            keys = key_path.split('.')
            value = lang_data
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    # Fallback to English if key not found in current language
                    if self.current_language != 'en':
                        return self._get_english_fallback(key_path, *args)
                    return key_path  # Return key path if not found
            
            # Format string with arguments if provided
            if args and isinstance(value, str):
                try:
                    return value.format(*args)
                except (IndexError, ValueError):
                    # If formatting fails, return unformatted string
                    return value
            
            return value if isinstance(value, str) else key_path
            
        except Exception as e:
            print(f"Translation error for key '{key_path}': {e}")
            return key_path
    
    def _get_english_fallback(self, key_path, *args):
        """Get English translation as fallback"""
        try:
            eng_data = self.languages.get('en', {})
            keys = key_path.split('.')
            value = eng_data
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return key_path
            
            if args and isinstance(value, str):
                try:
                    return value.format(*args)
                except (IndexError, ValueError):
                    return value
                    
            return value if isinstance(value, str) else key_path
            
        except Exception:
            return key_path
    
    def get_language_name(self, language_code=None):
        """Get the display name of a language"""
        code = language_code or self.current_language
        return self.available_languages.get(code, code)

# Global instance
_i18n = I18n()

def t(key_path, *args):
    """Global translation function"""
    return _i18n.t(key_path, *args)

def set_language(language_code):
    """Global function to set language"""
    return _i18n.set_language(language_code)

def get_language():
    """Global function to get current language"""
    return _i18n.get_language()

def get_available_languages():
    """Global function to get available languages"""
    return _i18n.get_available_languages()

def get_i18n():
    """Get the global i18n instance"""
    return _i18n