"""
Image input and management utilities.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

# Supported image formats
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}


class ImageInfo:
    """Information about an image."""
    
    def __init__(self, file_path: Path):
        """Load image information."""
        self.file_path = Path(file_path)
        self.file_name = self.file_path.name
        self.file_size_mb = self.file_path.stat().st_size / (1024 ** 2)
        self.format = self.file_path.suffix.lower()
        
        # Load image metadata
        try:
            img = Image.open(self.file_path)
            self.width = img.width
            self.height = img.height
            self.mode = img.mode
            self.image = None  # Don't keep image in memory
            logger.info(f"Loaded image info: {self.width}x{self.height} {self.mode}")
        except Exception as e:
            logger.error(f"Error loading image info: {e}")
            self.width = None
            self.height = None
            self.mode = None
            self.image = None
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        if self.width is None:
            return f"Error loading image: {self.file_name}"
        
        megapixels = (self.width * self.height) / (1024 * 1024)
        
        summary = f"""Image Information
File: {self.file_name}
Size: {self.file_size_mb:.2f} MB
Format: {self.format}
Dimensions: {self.width}x{self.height} ({megapixels:.2f} MP)
Color Mode: {self.mode}"""
        
        return summary
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "file_path": str(self.file_path),
            "file_name": self.file_name,
            "file_size_mb": round(self.file_size_mb, 2),
            "format": self.format,
            "width": self.width,
            "height": self.height,
            "mode": self.mode,
        }
    
    def is_valid(self) -> Tuple[bool, str]:
        """Validate image."""
        if self.width is None or self.height is None:
            return False, "Could not load image"
        
        if self.width < 64 or self.height < 64:
            return False, f"Image too small: {self.width}x{self.height} (minimum 64x64)"
        
        if self.width > 8192 or self.height > 8192:
            return False, f"Image too large: {self.width}x{self.height} (maximum 8192x8192)"
        
        if self.mode not in ['RGB', 'RGBA', 'L', 'LA']:
            return False, f"Unsupported color mode: {self.mode}"
        
        return True, "Valid image"
    
    def load_as_array(self) -> Optional[np.ndarray]:
        """Load image as numpy array (RGB)."""
        try:
            img = Image.open(self.file_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                if img.mode == 'RGBA':
                    # Keep alpha but process as RGBA
                    pass
                elif img.mode == 'L':
                    img = img.convert('RGB')
                else:
                    img = img.convert('RGB')
            
            return np.array(img)
        except Exception as e:
            logger.error(f"Error loading image array: {e}")
            return None


def is_supported_image(file_path: Path) -> bool:
    """Check if file is a supported image format."""
    return file_path.suffix.lower() in SUPPORTED_FORMATS


def get_supported_formats_filter() -> str:
    """Get Qt file dialog filter string."""
    formats = " ".join([f"*{fmt}" for fmt in sorted(SUPPORTED_FORMATS)])
    return f"Image Files ({formats});;All Files (*)"
