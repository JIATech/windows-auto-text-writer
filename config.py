import json
import os
from pathlib import Path
from datetime import datetime

class Config:
    """Enhanced configuration manager for complete application persistence"""
    
    def __init__(self):
        # Use AppData for better Windows integration
        appdata = Path(os.environ.get('APPDATA', Path.home()))
        self.config_dir = appdata / 'WindowsAutoTextWriter'
        self.config_file = self.config_dir / 'settings.json'
        
        # Ensure directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_data = self.load_config()
        self._has_changes = False
    
    def load_config(self):
        """Load configuration from file or create default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Migrate old config format if needed
                    return self._migrate_config(data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading config: {e}")
        
        # Return default configuration with full structure
        return {
            'app_version': '0.4',
            'last_saved': datetime.now().isoformat(),
            'user_preferences': {
                'language': 'en',  # Default to English
                'theme': 'light',
                'window_size': '1050x900',
                'window_position': None,
                'auto_save': True,
                'confirm_on_exit': True
            },
            'application_config': {
                'window_title': '',  # Empty means use default
                'typing_speed': 0.2,
                'last_window_title': '',
                'last_typing_speed': 0.2
            },
            'text_commands': []  # Empty list for user commands
        }
    
    def _migrate_config(self, data):
        """Migrate old config format to new structure"""
        if 'app_version' in data:
            return data  # Already new format
            
        # Migrate old format
        migrated = {
            'app_version': '0.4',
            'last_saved': datetime.now().isoformat(),
            'user_preferences': {
                'language': data.get('language', 'en'),
                'theme': data.get('theme', 'light'),
                'window_size': data.get('window_size', '1050x900'),
                'window_position': None,
                'auto_save': True,
                'confirm_on_exit': True
            },
            'application_config': {
                'window_title': '',
                'typing_speed': data.get('typing_speed', 0.2),
                'last_window_title': '',
                'last_typing_speed': 0.2
            },
            'text_commands': []
        }
        
        print("Configuration migrated to new format")
        return migrated
    
    def save_config(self, force=False):
        """Save configuration to file"""
        try:
            # Update timestamp
            self.config_data['last_saved'] = datetime.now().isoformat()
            
            # Create directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            self._has_changes = False
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def mark_changed(self):
        """Mark configuration as changed"""
        self._has_changes = True
    
    def has_changes(self):
        """Check if configuration has unsaved changes"""
        return self._has_changes
    
    def get(self, section, key, default=None):
        """Get configuration value from section"""
        return self.config_data.get(section, {}).get(key, default)
    
    def set(self, section, key, value, auto_save=False):
        """Set configuration value in section"""
        if section not in self.config_data:
            self.config_data[section] = {}
        
        self.config_data[section][key] = value
        
        if auto_save:
            self.save_config()
        else:
            self.mark_changed()
    
    def get_language(self):
        """Get current language setting"""
        return self.get('user_preferences', 'language', 'en')
    
    def set_language(self, language, auto_save=True):
        """Set language and optionally save"""
        self.set('user_preferences', 'language', language, auto_save)
    
    def get_theme(self):
        """Get current theme setting"""
        return self.get('user_preferences', 'theme', 'light')
    
    def set_theme(self, theme, auto_save=True):
        """Set theme and optionally save"""
        self.set('user_preferences', 'theme', theme, auto_save)
    
    def get_window_title(self):
        """Get saved window title"""
        return self.get('application_config', 'window_title', '')
    
    def set_window_title(self, title, auto_save=False):
        """Set window title"""
        self.set('application_config', 'window_title', title, auto_save)
    
    def get_typing_speed(self):
        """Get saved typing speed"""
        return self.get('application_config', 'typing_speed', 0.2)
    
    def set_typing_speed(self, speed, auto_save=False):
        """Set typing speed"""
        self.set('application_config', 'typing_speed', speed, auto_save)
    
    def get_text_commands(self):
        """Get saved text commands"""
        return self.config_data.get('text_commands', [])
    
    def set_text_commands(self, commands, auto_save=False):
        """Set text commands"""
        # Add timestamps to new commands
        for cmd in commands:
            if 'created_date' not in cmd:
                cmd['created_date'] = datetime.now().isoformat()
        
        self.config_data['text_commands'] = commands
        
        if auto_save:
            self.save_config()
        else:
            self.mark_changed()
    
    def get_auto_save(self):
        """Get auto-save preference"""
        return self.get('user_preferences', 'auto_save', True)
    
    def set_auto_save(self, auto_save):
        """Set auto-save preference"""
        self.set('user_preferences', 'auto_save', auto_save, True)
    
    def get_confirm_on_exit(self):
        """Get confirm-on-exit preference"""
        return self.get('user_preferences', 'confirm_on_exit', True)
    
    def set_confirm_on_exit(self, confirm):
        """Set confirm-on-exit preference"""
        self.set('user_preferences', 'confirm_on_exit', confirm, True)

# Global configuration instance
_config = Config()

def get_config():
    """Get global configuration instance"""
    return _config