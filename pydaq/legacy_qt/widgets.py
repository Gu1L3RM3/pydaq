from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal, Qt


class ClickableLineEdit(QLineEdit):
    """
    Custom QLineEdit that emits a signal when clicked, 
    used to trigger ComboBox menus in PYDAQ.
    """
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
