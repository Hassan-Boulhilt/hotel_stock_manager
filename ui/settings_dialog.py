from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGroupBox, QRadioButton, QButtonGroup,
    QDialogButtonBox, QComboBox, QLabel, QHBoxLayout
)

class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings_manager = settings_manager
        
        layout = QVBoxLayout()
        
        # Theme settings
        theme_group = QGroupBox("Theme")
        theme_layout = QHBoxLayout()
        self.theme_group = QButtonGroup(self)
        
        self.light_radio = QRadioButton("Light Mode")
        self.dark_radio = QRadioButton("Dark Mode")
        self.theme_group.addButton(self.light_radio, 1)
        self.theme_group.addButton(self.dark_radio, 2)
        
        theme_layout.addWidget(self.light_radio)
        theme_layout.addWidget(self.dark_radio)
        theme_group.setLayout(theme_layout)
        
        # Language settings
        lang_group = QGroupBox("Language")
        lang_layout = QVBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Arabic", "ar")
        self.lang_combo.addItem("French", "fr")
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(theme_group)
        layout.addWidget(lang_group)
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        # Load current settings
        self.load_settings()
    
    def load_settings(self):
        theme = self.settings_manager.get_theme()
        if theme == "light":
            self.light_radio.setChecked(True)
        else:
            self.dark_radio.setChecked(True)
        
        language = self.settings_manager.get_language()
        index = self.lang_combo.findData(language)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
    
    def get_settings(self):
        theme = "light" if self.light_radio.isChecked() else "dark"
        language = self.lang_combo.currentData()
        return theme, language