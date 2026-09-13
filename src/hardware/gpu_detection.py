"""
Hardware detection and system information module.
Detects GPU, CUDA, VRAM, and other compute capabilities.
"""

import os
import platform
import psutil
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class HardwareInfo:
    """Provides system and GPU hardware information."""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.gpu_info = self._get_gpu_info()
        self.cuda_info = self._get_cuda_info()
        self.pytorch_info = self._get_pytorch_info()
    
    def _get_system_info(self) -> Dict:
        """Get basic system information."""
        try:
            virtual_memory = psutil.virtual_memory()
            return {
                "os": platform.system(),
                "platform": platform.platform(),
                "processor": platform.processor(),
                "cpu_count": os.cpu_count(),
                "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                "ram_total_gb": round(virtual_memory.total / (1024 ** 3), 2),
                "ram_available_gb": round(virtual_memory.available / (1024 ** 3), 2),
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}
    
    def _get_gpu_info(self) -> Dict:
        """Detect NVIDIA GPU information."""
        try:
            import torch
            
            if not torch.cuda.is_available():
                return {
                    "gpu_available": False,
                    "gpu_name": None,
                    "vram_gb": None,
                    "cuda_available": False,
                }
            
            device_count = torch.cuda.device_count()
            if device_count == 0:
                return {
                    "gpu_available": False,
                    "gpu_name": None,
                    "vram_gb": None,
                    "cuda_available": False,
                }
            
            # Get info for first GPU
            gpu_properties = torch.cuda.get_device_properties(0)
            vram_gb = gpu_properties.total_memory / (1024 ** 3)
            
            return {
                "gpu_available": True,
                "gpu_name": gpu_properties.name,
                "vram_gb": round(vram_gb, 2),
                "cuda_available": torch.cuda.is_available(),
                "device_count": device_count,
            }
        except Exception as e:
            logger.warning(f"Error detecting GPU: {e}")
            return {
                "gpu_available": False,
                "gpu_name": None,
                "vram_gb": None,
                "cuda_available": False,
            }
    
    def _get_cuda_info(self) -> Dict:
        """Get CUDA information."""
        try:
            import torch
            
            cuda_available = torch.cuda.is_available()
            cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else None
            
            return {
                "cuda_available": cuda_available,
                "cuda_version": cuda_version,
                "cudnn_version": torch.backends.cudnn.version() if cuda_available else None,
            }
        except Exception as e:
            logger.warning(f"Error getting CUDA info: {e}")
            return {
                "cuda_available": False,
                "cuda_version": None,
                "cudnn_version": None,
            }
    
    def _get_pytorch_info(self) -> Dict:
        """Get PyTorch information."""
        try:
            import torch
            
            return {
                "pytorch_version": torch.__version__,
                "pytorch_cuda_available": torch.cuda.is_available(),
                "pytorch_device": "cuda" if torch.cuda.is_available() else "cpu",
            }
        except Exception as e:
            logger.warning(f"Error getting PyTorch info: {e}")
            return {
                "pytorch_version": None,
                "pytorch_cuda_available": False,
                "pytorch_device": "cpu",
            }
    
    def get_summary(self) -> str:
        """Get a human-readable summary of hardware."""
        lines = []
        
        # System info
        lines.append("=== SYSTEM INFORMATION ===")
        lines.append(f"OS: {self.system_info.get('os', 'Unknown')}")
        lines.append(f"Processor: {self.system_info.get('processor', 'Unknown')}")
        lines.append(f"CPU Cores: {self.system_info.get('cpu_count', 'Unknown')}")
        lines.append(f"RAM: {self.system_info.get('ram_available_gb', '?')}GB / {self.system_info.get('ram_total_gb', '?')}GB")
        
        lines.append("\n=== GPU INFORMATION ===")
        if self.gpu_info.get('gpu_available'):
            lines.append(f"GPU: {self.gpu_info.get('gpu_name', 'Unknown')}")
            lines.append(f"VRAM: {self.gpu_info.get('vram_gb', '?')}GB")
            lines.append(f"Device Count: {self.gpu_info.get('device_count', 1)}")
        else:
            lines.append("GPU: Not detected or not available")
        
        lines.append("\n=== CUDA INFORMATION ===")
        lines.append(f"CUDA Available: {self.cuda_info.get('cuda_available', False)}")
        if self.cuda_info.get('cuda_version'):
            lines.append(f"CUDA Version: {self.cuda_info.get('cuda_version')}")
        if self.cuda_info.get('cudnn_version'):
            lines.append(f"cuDNN Version: {self.cuda_info.get('cudnn_version')}")
        
        lines.append("\n=== PYTORCH INFORMATION ===")
        lines.append(f"PyTorch Version: {self.pytorch_info.get('pytorch_version', 'Unknown')}")
        lines.append(f"PyTorch CUDA Available: {self.pytorch_info.get('pytorch_cuda_available', False)}")
        lines.append(f"PyTorch Device: {self.pytorch_info.get('pytorch_device', 'cpu')}")
        
        return "\n".join(lines)
    
    def get_compute_device(self) -> str:
        """Get the recommended compute device (cuda or cpu)."""
        if self.pytorch_info.get('pytorch_cuda_available') and self.gpu_info.get('gpu_available'):
            return "cuda"
        return "cpu"
    
    def get_vram_gb(self) -> float:
        """Get GPU VRAM in GB, 0 if no GPU."""
        return self.gpu_info.get('vram_gb', 0.0) or 0.0
    
    def is_vram_sufficient(self, required_gb: float) -> bool:
        """Check if VRAM is sufficient for given requirement."""
        vram = self.get_vram_gb()
        if vram == 0:
            return False
        return vram >= required_gb


# Create a singleton instance
hardware_info = HardwareInfo()
