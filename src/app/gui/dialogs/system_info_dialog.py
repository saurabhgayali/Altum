"""
System Information dialog.
"""

import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


class SystemInformationDialog(QDialog):
    """Dialog displaying system information."""
    
    def __init__(self, hardware_info, parent=None):
        """Initialize system information dialog."""
        super().__init__(parent)
        self.hardware_info = hardware_info
        
        self.setWindowTitle("System Information")
        self.setGeometry(100, 100, 700, 600)
        self.setModal(True)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("System & Hardware Information")
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        title_label.setFont(font)
        layout.addWidget(title_label)
        
        # Information display
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setFont(QFont("Courier", 10))
        self.info_text.setText(self.hardware_info.get_summary())
        layout.addWidget(self.info_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(self._copy_to_clipboard)
        button_layout.addWidget(copy_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _copy_to_clipboard(self):
        """Copy information to clipboard."""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.info_text.toPlainText())
        logger.info("System information copied to clipboard")
