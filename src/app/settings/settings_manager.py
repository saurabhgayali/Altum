"""
Settings management module.
Handles persistent configuration for paths, model storage, temporary files, etc.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import platformdirs

logger = logging.getLogger(__name__)


class SettingsManager:
    """Manages application settings with persistent storage."""
    
    # Default settings
    DEFAULTS = {
        "temp_dir": None,  # Will be set to platform default
        "model_storage_dir": None,  # Will be set to platform default
        "processing_resolution": 768,
        "depth_model": "marigold-v2",
        "inpainting_model": "sd1.5",
        "max_processing_threads": 4,
        "gpu_enabled": True,
    }
    
    def __init__(self, app_name: str = "Altum"):
        """Initialize settings manager."""
        self.app_name = app_name
        self.config_dir = Path(platformdirs.user_config_dir(app_name))
        self.config_file = self.config_dir / "settings.json"
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize default directories if not set
        self.DEFAULTS["temp_dir"] = str(
            Path(platformdirs.user_cache_dir(app_name)) / "temp"
        )
        self.DEFAULTS["model_storage_dir"] = str(
            Path(platformdirs.user_cache_dir(app_name)) / "models"
        )
        
        # Load settings
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or use defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new settings
                    settings = self.DEFAULTS.copy()
                    settings.update(loaded)
                    logger.info(f"Loaded settings from {self.config_file}")
                    return settings
            except Exception as e:
                logger.error(f"Error loading settings: {e}, using defaults")
        
        return self.DEFAULTS.copy()
    
    def save(self) -> bool:
        """Save settings to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            logger.info(f"Saved settings to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self.settings[key] = value
    
    def get_temp_dir(self) -> Path:
        """Get temporary directory, creating it if needed."""
        temp_dir = Path(self.get("temp_dir"))
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir
    
    def get_model_storage_dir(self) -> Path:
        """Get model storage directory, creating it if needed."""
        model_dir = Path(self.get("model_storage_dir"))
        model_dir.mkdir(parents=True, exist_ok=True)
        return model_dir
    
    def get_depth_model_dir(self) -> Path:
        """Get depth models directory."""
        depth_dir = self.get_model_storage_dir() / "depth"
        depth_dir.mkdir(parents=True, exist_ok=True)
        return depth_dir
    
    def get_inpainting_model_dir(self) -> Path:
        """Get inpainting models directory."""
        inpaint_dir = self.get_model_storage_dir() / "inpainting"
        inpaint_dir.mkdir(parents=True, exist_ok=True)
        return inpaint_dir
    
    def validate_temp_dir(self) -> Tuple[bool, str]:
        """Validate temporary directory write access."""
        temp_dir = self.get_temp_dir()
        try:
            test_file = temp_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            return True, "Write access OK"
        except Exception as e:
            return False, str(e)
    
    def validate_model_storage_dir(self) -> Tuple[bool, str]:
        """Validate model storage directory write access."""
        model_dir = self.get_model_storage_dir()
        try:
            test_file = model_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            return True, "Write access OK"
        except Exception as e:
            return False, str(e)
    
    def clear_temp_files(self) -> Tuple[int, str]:
        """Clear all temporary files. Returns (count, error_message)."""
        temp_dir = self.get_temp_dir()
        count = 0
        errors = []
        
        try:
            for item in temp_dir.rglob('*'):
                if item.is_file():
                    try:
                        item.unlink()
                        count += 1
                    except Exception as e:
                        errors.append(str(e))
                elif item.is_dir() and item != temp_dir:
                    try:
                        import shutil
                        shutil.rmtree(item)
                        count += 1
                    except Exception as e:
                        errors.append(str(e))
        except Exception as e:
            return 0, str(e)
        
        error_msg = "; ".join(errors) if errors else ""
        return count, error_msg
    
    def set_temp_dir(self, path: str) -> Tuple[bool, str]:
        """Set temporary directory with validation."""
        try:
            path_obj = Path(path)
            path_obj.mkdir(parents=True, exist_ok=True)
            
            # Test write access
            test_file = path_obj / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            
            self.set("temp_dir", str(path_obj))
            self.save()
            return True, "Temporary directory set successfully"
        except Exception as e:
            return False, f"Error setting temporary directory: {e}"
    
    def set_model_storage_dir(self, path: str) -> Tuple[bool, str]:
        """Set model storage directory with validation."""
        try:
            path_obj = Path(path)
            path_obj.mkdir(parents=True, exist_ok=True)
            
            # Test write access
            test_file = path_obj / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            
            self.set("model_storage_dir", str(path_obj))
            self.save()
            return True, "Model storage directory set successfully"
        except Exception as e:
            return False, f"Error setting model storage directory: {e}"


# Create default singleton instance
settings_manager = SettingsManager()
