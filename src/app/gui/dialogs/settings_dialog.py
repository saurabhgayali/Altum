"""
Settings dialog for the application.
"""

import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QPushButton, QLabel, QLineEdit, QSpinBox, QCheckBox,
    QFileDialog, QMessageBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """Settings dialog window."""
    
    def __init__(self, settings_manager, parent=None):
        """Initialize settings dialog."""
        super().__init__(parent)
        self.settings_manager = settings_manager
        
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 600, 500)
        self.setModal(True)
        
        self._create_ui()
        self._load_settings()
    
    def _create_ui(self):
        """Create the UI."""
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Paths tab
        paths_tab = self._create_paths_tab()
        self.tab_widget.addTab(paths_tab, "Paths")
        
        # Processing tab
        processing_tab = self._create_processing_tab()
        self.tab_widget.addTab(processing_tab, "Processing")
        
        # Models tab
        models_tab = self._create_models_tab()
        self.tab_widget.addTab(models_tab, "Models")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self._save_and_close)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._apply_settings)
        button_layout.addWidget(apply_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_paths_tab(self) -> QWidget:
        """Create the paths tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Temporary files path
        temp_group = QGroupBox("Temporary Files")
        temp_layout = QFormLayout()
        
        self.temp_path_input = QLineEdit()
        temp_browse_btn = QPushButton("Browse...")
        temp_browse_btn.clicked.connect(self._browse_temp_dir)
        
        temp_path_layout = QHBoxLayout()
        temp_path_layout.addWidget(self.temp_path_input)
        temp_path_layout.addWidget(temp_browse_btn)
        
        temp_layout.addRow("Path:", temp_path_layout)
        
        # Validate temp dir button
        temp_validate_btn = QPushButton("Validate")
        temp_validate_btn.clicked.connect(self._validate_temp_dir)
        temp_layout.addRow("", temp_validate_btn)
        
        temp_group.setLayout(temp_layout)
        layout.addWidget(temp_group)
        
        # Model storage path
        model_group = QGroupBox("Model Storage")
        model_layout = QFormLayout()
        
        self.model_path_input = QLineEdit()
        model_browse_btn = QPushButton("Browse...")
        model_browse_btn.clicked.connect(self._browse_model_dir)
        
        model_path_layout = QHBoxLayout()
        model_path_layout.addWidget(self.model_path_input)
        model_path_layout.addWidget(model_browse_btn)
        
        model_layout.addRow("Path:", model_path_layout)
        
        # Validate model dir button
        model_validate_btn = QPushButton("Validate")
        model_validate_btn.clicked.connect(self._validate_model_dir)
        model_layout.addRow("", model_validate_btn)
        
        # Clear temp files button
        clear_btn = QPushButton("Clear Temporary Files")
        clear_btn.clicked.connect(self._clear_temp_files)
        model_layout.addRow("", clear_btn)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_processing_tab(self) -> QWidget:
        """Create the processing tab."""
        widget = QWidget()
        layout = QFormLayout()
        
        # Processing resolution
        self.resolution_spinbox = QSpinBox()
        self.resolution_spinbox.setMinimum(256)
        self.resolution_spinbox.setMaximum(2048)
        self.resolution_spinbox.setSingleStep(128)
        layout.addRow("Processing Resolution (max):", self.resolution_spinbox)
        
        # Processing threads
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setMinimum(1)
        self.threads_spinbox.setMaximum(16)
        layout.addRow("Processing Threads:", self.threads_spinbox)
        
        # GPU enabled
        self.gpu_checkbox = QCheckBox("Use GPU if available")
        layout.addRow("Hardware:", self.gpu_checkbox)
        
        # Stretch
        widget.setLayout(layout)
        return widget
    
    def _create_models_tab(self) -> QWidget:
        """Create the models tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("Model selection and management will be available in a future update.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _load_settings(self):
        """Load settings into UI."""
        self.temp_path_input.setText(str(self.settings_manager.get_temp_dir()))
        self.model_path_input.setText(str(self.settings_manager.get_model_storage_dir()))
        self.resolution_spinbox.setValue(self.settings_manager.get("processing_resolution", 768))
        self.threads_spinbox.setValue(self.settings_manager.get("max_processing_threads", 4))
        self.gpu_checkbox.setChecked(self.settings_manager.get("gpu_enabled", True))
    
    def _save_and_close(self):
        """Save settings and close dialog."""
        self._apply_settings()
        self.accept()
    
    def _apply_settings(self):
        """Apply and save settings."""
        try:
            # Validate and set paths
            temp_valid, temp_msg = self.settings_manager.set_temp_dir(self.temp_path_input.text())
            if not temp_valid:
                QMessageBox.warning(self, "Temporary Path", f"Invalid: {temp_msg}")
                return
            
            model_valid, model_msg = self.settings_manager.set_model_storage_dir(self.model_path_input.text())
            if not model_valid:
                QMessageBox.warning(self, "Model Path", f"Invalid: {model_msg}")
                return
            
            # Save other settings
            self.settings_manager.set("processing_resolution", self.resolution_spinbox.value())
            self.settings_manager.set("max_processing_threads", self.threads_spinbox.value())
            self.settings_manager.set("gpu_enabled", self.gpu_checkbox.isChecked())
            
            # Persist
            if self.settings_manager.save():
                QMessageBox.information(self, "Settings", "Settings saved successfully")
                logger.info("Settings saved")
            else:
                QMessageBox.warning(self, "Settings", "Failed to save settings")
        
        except Exception as e:
            logger.error(f"Error applying settings: {e}")
            QMessageBox.critical(self, "Error", f"Error applying settings: {e}")
    
    def _browse_temp_dir(self):
        """Browse for temporary directory."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Temporary Directory")
        if dir_path:
            self.temp_path_input.setText(dir_path)
    
    def _browse_model_dir(self):
        """Browse for model directory."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Model Storage Directory")
        if dir_path:
            self.model_path_input.setText(dir_path)
    
    def _validate_temp_dir(self):
        """Validate temporary directory."""
        temp_path = self.temp_path_input.text()
        try:
            path = Path(temp_path)
            path.mkdir(parents=True, exist_ok=True)
            
            # Test write
            test_file = path / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            
            QMessageBox.information(self, "Validation", f"Temporary directory is valid:\n{temp_path}")
        except Exception as e:
            QMessageBox.warning(self, "Validation Error", f"Directory validation failed:\n{e}")
    
    def _validate_model_dir(self):
        """Validate model directory."""
        model_path = self.model_path_input.text()
        try:
            path = Path(model_path)
            path.mkdir(parents=True, exist_ok=True)
            
            # Test write
            test_file = path / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            
            QMessageBox.information(self, "Validation", f"Model directory is valid:\n{model_path}")
        except Exception as e:
            QMessageBox.warning(self, "Validation Error", f"Directory validation failed:\n{e}")
    
    def _clear_temp_files(self):
        """Clear temporary files."""
        reply = QMessageBox.question(
            self,
            "Clear Temporary Files",
            "Are you sure you want to clear all temporary files?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            count, error = self.settings_manager.clear_temp_files()
            if error:
                QMessageBox.warning(self, "Clear", f"Cleared {count} items with errors:\n{error}")
            else:
                QMessageBox.information(self, "Clear", f"Successfully cleared {count} temporary items")
