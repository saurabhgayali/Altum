# Altum - Single-Image 3D Photo Generator

A standalone, offline-first Python desktop GUI that converts a single 2D photograph into an interactive 2.5D/3D parallax photo.

## Features

- **PyQt6 Desktop Application**: Modern, responsive GUI
- **AI-Powered Depth Estimation**: Uses Marigold V2 model for depth generation
- **Parallax Image Generation**: Creates interactive 2.5D parallax effects
- **WebGL Viewer**: Browser-based 3D viewer for the generated photos
- **Offline Processing**: All processing happens locally - no cloud required
- **Model Management**: Download and manage AI models locally
- **Hardware Detection**: Automatic GPU detection and CUDA support
- **Flexible Export**: Export as self-contained HTML or ZIP packages

## Project Structure

```
Altum/
├── ai/                              # AI/Project documentation
│   └── idea(4).md                  # Project specification
├── status/                          # Project status tracking
│   ├── roadmap.md                  # Development roadmap
│   └── status.md                   # Task status tracker
├── src/                            # Main source code
│   ├── app/                        # Application logic
│   │   ├── main.py                # Entry point
│   │   ├── image_utils.py         # Image handling utilities
│   │   ├── gui/                   # GUI components
│   │   │   ├── main_window.py     # Main application window
│   │   │   ├── widgets/           # Custom widgets
│   │   │   ├── dialogs/           # Dialog windows
│   │   │   └── styles/            # UI stylesheets
│   │   └── settings/              # Settings management
│   ├── ai/                        # AI models and inference
│   │   ├── depth/                # Depth estimation
│   │   └── inpainting/           # Inpainting models
│   ├── processing/               # Image processing pipeline
│   │   ├── depth_processing/    # Depth map processing
│   │   ├── projection/          # 3D projection
│   │   ├── disocclusion/        # Disocclusion detection
│   │   └── compositing/         # Image compositing
│   ├── preview/                 # Preview generation
│   ├── export/                  # Export functionality
│   ├── hardware/                # Hardware detection
│   │   └── gpu_detection.py     # GPU and system info
│   └── models/                  # Model management
├── web/                         # Browser-based viewer
│   ├── index.html
│   ├── viewer.js
│   ├── renderer.js
│   └── shaders/
├── build.py                     # Build script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Requirements

- Python 3.10 or higher
- pip package manager
- 8GB RAM minimum (16GB+ recommended for GPU processing)
- NVIDIA GPU with CUDA support (optional, CPU fallback available)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saurabhgayali/Altum.git
cd Altum
```

### 2. Build and Setup Virtual Environment

The project includes an automated build script that sets up a virtual environment and installs all dependencies:

```bash
python3 build.py
```

This will:
- Create a virtual environment in the `venv` directory
- Upgrade pip, setuptools, and wheel
- Install all dependencies from `requirements.txt`
- Run basic validation tests

#### Custom Virtual Environment Path

To use a custom path for the virtual environment:

```bash
python3 build.py --venv /path/to/venv
```

#### Clean Build

To remove and recreate the virtual environment:

```bash
python3 build.py --clean
```

### 3. Activate Virtual Environment

After the build completes, activate the virtual environment:

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

## Running the Application

### Using the Virtual Environment

```bash
python -m src.app.main
```

### Manual Run with Python

```bash
cd /path/to/Altum
python -m src.app.main
```

## Development Roadmap

See [status/roadmap.md](status/roadmap.md) for the complete development roadmap.

### Current Phase: Phase 1 - MVP1 Foundation

**Completed:**
- [x] Project setup and documentation
- [x] PyQt6 GUI framework
- [x] Image input and management
- [x] Settings management system
- [x] Hardware detection module
- [x] Model manager infrastructure

**In Progress:**
- [ ] Settings dialog UI
- [ ] Hardware detection UI integration
- [ ] Model management UI
- [ ] Begin Phase 2 - AI model integration

### Planned Phases

1. **Phase 1**: MVP1 - Foundation & Core Infrastructure ✓ (80% complete)
2. **Phase 2**: MVP1 - AI Model Integration
3. **Phase 3**: MVP1 - 2.5D Visualization & Export
4. **Phase 4**: MVP2 - Advanced 2.5D & Inpainting
5. **Phase 5**: MVP3 - Polish & Advanced Features
6. **Phase 6**: Finalization & Release

## Project Status

See [status/status.md](status/status.md) for detailed task tracking and completion status.

**Overall Completion**: 10.2% (13/127 tasks)
**Current Phase**: Phase 1 - MVP1 Foundation & Core Infrastructure

## Architecture

### Python Backend (Desktop Application)
- **Framework**: PyQt6
- **Image Processing**: Pillow, OpenCV, NumPy
- **AI/ML**: PyTorch, Transformers, Diffusers
- **Async Processing**: asyncio, threading

### Browser Frontend (Web Viewer)
- **Language**: JavaScript (ES6+)
- **Graphics**: WebGL
- **Rendering**: Custom shader-based depth displacement

## Key Design Principles

1. **Separation of Concerns**: Content generation (Python + AI) vs. content playback (HTML + WebGL)
2. **Offline-First**: All processing happens locally after models are downloaded
3. **Privacy**: No image uploads, no telemetry, no cloud required
4. **Performance**: GPU acceleration when available, CPU fallback supported
5. **Extensibility**: Plugin architecture for custom depth/inpainting models

## Usage Workflow

### Basic Workflow

1. **Open Image**: Load a single 2D photograph (JPG, PNG, etc.)
2. **Generate Depth**: Use AI to estimate depth map from the image
3. **Generate Background**: Use inpainting to fill disoccluded regions
4. **Preview**: View interactive parallax effect in the app
5. **Export**: Export as self-contained HTML or ZIP package

### Advanced Options

- Adjust depth processing parameters
- Fine-tune inpainting results
- Control parallax strength and camera movement
- Generate multiple variations with different seeds
- Customize export quality and format

## System Information

The app automatically detects and displays:
- GPU model and VRAM
- CUDA version and availability
- PyTorch GPU support
- CPU and RAM information
- Recommended processing device

## Settings

Settings are stored in the user's config directory:
- **Windows**: `%APPDATA%\Altum\settings.json`
- **Linux**: `~/.config/Altum/settings.json`
- **macOS**: `~/Library/Preferences/Altum/settings.json`

### Configurable Settings

- **Temporary Files Path**: Where processing intermediates are stored
- **Model Storage Path**: Where AI models are downloaded
- **Processing Resolution**: Maximum resolution for AI processing
- **GPU Enabled**: Whether to use GPU acceleration
- **Processing Threads**: Number of parallel processing threads

## Troubleshooting

### GPU Not Detected

1. Ensure NVIDIA drivers are installed
2. Verify CUDA toolkit installation
3. Check: `python -c "import torch; print(torch.cuda.is_available())"`

### Out of Memory Errors

1. Reduce processing resolution in settings
2. Close other applications
3. Try CPU mode (Settings → Processing)

### Build Issues

1. Ensure Python 3.10+ is installed
2. Try `python3 build.py --clean`
3. Manually install: `pip install -r requirements.txt`

### Missing Dependencies

Install missing packages:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [status/roadmap.md](status/roadmap.md) for development priorities.

## License

[To be determined]

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- Marigold V2 for depth estimation
- Stable Diffusion for inpainting
- PyQt6 for GUI framework
- PyTorch and Hugging Face for ML infrastructure

---

**Current Version**: 0.1.0 (Early Development)

**Last Updated**: 2026-09-13

For more information, see the [Project Specification](ai/idea(4).md)
