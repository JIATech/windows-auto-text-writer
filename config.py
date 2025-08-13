import json
import os
from pathlib import Path

class Config:
    """Configuration manager for application settings"""
    
    def __init__(self):
        self.config_file = Path.home() / '.windows_auto_text_writer' / 'config.json'
        self.config_data = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading config: {e}")
        
        # Return default configuration
        return {
            'language': 'en',  # Default to English
            'theme': 'light',
            'window_size': '1050x900',
            'typing_speed': 0.2
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            # Create directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config_data.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config_data[key] = value
    
    def get_language(self):
        """Get current language setting"""
        return self.get('language', 'en')
    
    def set_language(self, language):
        """Set language and save"""
        self.set('language', language)
        self.save_config()
    
    def get_theme(self):
        """Get current theme setting"""
        return self.get('theme', 'light')
    
    def set_theme(self, theme):
        """Set theme and save"""
        self.set('theme', theme)
        self.save_config()

# Global configuration instance
_config = Config()

def get_config():
    """Get global configuration instance"""
    return _config