"""
Main application window.
"""

import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QStatusBar, QMenuBar, QMenu, QFileDialog,
    QMessageBox, QSplitter, QTextEdit, QDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction

from src.app.settings.settings_manager import settings_manager
from src.hardware.gpu_detection import hardware_info
from src.models.model_manager import ModelManager
from src.app.image_utils import ImageInfo, is_supported_image, get_supported_formats_filter
from src.app.gui.widgets.image_display import ImageDisplayWidget
from src.app.gui.dialogs.settings_dialog import SettingsDialog
from src.app.gui.dialogs.system_info_dialog import SystemInformationDialog
from src.app.gui.dialogs.model_manager_dialog import ModelManagementDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize managers
        self.settings = settings_manager
        self.model_manager = ModelManager(self.settings.get_model_storage_dir())
        
        # Window setup
        self.setWindowTitle("Altum - Single-Image 3D Photo Generator")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create UI
        self._create_menu_bar()
        self._create_central_widget()
        self._create_status_bar()
        
        logger.info("Main window initialized")
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Photo", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_photo)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        settings_action = QAction("&Settings", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._open_settings)
        edit_menu.addAction(settings_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        system_info_action = QAction("&System Information", self)
        system_info_action.triggered.connect(self._show_system_info)
        view_menu.addAction(system_info_action)
        
        # Models menu
        models_menu = menubar.addMenu("&Models")
        
        manage_models_action = QAction("&Manage Models", self)
        manage_models_action.triggered.connect(self._manage_models)
        models_menu.addAction(manage_models_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_central_widget(self):
        """Create the central widget with tabs."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Image tab
        self.image_tab = self._create_image_tab()
        self.tab_widget.addTab(self.image_tab, "Image & Input")
        
        # Processing tab
        self.processing_tab = self._create_processing_tab()
        self.tab_widget.addTab(self.processing_tab, "Processing")
        
        # Preview tab
        self.preview_tab = self._create_preview_tab()
        self.tab_widget.addTab(self.preview_tab, "Preview")
        
        # Export tab
        self.export_tab = self._create_export_tab()
        self.tab_widget.addTab(self.export_tab, "Export")
        
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
    
    def _create_image_tab(self) -> QWidget:
        """Create the image input tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("Open Photo")
        open_btn.clicked.connect(self._open_photo)
        button_layout.addWidget(open_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_image)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Image display
        self.image_display = ImageDisplayWidget()
        layout.addWidget(self.image_display, stretch=1)
        
        # Image info
        self.image_info_label = QLabel("Image Information: None")
        self.image_info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(self.image_info_label)
        
        # Store current image info
        self.current_image_info = None
        
        widget.setLayout(layout)
        return widget
    
    def _create_processing_tab(self) -> QWidget:
        """Create the processing tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Processing buttons
        button_layout = QHBoxLayout()
        
        depth_btn = QPushButton("Generate Depth")
        depth_btn.clicked.connect(self._generate_depth)
        button_layout.addWidget(depth_btn)
        
        background_btn = QPushButton("Generate Background")
        background_btn.clicked.connect(self._generate_background)
        button_layout.addWidget(background_btn)
        
        preview_btn = QPushButton("Generate Preview")
        preview_btn.clicked.connect(self._generate_preview)
        button_layout.addWidget(preview_btn)
        
        layout.addLayout(button_layout)
        
        # Processing status
        self.processing_status_label = QLabel("Status: Idle")
        layout.addWidget(self.processing_status_label)
        
        # Processing log
        self.processing_log = QTextEdit()
        self.processing_log.setReadOnly(True)
        layout.addWidget(self.processing_log)
        
        widget.setLayout(layout)
        return widget
    
    def _create_preview_tab(self) -> QWidget:
        """Create the preview tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        preview_label = QLabel("Preview will be displayed here after processing")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(preview_label)
        
        widget.setLayout(layout)
        return widget
    
    def _create_export_tab(self) -> QWidget:
        """Create the export tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        html_btn = QPushButton("Export as HTML")
        html_btn.clicked.connect(self._export_html)
        button_layout.addWidget(html_btn)
        
        zip_btn = QPushButton("Export as ZIP")
        zip_btn.clicked.connect(self._export_zip)
        button_layout.addWidget(zip_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_status_bar(self):
        """Create the status bar."""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        
        self.status_label = QLabel("Ready")
        statusbar.addWidget(self.status_label)
        
        self.gpu_label = QLabel(f"GPU: {hardware_info.get_compute_device().upper()}")
        statusbar.addPermanentWidget(self.gpu_label)
    
    # Menu actions
    def _open_photo(self):
        """Open a photo file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Photo",
            "",
            get_supported_formats_filter()
        )
        
        if not file_path:
            return
        
        try:
            file_path = Path(file_path)
            
            # Load image info
            image_info = ImageInfo(file_path)
            
            # Validate image
            is_valid, message = image_info.is_valid()
            if not is_valid:
                QMessageBox.warning(self, "Invalid Image", message)
                logger.warning(f"Invalid image: {message}")
                return
            
            # Display image
            if not self.image_display.load_image(file_path):
                QMessageBox.warning(self, "Error", "Could not load image")
                return
            
            # Store image info
            self.current_image_info = image_info
            
            # Update UI
            self.image_info_label.setText(image_info.get_summary())
            self.status_label.setText(f"Loaded: {file_path.name}")
            self.tab_widget.setTabText(0, f"Image & Input - {file_path.name}")
            
            logger.info(f"Successfully opened image: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error opening image: {e}")
            QMessageBox.critical(self, "Error", f"Failed to open image: {e}")
    
    def _clear_image(self):
        """Clear the current image."""
        self.image_display.clear()
        self.current_image_info = None
        self.image_info_label.setText("Image Information: None")
        self.status_label.setText("Ready")
        self.tab_widget.setTabText(0, "Image & Input")
        logger.info("Cleared current image")
    
    def _open_settings(self):
        """Open settings dialog."""
        logger.info("Opening settings dialog")
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            logger.info("Settings updated")
            self.status_label.setText("Settings updated")
    
    def _show_system_info(self):
        """Show system information."""
        dialog = SystemInformationDialog(hardware_info, self)
        dialog.exec()
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """
<b>Altum</b> v0.1.0<br><br>
Single-Image 3D Photo Generator<br><br>
A standalone, offline-first Python desktop GUI that converts 
a single 2D photograph into an interactive 2.5D/3D parallax photo.
        """
        QMessageBox.about(self, "About Altum", about_text)
    
    def _manage_models(self):
        """Open model management dialog."""
        logger.info("Opening model management dialog")
        dialog = ModelManagementDialog(self.model_manager, self)
        dialog.exec()
    
    # Processing actions
    def _generate_depth(self):
        """Generate depth map."""
        logger.info("Generate depth action triggered")
        self.processing_status_label.setText("Status: Generating depth...")
        self.processing_log.append("Starting depth generation...\n")
    
    def _generate_background(self):
        """Generate background."""
        logger.info("Generate background action triggered")
        self.processing_status_label.setText("Status: Generating background...")
        self.processing_log.append("Starting background generation...\n")
    
    def _generate_preview(self):
        """Generate preview."""
        logger.info("Generate preview action triggered")
        self.processing_status_label.setText("Status: Generating preview...")
        self.processing_log.append("Starting preview generation...\n")
    
    # Export actions
    def _export_html(self):
        """Export as HTML."""
        logger.info("Export HTML action triggered")
        QMessageBox.information(self, "Export", "HTML export - to be implemented")
    
    def _export_zip(self):
        """Export as ZIP."""
        logger.info("Export ZIP action triggered")
        QMessageBox.information(self, "Export", "ZIP export - to be implemented")
