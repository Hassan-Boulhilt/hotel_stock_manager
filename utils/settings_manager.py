import json
import os
from PyQt6.QtCore import QStandardPaths

class SettingsManager:
    def __init__(self):
        self.settings = {
            "theme": "light",
            "language": "en"
        }
        self.config_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.settings_file = os.path.join(self.config_dir, "hotel_stock_settings.json")
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Use defaults

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_theme(self):
        return self.settings.get("theme", "light")

    def set_theme(self, theme):
        self.settings["theme"] = theme
        self.save_settings()

    def get_language(self):
        return self.settings.get("language", "en")

    def set_language(self, language):
        self.settings["language"] = language
        self.save_settings()