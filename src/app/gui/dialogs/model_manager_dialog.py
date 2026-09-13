"""
Model management dialog.
"""

import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QPushButton, QLabel, QMessageBox, QGroupBox, QFormLayout,
    QProgressBar, QScrollArea
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class ModelManagementDialog(QDialog):
    """Dialog for managing AI models."""
    
    def __init__(self, model_manager, parent=None):
        """Initialize model management dialog."""
        super().__init__(parent)
        self.model_manager = model_manager
        
        self.setWindowTitle("Model Management")
        self.setGeometry(100, 100, 700, 600)
        self.setModal(True)
        
        self._create_ui()
        self._refresh_display()
    
    def _create_ui(self):
        """Create the UI."""
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Depth models tab
        depth_tab = self._create_depth_models_tab()
        self.tab_widget.addTab(depth_tab, "Depth Models")
        
        # Inpainting models tab
        inpaint_tab = self._create_inpainting_models_tab()
        self.tab_widget.addTab(inpaint_tab, "Inpainting Models")
        
        # Storage info tab
        storage_tab = self._create_storage_info_tab()
        self.tab_widget.addTab(storage_tab, "Storage & Info")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_display)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_depth_models_tab(self) -> QWidget:
        """Create depth models tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Scroll area for models
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        self.depth_model_groups = {}
        
        for model_id, model_info in self.model_manager.DEPTH_MODELS.items():
            group = self._create_model_group(model_id, model_info, "depth")
            self.depth_model_groups[model_id] = group
            scroll_layout.addWidget(group)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def _create_inpainting_models_tab(self) -> QWidget:
        """Create inpainting models tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Scroll area for models
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        self.inpaint_model_groups = {}
        
        for model_id, model_info in self.model_manager.INPAINTING_MODELS.items():
            group = self._create_model_group(model_id, model_info, "inpainting")
            self.inpaint_model_groups[model_id] = group
            scroll_layout.addWidget(group)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def _create_storage_info_tab(self) -> QWidget:
        """Create storage info tab."""
        widget = QWidget()
        layout = QFormLayout()
        
        # Model directory
        self.model_dir_label = QLabel()
        layout.addRow("Model Directory:", self.model_dir_label)
        
        # Depth models directory
        self.depth_dir_label = QLabel()
        layout.addRow("Depth Models:", self.depth_dir_label)
        
        # Inpainting models directory
        self.inpaint_dir_label = QLabel()
        layout.addRow("Inpainting Models:", self.inpaint_dir_label)
        
        # Status summary
        layout.addRow("", QLabel(""))  # Spacer
        
        self.status_label = QLabel()
        layout.addRow("Status:", self.status_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_model_group(self, model_id: str, model_info, model_type: str) -> QGroupBox:
        """Create a model group widget."""
        group = QGroupBox(model_info.name)
        layout = QFormLayout()
        
        # Description
        layout.addRow("Description:", QLabel(model_info.description))
        
        # Size
        layout.addRow("Size:", QLabel(f"{model_info.size_gb} GB"))
        
        # Status
        is_installed = self.model_manager.is_installed(model_id)
        status_text = "Installed" if is_installed else "Not Installed"
        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"color: {'green' if is_installed else 'red'};")
        layout.addRow("Status:", status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        if is_installed:
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(
                lambda: self._delete_model(model_id, model_info.name)
            )
            button_layout.addWidget(delete_btn)
        else:
            download_btn = QPushButton("Download (Placeholder)")
            download_btn.setEnabled(False)
            download_btn.setToolTip("Model download will be implemented in a future update")
            button_layout.addWidget(download_btn)
        
        layout.addRow("", button_layout)
        
        return group
    
    def _delete_model(self, model_id: str, model_name: str):
        """Delete a model."""
        reply = QMessageBox.question(
            self,
            "Delete Model",
            f"Are you sure you want to delete '{model_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.model_manager.delete_model(model_id):
                QMessageBox.information(
                    self,
                    "Success",
                    f"Successfully deleted '{model_name}'"
                )
                self._refresh_display()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to delete '{model_name}'"
                )
    
    def _refresh_display(self):
        """Refresh the model display."""
        # Update storage info
        self.model_dir_label.setText(str(self.model_manager.model_dir))
        self.depth_dir_label.setText(str(self.model_manager.depth_dir))
        self.inpaint_dir_label.setText(str(self.model_manager.inpainting_dir))
        
        # Update status
        summary = self.model_manager.get_status_summary()
        status_text = f"{summary['installed_models']}/{summary['total_models']} models installed"
        self.status_label.setText(status_text)
        
        # Refresh model widgets if they exist
        if hasattr(self, 'depth_model_groups'):
            for model_id, group in self.depth_model_groups.items():
                self._update_model_group(group, model_id)
        
        if hasattr(self, 'inpaint_model_groups'):
            for model_id, group in self.inpaint_model_groups.items():
                self._update_model_group(group, model_id)
    
    def _update_model_group(self, group: QGroupBox, model_id: str):
        """Update a model group's status."""
        # This would be more complex with the current implementation
        # For now, we just log that refresh happened
        logger.info(f"Updated model group for {model_id}")
