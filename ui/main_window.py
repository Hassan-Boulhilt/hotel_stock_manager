from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMenuBar, QMenu, 
    QStatusBar, QToolBar, QMessageBox, QApplication
)
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import Qt, QCoreApplication, QTranslator, QLibraryInfo
from database.db_manager import DatabaseManager
from models.stock_item import StockItem
from ui.stock_form import StockFormDialog
from ui.settings_dialog import SettingsDialog
from utils.helpers import show_error, format_quantity
from utils.settings_manager import SettingsManager

class MainWindow(QMainWindow):
    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        self.settings_manager = settings_manager
        self.db_manager = DatabaseManager()
        self.translators = []
        
        self.setup_ui()
        self.load_stock_data()
    
    def setup_ui(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Hotel Stock Manager"))
        self.resize(1000, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Apply language
        self.apply_language()
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Setup toolbar
        self.setup_toolbar()
        
        # Setup status bar
        self.setup_status_bar()
        
        # Setup tabs
        self.setup_tabs()
        
        # Add tabs to main layout
        main_layout.addWidget(self.tab_widget)
    
    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu(QCoreApplication.translate("MainWindow", "&File"))
        exit_action = QAction(QCoreApplication.translate("MainWindow", "Exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Stock menu
        stock_menu = menu_bar.addMenu(QCoreApplication.translate("MainWindow", "&Stock"))
        new_action = QAction(QIcon("resources/icons/add.png"), QCoreApplication.translate("MainWindow", "New Item"), self)
        new_action.triggered.connect(self.add_stock_item)
        stock_menu.addAction(new_action)
        
        # Settings menu
        settings_menu = menu_bar.addMenu(QCoreApplication.translate("MainWindow", "&Settings"))
        settings_action = QAction(QCoreApplication.translate("MainWindow", "Settings"), self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        
        # Language menu
        lang_menu = menu_bar.addMenu(QCoreApplication.translate("MainWindow", "&Language"))
        self.lang_group = QActionGroup(self)
        
        self.en_action = QAction("English", self)
        self.en_action.setCheckable(True)
        self.en_action.triggered.connect(lambda: self.change_language("en"))
        
        self.ar_action = QAction("العربية", self)
        self.ar_action.setCheckable(True)
        self.ar_action.triggered.connect(lambda: self.change_language("ar"))
        
        self.fr_action = QAction("Français", self)
        self.fr_action.setCheckable(True)
        self.fr_action.triggered.connect(lambda: self.change_language("fr"))
        
        lang_menu.addAction(self.en_action)
        lang_menu.addAction(self.ar_action)
        lang_menu.addAction(self.fr_action)
        
        # Set current language
        lang = self.settings_manager.get_language()
        if lang == "ar":
            self.ar_action.setChecked(True)
        elif lang == "fr":
            self.fr_action.setChecked(True)
        else:
            self.en_action.setChecked(True)
        
        # Help menu
        help_menu = menu_bar.addMenu(QCoreApplication.translate("MainWindow", "&Help"))
        about_action = QAction(QCoreApplication.translate("MainWindow", "About"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        toolbar = self.addToolBar("Tools")
        toolbar.setMovable(False)
        
        # Theme toggle
        self.theme_button = QPushButton()
        self.update_theme_button()
        self.theme_button.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_button)
    
    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(QCoreApplication.translate("MainWindow", "Ready"))
    
    def setup_tabs(self):
        self.tab_widget = QTabWidget()
        
        # Create stock management tab
        self.setup_stock_tab()
        
        # Create dashboard tab
        self.setup_dashboard_tab()
    
    def setup_stock_tab(self):
        stock_tab = QWidget()
        layout = QVBoxLayout(stock_tab)
        
        # Table for stock items
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(6)
        self.stock_table.setHorizontalHeaderLabels([
            QCoreApplication.translate("MainWindow", "ID"),
            QCoreApplication.translate("MainWindow", "Name"),
            QCoreApplication.translate("MainWindow", "Category"),
            QCoreApplication.translate("MainWindow", "Quantity"),
            QCoreApplication.translate("MainWindow", "Min Stock"),
            QCoreApplication.translate("MainWindow", "Last Updated")
        ])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stock_table.doubleClicked.connect(self.edit_stock_item)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton(QCoreApplication.translate("MainWindow", "Add Item"))
        self.add_button.clicked.connect(self.add_stock_item)
        
        self.edit_button = QPushButton(QCoreApplication.translate("MainWindow", "Edit Item"))
        self.edit_button.clicked.connect(self.edit_stock_item)
        
        self.delete_button = QPushButton(QCoreApplication.translate("MainWindow", "Delete Item"))
        self.delete_button.clicked.connect(self.delete_stock_item)
        
        self.refresh_button = QPushButton(QCoreApplication.translate("MainWindow", "Refresh"))
        self.refresh_button.clicked.connect(self.load_stock_data)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        
        layout.addWidget(self.stock_table)
        layout.addLayout(button_layout)
        
        self.tab_widget.addTab(stock_tab, QCoreApplication.translate("MainWindow", "Stock Management"))
    
    def setup_dashboard_tab(self):
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)
        
        # Low stock warning section
        low_stock_label = QLabel(QCoreApplication.translate("MainWindow", "Low Stock Items"))
        low_stock_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.low_stock_list = QLabel()
        self.low_stock_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(low_stock_label)
        layout.addWidget(self.low_stock_list)
        
        self.tab_widget.addTab(dashboard_tab, QCoreApplication.translate("MainWindow", "Dashboard"))
    
    # Core functionality methods
    def add_stock_item(self):
        dialog = StockFormDialog(self)
        if dialog.exec():
            self.db_manager.add_stock_item(dialog.get_stock_item())
            self.load_stock_data()
    
    def edit_stock_item(self):
        selected_row = self.stock_table.currentRow()
        if selected_row < 0:
            show_error(QCoreApplication.translate("MainWindow", "Please select an item to edit"), self)
            return
        
        item_id = int(self.stock_table.item(selected_row, 0).text())
        item = self.db_manager.get_item_by_id(item_id)
        
        if item:
            dialog = StockFormDialog(self, item)
            if dialog.exec():
                updated_item = dialog.get_stock_item()
                updated_item.id = item.id
                self.db_manager.update_stock_item(updated_item)
                self.load_stock_data()
    
    def delete_stock_item(self):
        selected_row = self.stock_table.currentRow()
        if selected_row < 0:
            show_error(QCoreApplication.translate("MainWindow", "Please select an item to delete"), self)
            return
        
        item_id = int(self.stock_table.item(selected_row, 0).text())
        self.db_manager.delete_stock_item(item_id)
        self.load_stock_data()
    
    def load_stock_data(self):
        items = self.db_manager.get_all_items()
        self.stock_table.setRowCount(len(items))
        
        low_stock_items = []
        
        for row, item in enumerate(items):
            self.stock_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.stock_table.setItem(row, 1, QTableWidgetItem(item.name))
            self.stock_table.setItem(row, 2, QTableWidgetItem(item.category))
            self.stock_table.setItem(row, 3, QTableWidgetItem(format_quantity(item.quantity, item.unit)))
            self.stock_table.setItem(row, 4, QTableWidgetItem(format_quantity(item.min_stock, item.unit)))
            self.stock_table.setItem(row, 5, QTableWidgetItem(item.last_updated or ""))
            
            if item.is_low_stock():
                low_stock_items.append(
                    QCoreApplication.translate("MainWindow", "- {0}: {1}{2} (min: {3}{2})"
                    ).format(item.name, item.quantity, item.unit, item.min_stock)
                )
        
        # Update dashboard
        if low_stock_items:
            self.low_stock_list.setText("\n".join(low_stock_items))
        else:
            self.low_stock_list.setText(QCoreApplication.translate("MainWindow", "No low stock items"))
    
    # Settings and language methods
    def apply_language(self):
        # Remove existing translators
        app = QApplication.instance()
        for translator in self.translators:
            app.removeTranslator(translator)
        self.translators = []
        
        # Load new translations
        lang = self.settings_manager.get_language()
        if lang != "en":
            # System translations
            qt_translator = QTranslator()
            if qt_translator.load(f"qtbase_{lang}", 
                                 QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
                app.installTranslator(qt_translator)
                self.translators.append(qt_translator)
            
            # App translations
            app_translator = QTranslator()
            if app_translator.load(f":/translations/app_{lang}"):
                app.installTranslator(app_translator)
                self.translators.append(app_translator)
    
    def retranslate_ui(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Hotel Stock Manager"))
        self.status_bar.showMessage(QCoreApplication.translate("MainWindow", "Ready"))
        self.update_theme_button()
        
        # Update tab names
        self.tab_widget.setTabText(0, QCoreApplication.translate("MainWindow", "Stock Management"))
        self.tab_widget.setTabText(1, QCoreApplication.translate("MainWindow", "Dashboard"))
        
        # Update stock table headers
        self.stock_table.setHorizontalHeaderLabels([
            QCoreApplication.translate("MainWindow", "ID"),
            QCoreApplication.translate("MainWindow", "Name"),
            QCoreApplication.translate("MainWindow", "Category"),
            QCoreApplication.translate("MainWindow", "Quantity"),
            QCoreApplication.translate("MainWindow", "Min Stock"),
            QCoreApplication.translate("MainWindow", "Last Updated")
        ])
        
        # Update buttons
        self.add_button.setText(QCoreApplication.translate("MainWindow", "Add Item"))
        self.edit_button.setText(QCoreApplication.translate("MainWindow", "Edit Item"))
        self.delete_button.setText(QCoreApplication.translate("MainWindow", "Delete Item"))
        self.refresh_button.setText(QCoreApplication.translate("MainWindow", "Refresh"))
        
        # Update dashboard
        self.load_stock_data()
    
    def update_theme_button(self):
        theme = self.settings_manager.get_theme()
        if theme == "dark":
            self.theme_button.setText(QCoreApplication.translate("MainWindow", "Switch to Light Mode"))
            self.theme_button.setIcon(QIcon("resources/icons/sun.png"))
        else:
            self.theme_button.setText(QCoreApplication.translate("MainWindow", "Switch to Dark Mode"))
            self.theme_button.setIcon(QIcon("resources/icons/moon.png"))
    
    def toggle_theme(self):
        theme = self.settings_manager.get_theme()
        new_theme = "dark" if theme == "light" else "light"
        self.settings_manager.set_theme(new_theme)
        
        # Reapply stylesheet
        app = QApplication.instance()
        try:
            stylesheet_file = f'resources/styles_{new_theme}.qss'
            with open(stylesheet_file, 'r') as f:
                app.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Stylesheet for theme '{new_theme}' not found")
        
        self.update_theme_button()
    
    def change_language(self, language):
        self.settings_manager.set_language(language)
        self.apply_language()
        self.retranslate_ui()
    
    def open_settings(self):
        dialog = SettingsDialog(self.settings_manager, self)
        if dialog.exec():
            new_theme, new_lang = dialog.get_settings()
            
            # Update theme if changed
            if new_theme != self.settings_manager.get_theme():
                self.settings_manager.set_theme(new_theme)
                app = QApplication.instance()
                try:
                    stylesheet_file = f'resources/styles_{new_theme}.qss'
                    with open(stylesheet_file, 'r') as f:
                        app.setStyleSheet(f.read())
                except FileNotFoundError:
                    print(f"Stylesheet for theme '{new_theme}' not found")
                self.update_theme_button()
            
            # Update language if changed
            if new_lang != self.settings_manager.get_language():
                self.change_language(new_lang)
    
    def show_about(self):
        about_text = QCoreApplication.translate("MainWindow", """
        <h2>Hotel Stock Manager</h2>
        <p>Version 1.0</p>
        <p>Manage hotel inventory including food, linens, and supplies.</p>
        <p>Developed with PyQt6</p>
        """)
        QMessageBox.about(self, QCoreApplication.translate("MainWindow", "About"), about_text)
    
    def closeEvent(self, event):
        self.db_manager.close()
        super().closeEvent(event)