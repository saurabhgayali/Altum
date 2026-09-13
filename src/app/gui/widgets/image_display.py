"""
Image display widget.
"""

from PyQt6.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ImageDisplayWidget(QScrollArea):
    """Widget for displaying images with zoom and pan support."""
    
    def __init__(self, max_display_size: int = 800):
        """Initialize image display widget."""
        super().__init__()
        
        self.max_display_size = max_display_size
        self.current_image_path = None
        self.original_pixmap = None
        self.zoom_level = 1.0
        
        # Create label for image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        
        self.setWidget(self.image_label)
        self.setStyleSheet("QScrollArea { background-color: #2b2b2b; }")
        
        self._set_placeholder()
    
    def _set_placeholder(self):
        """Set placeholder image."""
        placeholder = QPixmap(400, 300)
        placeholder.fill(Qt.GlobalColor.gray)
        
        self.image_label.setPixmap(placeholder)
        self.image_label.setText("No image loaded")
    
    def load_image(self, file_path: Path) -> bool:
        """Load and display an image."""
        try:
            file_path = Path(file_path)
            
            # Open image with PIL
            pil_image = Image.open(file_path)
            
            # Convert to RGB if needed
            if pil_image.mode != 'RGB':
                if pil_image.mode == 'RGBA':
                    # Create white background
                    bg = Image.new('RGB', pil_image.size, (255, 255, 255))
                    bg.paste(pil_image, mask=pil_image.split()[3] if len(pil_image.split()) > 3 else None)
                    pil_image = bg
                else:
                    pil_image = pil_image.convert('RGB')
            
            # Resize for display if needed
            display_image = pil_image.copy()
            display_image.thumbnail((self.max_display_size, self.max_display_size), Image.Resampling.LANCZOS)
            
            # Convert PIL image to QPixmap
            data = display_image.tobytes("raw", "RGB")
            qimage = QImage(data, display_image.width, display_image.height, QImage.Format.Format_RGB888)
            self.original_pixmap = QPixmap.fromImage(qimage)
            
            # Display
            self.image_label.setPixmap(self.original_pixmap)
            self.current_image_path = file_path
            self.zoom_level = 1.0
            
            logger.info(f"Loaded image: {file_path.name} ({display_image.width}x{display_image.height})")
            return True
            
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            self._set_placeholder()
            return False
    
    def clear(self):
        """Clear the display."""
        self._set_placeholder()
        self.current_image_path = None
        self.original_pixmap = None
    
    def zoom_in(self):
        """Zoom in."""
        self.zoom_level *= 1.2
        self._update_display()
    
    def zoom_out(self):
        """Zoom out."""
        self.zoom_level /= 1.2
        self._update_display()
    
    def fit_to_window(self):
        """Fit image to window."""
        self.zoom_level = 1.0
        self._update_display()
    
    def _update_display(self):
        """Update display with current zoom level."""
        if self.original_pixmap is None:
            return
        
        size = int(self.original_pixmap.width() * self.zoom_level)
        scaled = self.original_pixmap.scaledToWidth(size, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled)
