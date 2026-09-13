# Altum - Single-Image 3D Photo Generator Roadmap

## Project Overview
A standalone, offline-first Python desktop GUI that converts a single 2D photograph into an interactive 2.5D/3D parallax photo using PyQt.

## Phase 1: MVP1 - Foundation & Core Infrastructure

### 1.1 Project Setup
- [x] Understand project requirements from idea(4).md
- [x] Create project structure with `/src`, `/ai`, and `/status` folders
- [ ] Initialize git repository with proper structure
- [ ] Create virtual environment setup

### 1.2 Desktop GUI Framework (PyQt)
- [ ] Create main application window class
- [ ] Implement menu bar and toolbar
- [ ] Create status bar with processing state display
- [ ] Implement tabbed interface for different sections
- [ ] Add logging UI component

### 1.3 Image Input & Management
- [ ] Implement image file open dialog (JPG, JPEG, PNG, etc.)
- [ ] Create image display widget
- [ ] Display image metadata (dimensions, format, file size)
- [ ] Implement image validation and error handling
- [ ] Preserve original image without modification

### 1.4 Hardware Detection
- [ ] Detect NVIDIA GPU and CUDA availability
- [ ] Display VRAM information
- [ ] Show CUDA version
- [ ] Detect PyTorch CUDA support
- [ ] Implement CPU fallback detection
- [ ] Create System Information UI component
- [ ] Add VRAM sufficiency warnings

### 1.5 Settings Management
- [ ] Create settings dialog UI
- [ ] Implement temporary files path setting with validation
- [ ] Implement model storage path setting with validation
- [ ] Add write-access validation for paths
- [ ] Create auto-create directory functionality
- [ ] Implement clear temporary files option
- [ ] Persist settings to configuration file

### 1.6 Model Management Infrastructure
- [ ] Create model manager base class
- [ ] Implement model status tracking system
- [ ] Create download progress UI
- [ ] Implement model verification system
- [ ] Create separate depth and inpainting model directories
- [ ] Add model installation status display

---

## Phase 2: MVP1 - AI Model Integration

### 2.1 Depth Model (Marigold V2)
- [ ] Create depth model abstraction
- [ ] Implement Marigold V2 model loader
- [ ] Create model download functionality with progress tracking
- [ ] Implement depth inference pipeline
- [ ] Add VRAM check before inference
- [ ] Create GPU/CPU inference selection

### 2.2 Depth Processing
- [ ] Implement depth map normalization
- [ ] Add optional depth inversion
- [ ] Implement edge-aware smoothing
- [ ] Add resolution handling and resizing
- [ ] Implement depth-strength adjustment controls
- [ ] Export depth map as visualization

### 2.3 Processing Pipeline States
- [ ] Create processing state manager
- [ ] Implement UI state updates during processing
- [ ] Add async task execution for long-running operations
- [ ] Implement progress callbacks
- [ ] Create cancellation mechanism
- [ ] Add detailed logging for each processing stage

---

## Phase 3: MVP1 - 2.5D Visualization & Export

### 3.1 2.5D Scene Projection
- [ ] Implement RGB to 2.5D representation converter
- [ ] Create basic 3D projection engine
- [ ] Implement virtual camera simulation
- [ ] Add reprojection calculations

### 3.2 HTML/WebGL Viewer Generation
- [ ] Create HTML template generation system
- [ ] Implement WebGL-based renderer
- [ ] Create vertex and fragment shaders for parallax
- [ ] Implement camera movement based on mouse input
- [ ] Add smooth interpolation for camera movement
- [ ] Implement configurable parallax strength

### 3.3 In-App Preview
- [ ] Create embedded HTML viewer widget (QWebEngineView)
- [ ] Implement live preview rendering
- [ ] Add preview update triggers after depth/inpainting
- [ ] Implement preview refresh without AI re-inference

### 3.4 HTML Export
- [ ] Create self-contained HTML package exporter
- [ ] Implement WebP/AVIF asset compression
- [ ] Create standalone ZIP export functionality
- [ ] Implement embeddable iframe HTML mode
- [ ] Create README.txt in exports
- [ ] Test standalone HTML playback in browsers

---

## Phase 4: MVP2 - Advanced 2.5D & Inpainting

### 4.1 Disocclusion Detection
- [ ] Implement controlled camera movement simulation range
- [ ] Implement pixel reprojection algorithm
- [ ] Create disocclusion/inpainting mask generation
- [ ] Implement mask expansion and feathering
- [ ] Add mask visualization for debugging

### 4.2 Inpainting Model Integration
- [ ] Create inpainting model abstraction
- [ ] Implement inpainting model download & installation
- [ ] Support Stable Diffusion 1.5 Inpainting
- [ ] Support SDXL Inpainting
- [ ] Implement inference pipeline with context
- [ ] Add seed and strength controls

### 4.3 AI Background Inpainting
- [ ] Create inpainting mask application
- [ ] Implement inpainting inference with:
  - Inpainting strength parameter
  - Mask expansion control
  - Feathering control
  - Inference steps selection
  - Random seed selection
  - Optional prompt input
  - Optional negative prompt input
- [ ] Implement regeneration without re-running depth
- [ ] Store generated background separately
- [ ] Add inpainting preview

### 4.4 Seamless Parallax Enhancement
- [ ] Improve parallax viewer with inpainted background
- [ ] Test seam visibility across camera range
- [ ] Implement advanced camera movement smoothing
- [ ] Add controlled camera range limits

---

## Phase 5: MVP3 - Polish & Advanced Features

### 5.1 Advanced Renderer Controls
- [ ] Add parallax strength slider
- [ ] Implement movement limit controls
- [ ] Add smoothing/interpolation options
- [ ] Implement multiple interaction modes:
  - Mouse movement
  - Touch movement
  - Device orientation support
  - Automatic motion option

### 5.2 Model Selection & Management
- [ ] Support multiple depth models (extensible architecture)
- [ ] Support multiple inpainting models
- [ ] Implement model switching UI
- [ ] Add model capability detection

### 5.3 Project/Session Management
- [ ] Create project save functionality
- [ ] Implement project load functionality
- [ ] Save session metadata
- [ ] Cache intermediate results (depth, masks, backgrounds)
- [ ] Implement project directory structure

### 5.4 Advanced Depth Refinement
- [ ] Implement edge-aware depth enhancement
- [ ] Add manual depth adjustment tools
- [ ] Create depth map editing capabilities
- [ ] Add depth visualization options

### 5.5 Disocclusion Improvements
- [ ] Enhanced edge detection at disocclusions
- [ ] Implement better mask feathering algorithms
- [ ] Add manual disocclusion refinement tools

### 5.6 Export Enhancements
- [ ] Implement ZIP export with proper structure
- [ ] Add multiple quality/resolution presets
- [ ] Create embeddable viewer variant
- [ ] Generate comprehensive README for exports
- [ ] Test iframe embedding in websites

### 5.7 Performance Optimizations
- [ ] Implement configurable processing resolution
- [ ] Add image downsampling for large inputs
- [ ] Optimize asset compression for export
- [ ] Profile and optimize inference performance
- [ ] Implement GPU memory management

---

## Phase 6: Finalization

### 6.1 Testing & Validation
- [ ] Unit tests for core modules
- [ ] Integration tests for pipeline
- [ ] Test with various image sizes and formats
- [ ] GPU and CPU fallback testing
- [ ] Cross-browser compatibility testing for exports
- [ ] Performance benchmarking

### 6.2 Documentation
- [ ] User guide documentation
- [ ] API documentation for extensible components
- [ ] Model integration guide
- [ ] Architecture documentation

### 6.3 Build & Distribution
- [ ] Create requirements.txt with all dependencies
- [ ] Create build.py for automated compilation
- [ ] Test build process on clean environment
- [ ] Create installation instructions
- [ ] Package for distribution

### 6.4 Project Completion
- [ ] Final code review
- [ ] Security review
- [ ] Performance review
- [ ] Documentation review
- [ ] Release preparation

---

## Key Technical Milestones

| Milestone | Phase | Target |
|-----------|-------|--------|
| GUI Framework Ready | 1.2 | Week 1 |
| Model Management | 1.6 + 2.1 | Week 2 |
| Basic 2.5D Viewer | 3.1-3.4 | Week 3 |
| Inpainting Pipeline | 4.1-4.3 | Week 4 |
| Advanced Features | 5.1-5.7 | Week 5 |
| Build & Release | 6.1-6.4 | Week 6 |

---

## Technology Stack

- **GUI Framework**: PyQt6
- **AI Models**: Marigold V2 (depth), Stable Diffusion (inpainting)
- **ML Frameworks**: PyTorch, Diffusers, transformers
- **Web Rendering**: WebGL, JavaScript
- **Image Processing**: OpenCV, Pillow, NumPy
- **Async**: Python asyncio, threading
- **Build**: Python venv, pip

---

## Architecture Overview

```
src/
├── app/
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── widgets/
│   │   ├── dialogs/
│   │   └── styles/
│   ├── settings/
│   │   └── settings_manager.py
│   └── main.py
├── ai/
│   ├── depth/
│   │   ├── depth_estimator.py
│   │   ├── marigold_model.py
│   │   └── processors/
│   ├── inpainting/
│   │   ├── inpainting_model.py
│   │   └── processors/
│   └── model_manager.py
├── processing/
│   ├── depth_processing/
│   ├── projection/
│   ├── disocclusion/
│   └── compositing/
├── preview/
│   ├── webview/
│   │   └── embedded_viewer.py
│   ├── temp_manager.py
│   └── html_generator.py
├── export/
│   ├── html_exporter.py
│   ├── zip_exporter.py
│   └── templates/
├── hardware/
│   └── gpu_detection.py
└── models/
    └── model_manager.py

web/
├── index.html
├── viewer.js
├── renderer.js
├── shaders/
│   ├── vertex.glsl
│   └── fragment.glsl
└── styles.css

build.py
requirements.txt
```

---

## File Structure After Setup

```
Altum/
├── ai/
│   └── idea(4).md (moved from root)
├── status/
│   ├── roadmap.md
│   └── status.md
├── src/
│   ├── app/
│   ├── ai/
│   ├── processing/
│   ├── preview/
│   ├── export/
│   ├── hardware/
│   └── models/
├── web/
├── build.py
├── requirements.txt
└── README.md
```
