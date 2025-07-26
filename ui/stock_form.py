from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, 
    QDoubleSpinBox, QDialogButtonBox, QLabel
)
from models.stock_item import StockItem
from utils.helpers import validate_number_input, show_error

class StockFormDialog(QDialog):
    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.setWindowTitle("Add Stock Item" if not item else "Edit Stock Item")
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Item name
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        
        # Category
        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Linen", "Cleaning Supplies", "Toiletries", "Other"])
        form_layout.addRow("Category:", self.category_input)
        
        # Quantity
        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(10000)
        self.quantity_input.setValue(1.0)
        form_layout.addRow("Quantity:", self.quantity_input)
        
        # Unit
        self.unit_input = QComboBox()
        self.unit_input.addItems(["kg", "g", "lb", "pieces", "liters", "ml", "bottles"])
        form_layout.addRow("Unit:", self.unit_input)
        
        # Min stock
        self.min_stock_input = QDoubleSpinBox()
        self.min_stock_input.setMinimum(0)
        self.min_stock_input.setMaximum(10000)
        self.min_stock_input.setValue(0.5)
        form_layout.addRow("Min Stock:", self.min_stock_input)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                     QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.validate)
        button_box.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        # Populate if editing
        if item:
            self.populate_form(item)
    
    def populate_form(self, item):
        self.name_input.setText(item.name)
        self.category_input.setCurrentText(item.category)
        self.quantity_input.setValue(item.quantity)
        self.unit_input.setCurrentText(item.unit)
        self.min_stock_input.setValue(item.min_stock)
    
    def validate(self):
        if not self.name_input.text().strip():
            show_error("Name is required", self)
            return
        
        if self.min_stock_input.value() < 0:
            show_error("Min stock cannot be negative", self)
            return
        
        self.accept()
    
    def get_stock_item(self):
        return StockItem(
            name=self.name_input.text().strip(),
            category=self.category_input.currentText(),
            quantity=self.quantity_input.value(),
            unit=self.unit_input.currentText(),
            min_stock=self.min_stock_input.value()
        )