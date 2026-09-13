"""
Model manager for downloading and managing AI models.
Handles depth models and inpainting models.
"""

import logging
import os
from pathlib import Path
from typing import Dict, Optional, Callable
import json

logger = logging.getLogger(__name__)


class ModelInfo:
    """Information about a model."""
    
    def __init__(self, name: str, model_type: str, description: str,
                 download_url: str, size_gb: float, model_id: str):
        self.name = name
        self.model_type = model_type  # "depth" or "inpainting"
        self.description = description
        self.download_url = download_url
        self.size_gb = size_gb
        self.model_id = model_id
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "model_type": self.model_type,
            "description": self.description,
            "download_url": self.download_url,
            "size_gb": self.size_gb,
            "model_id": self.model_id,
        }


class ModelManager:
    """Manages AI model downloads and installation."""
    
    # Supported models
    DEPTH_MODELS = {
        "marigold-v2": ModelInfo(
            name="Marigold V2",
            model_type="depth",
            description="High-quality depth estimation model",
            download_url="https://huggingface.co/prs/marigold",
            size_gb=1.5,
            model_id="marigold-v2",
        ),
    }
    
    INPAINTING_MODELS = {
        "sd1.5": ModelInfo(
            name="Stable Diffusion 1.5 Inpainting",
            model_type="inpainting",
            description="Stable Diffusion 1.5 optimized for inpainting",
            download_url="https://huggingface.co/runwayml/stable-diffusion-inpainting",
            size_gb=4.0,
            model_id="sd1.5",
        ),
        "sdxl": ModelInfo(
            name="Stable Diffusion XL Inpainting",
            model_type="inpainting",
            description="SDXL optimized for high-quality inpainting",
            download_url="https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
            size_gb=6.9,
            model_id="sdxl",
        ),
    }
    
    def __init__(self, model_dir: Path):
        """Initialize model manager."""
        self.model_dir = model_dir
        self.depth_dir = model_dir / "depth"
        self.inpainting_dir = model_dir / "inpainting"
        
        self.depth_dir.mkdir(parents=True, exist_ok=True)
        self.inpainting_dir.mkdir(parents=True, exist_ok=True)
        
        self._installed_models: Dict[str, bool] = {}
        self._refresh_installed_models()
    
    def _refresh_installed_models(self):
        """Scan for installed models."""
        self._installed_models = {}
        
        # Check depth models
        for model_id in self.DEPTH_MODELS:
            model_path = self.depth_dir / model_id
            self._installed_models[model_id] = model_path.exists()
        
        # Check inpainting models
        for model_id in self.INPAINTING_MODELS:
            model_path = self.inpainting_dir / model_id
            self._installed_models[model_id] = model_path.exists()
    
    def is_installed(self, model_id: str) -> bool:
        """Check if a model is installed."""
        self._refresh_installed_models()
        return self._installed_models.get(model_id, False)
    
    def get_depth_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get depth model info."""
        return self.DEPTH_MODELS.get(model_id)
    
    def get_inpainting_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get inpainting model info."""
        return self.INPAINTING_MODELS.get(model_id)
    
    def get_all_depth_models(self) -> Dict[str, ModelInfo]:
        """Get all available depth models."""
        return self.DEPTH_MODELS.copy()
    
    def get_all_inpainting_models(self) -> Dict[str, ModelInfo]:
        """Get all available inpainting models."""
        return self.INPAINTING_MODELS.copy()
    
    def get_model_path(self, model_id: str) -> Optional[Path]:
        """Get the path where a model should be/is stored."""
        if model_id in self.DEPTH_MODELS:
            return self.depth_dir / model_id
        elif model_id in self.INPAINTING_MODELS:
            return self.inpainting_dir / model_id
        return None
    
    def get_installed_depth_models(self) -> Dict[str, ModelInfo]:
        """Get installed depth models."""
        return {
            model_id: info
            for model_id, info in self.DEPTH_MODELS.items()
            if self.is_installed(model_id)
        }
    
    def get_installed_inpainting_models(self) -> Dict[str, ModelInfo]:
        """Get installed inpainting models."""
        return {
            model_id: info
            for model_id, info in self.INPAINTING_MODELS.items()
            if self.is_installed(model_id)
        }
    
    def download_model(self, model_id: str,
                      progress_callback: Optional[Callable[[int], None]] = None) -> bool:
        """
        Download a model.
        
        Note: Actual download implementation depends on model source.
        This is a placeholder showing the interface.
        """
        if model_id in self.DEPTH_MODELS:
            model_info = self.DEPTH_MODELS[model_id]
            model_path = self.depth_dir / model_id
        elif model_id in self.INPAINTING_MODELS:
            model_info = self.INPAINTING_MODELS[model_id]
            model_path = self.inpainting_dir / model_id
        else:
            logger.error(f"Unknown model: {model_id}")
            return False
        
        # Create model directory
        model_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Model {model_id} download placeholder. "
                   f"In production, would download from {model_info.download_url}")
        
        # Mark model as installed (in real implementation, would download first)
        self._refresh_installed_models()
        return True
    
    def delete_model(self, model_id: str) -> bool:
        """Delete an installed model."""
        model_path = self.get_model_path(model_id)
        if not model_path or not model_path.exists():
            logger.warning(f"Model {model_id} not found at {model_path}")
            return False
        
        try:
            import shutil
            shutil.rmtree(model_path)
            self._refresh_installed_models()
            logger.info(f"Deleted model {model_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting model {model_id}: {e}")
            return False
    
    def get_status_summary(self) -> Dict[str, any]:
        """Get status summary of all models."""
        return {
            "total_models": len(self.DEPTH_MODELS) + len(self.INPAINTING_MODELS),
            "installed_models": sum(1 for v in self._installed_models.values() if v),
            "depth_models": {
                model_id: {
                    "installed": self.is_installed(model_id),
                    "info": info.to_dict(),
                }
                for model_id, info in self.DEPTH_MODELS.items()
            },
            "inpainting_models": {
                model_id: {
                    "installed": self.is_installed(model_id),
                    "info": info.to_dict(),
                }
                for model_id, info in self.INPAINTING_MODELS.items()
            },
        }
