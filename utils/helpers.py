from PyQt6.QtWidgets import QMessageBox

def show_error(message, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText("Error")
    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.exec()

def format_quantity(quantity, unit):
    return f"{quantity} {unit}"

def validate_number_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False