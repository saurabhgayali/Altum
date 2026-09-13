"""
Main application entry point for Altum.
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    try:
        # Import here to catch import errors gracefully
        from PyQt6.QtWidgets import QApplication
        from src.app.gui.main_window import MainWindow
        from src.hardware.gpu_detection import hardware_info
        
        # Log hardware info
        logger.info("=== ALTUM APPLICATION START ===")
        logger.info(hardware_info.get_summary())
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName("Altum")
        app.setApplicationVersion("0.1.0")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application window created and shown")
        
        # Run event loop
        sys.exit(app.exec())
    
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Please run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
