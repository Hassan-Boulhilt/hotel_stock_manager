import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLibraryInfo
from ui.main_window import MainWindow
from utils.settings_manager import SettingsManager

def main():
    app = QApplication(sys.argv)
    
    # Load settings
    settings = SettingsManager()
    
    # Setup translations
    translator = QTranslator()
    language = settings.get_language()
    
    # Load translations
    if language != "en":
        # First try system translations
        if translator.load(f"qtbase_{language}", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
            app.installTranslator(translator)
        
        # Then try our app translations
        app_translator = QTranslator()
        if app_translator.load(f":/translations/app_{language}.qm"):
            app.installTranslator(app_translator)
    
    # Apply theme
    theme = settings.get_theme()
    try:
        stylesheet_file = f'resources/styles_{theme}.qss'
        with open(stylesheet_file, 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Stylesheet for theme '{theme}' not found")
    
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()