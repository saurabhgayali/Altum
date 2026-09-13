# Single-Image 3D Photo Generator

## Overview

A standalone, offline-first Python desktop GUI that converts a single 2D
photograph into an interactive 2.5D/3D parallax photo.

The application will:

1.  Accept a single photo.
2.  Generate a depth map using an AI depth-estimation model.
3.  Project the photo into a virtual camera view to identify newly
    exposed/disoccluded regions.
4.  Generate plausible missing background content for those regions
    using an AI inpainting model.
5.  Generate a browser-based WebGL/WebGPU parallax viewer.
6.  Preview that exact HTML viewer inside the desktop application.
7.  Export the generated viewer as a self-contained HTML package that
    can be embedded or hosted on a website.

The application should not attempt to reproduce Facebook's proprietary
implementation. The goal is to create a high-quality, controllable
equivalent using locally available models and a browser-based renderer.

------------------------------------------------------------------------

## Core Pipeline

``` text
Single Photo
     |
     v
Depth Estimation
     |
     v
Depth Map
     |
     +-----------------------------+
     |                             |
     v                             v
Depth Processing              Original Photo
     |                             |
     +-------------+---------------+
                   |
                   v
          2.5D Scene Projection
                   |
                   v
        Disocclusion Detection
                   |
                   v
          Inpainting Mask
                   |
                   v
        AI Background Inpainting
                   |
                   v
        Completed Scene Texture
                   |
                   v
       HTML/WebGL Parallax Viewer
                   |
          +--------+--------+
          |                 |
          v                 v
     App Preview       HTML Export
```

------------------------------------------------------------------------

## Main Features

### 1. Single Photo Input

-   Open JPG, JPEG, PNG, and other commonly supported image formats.
-   Preserve the original image separately from all generated assets.
-   Display input image dimensions and basic image information.
-   Avoid modifying the source image.

### 2. AI Depth Generation

Generate a dense depth map from the input photograph.

Initial model target:

-   Marigold V2
-   Prefer a locally downloaded model.
-   Model selection should be abstracted so another depth model can be
    added later.

Outputs:

-   Numerical depth representation for processing.
-   Normalized depth visualization.
-   Exportable depth map.

Depth processing should include:

-   normalization
-   optional inversion
-   edge-aware smoothing
-   resolution handling
-   optional depth-strength adjustment

The depth map is geometry data, not merely a grayscale visual asset.

### 3. Disocclusion Detection

The application should determine which image regions become visible when
the virtual camera moves.

Process:

1.  Convert the RGB image and depth map into a 2.5D representation.
2.  Simulate a controlled range of virtual camera movement.
3.  Reproject the source pixels into the new camera view.
4.  Identify pixels for which no source pixel exists.
5.  Generate a disocclusion/inpainting mask.
6.  Expand/feather the mask where necessary to avoid visible seams.

Only genuinely missing regions should be sent to the inpainting stage
whenever possible.

### 4. AI Background Inpainting

Use a dedicated image-inpainting model to fill the regions exposed by
virtual camera movement.

Initial implementation should support a locally downloaded
diffusion-based inpainting model.

Candidate models:

-   Stable Diffusion 1.5 Inpainting
-   SDXL Inpainting
-   Other compatible Diffusers inpainting models

The architecture must allow the inpainting model to be replaced later.

Important rule:

**Do not regenerate the entire photograph.**

The original photograph should remain authoritative. AI generation
should primarily be restricted to disoccluded/missing regions.

Pipeline:

``` text
Original RGB
     +
Disocclusion Mask
     +
Optional context / depth information
     |
     v
Inpainting Model
     |
     v
Generated Missing Background
```

The application should support:

-   inpainting strength
-   mask expansion
-   feathering
-   inference steps
-   random seed
-   optional prompt
-   optional negative prompt
-   regeneration without rerunning depth estimation

The generated background should be stored separately so that users can
regenerate it without losing the original photo.

### 5. 2.5D / Parallax Renderer

The final viewer should be browser-based.

Do not use simple DOM image translation for the final renderer.

Preferred implementation:

-   WebGL initially
-   WebGPU may be considered later
-   GPU-accelerated shader-based depth displacement
-   Smooth virtual camera movement
-   Depth-aware rendering
-   Completed background texture

Supported interaction:

-   mouse movement
-   touch movement
-   optional device orientation
-   automatic motion
-   configurable parallax strength
-   configurable movement limits
-   smoothing/interpolation

The renderer should avoid excessive camera movement because large
movement magnifies depth-map and inpainting errors.

------------------------------------------------------------------------

## In-App Preview

The desktop application should **not implement a separate Python-native
parallax preview**.

The preview must use the **same generated HTML/JavaScript viewer that
will be exported**.

Conceptually:

``` text
Python Processing
       |
       v
Generated Assets
       |
       v
HTML Viewer
       |
       +--------------------+
       |                    |
       v                    v
Embedded App Preview     HTML Export
```

This ensures that what the user sees in the application is as close as
possible to the exported result.

The desktop GUI should host the generated HTML viewer using an embedded
browser/webview component.

The preview should update after:

-   depth generation
-   inpainting
-   parallax setting changes
-   renderer setting changes

Where possible, settings should update the viewer without regenerating
AI assets.

------------------------------------------------------------------------

## HTML Export

Export a self-contained web viewer.

Example package:

``` text
3d-photo/
├── index.html
├── viewer.js
├── assets/
│   ├── image.webp
│   ├── depth.webp
│   └── background.webp
└── README.txt
```

The exported viewer should:

-   require no Python installation
-   require no AI model
-   perform no AI inference
-   contain only the assets and browser renderer required for playback
-   work on normal modern browsers
-   be hostable on ordinary web hosting

The export should support two modes:

### Standalone HTML Package

A folder/ZIP containing all required files.

### Embeddable Viewer

Provide an iframe-friendly `index.html` or equivalent embed package.

Example intended usage:

``` html
<iframe
    src="https://example.com/my-3d-photo/"
    width="100%"
    height="600"
    frameborder="0"
    allow="autoplay">
</iframe>
```

The exported viewer should not depend on the Python application.

------------------------------------------------------------------------

## Desktop GUI

The application should be a standalone Python desktop application.

Suggested high-level layout:

``` text
+------------------------------------------------------+
| Single-Image 3D Photo Generator                     |
+------------------------------------------------------+
|                                                      |
|  [ Open Photo ]                                      |
|                                                      |
|  Input Image                                         |
|  +----------------------+                            |
|  |                      |                            |
|  |      Photo           |                            |
|  |                      |                            |
|  +----------------------+                            |
|                                                      |
|  [ Generate Depth ]                                   |
|  [ Generate Background ]                              |
|  [ Generate Preview ]                                 |
|                                                      |
|  Preview                                              |
|  +-----------------------------------------------+   |
|  |                                               |   |
|  |       Embedded HTML/WebGL 3D Preview         |   |
|  |                                               |   |
|  +-----------------------------------------------+   |
|                                                      |
|  [ Export HTML ]   [ Export ZIP ]                    |
+------------------------------------------------------+
```

The exact UI toolkit can be decided during implementation.

------------------------------------------------------------------------

## Settings

### Temporary Files Path

Provide a setting for where temporary/generated preview files are
stored.

Purpose:

-   HTML preview files
-   generated intermediate images
-   masks
-   temporary WebGL assets
-   processing intermediates

Example:

``` text
Settings
  > Temporary files path
      C:\Users\<user>\AppData\Local\3DPhoto\temp
```

Requirements:

-   selectable directory
-   display current path
-   validate write access
-   create directory if required
-   clear temporary files option
-   never store temporary files in the application installation
    directory unless explicitly configured

The preview HTML should be generated into this temporary location.

### Model Storage Path

Provide a separate setting for AI model storage.

Example:

``` text
Settings
  > Model storage
      D:\AI\Models\3DPhoto
```

Requirements:

-   selectable directory
-   depth models and inpainting models stored separately
-   show installed model status
-   allow changing the model storage location
-   do not duplicate models unnecessarily
-   detect existing compatible model files where possible

Suggested structure:

``` text
models/
├── depth/
│   └── marigold-v2/
└── inpainting/
    └── <model-name>/
```

------------------------------------------------------------------------

## Model Management

Provide dedicated download controls.

### Depth Model

UI:

``` text
Depth Model
Marigold V2
[ Download ]
Status: Not installed
```

After download:

``` text
Depth Model
Marigold V2
[ Re-download ] [ Delete ]
Status: Installed
```

Requirements:

-   download model from its official/model-host source
-   show download progress
-   show approximate storage requirement where available
-   verify download/model availability
-   do not silently download models during normal processing
-   clearly report missing model dependencies

### Inpainting Model

UI:

``` text
Inpainting Model
<Selected Model>
[ Download ]
Status: Not installed
```

The application should eventually allow multiple compatible inpainting
models, but MVP can expose one recommended model.

The user should explicitly initiate model downloads.

------------------------------------------------------------------------

## GPU Detection

On startup and in Settings/System Information, detect available
hardware.

Display:

``` text
Compute Device
GPU: NVIDIA GeForce RTX XXXX
VRAM: XX GB
CUDA: Available
CUDA Version: X.X
PyTorch CUDA: Available
```

Possible states:

``` text
GPU detected and available
GPU detected but CUDA unavailable
No supported GPU detected
CPU fallback
```

Requirements:

-   detect NVIDIA GPU where CUDA is available
-   detect VRAM
-   detect CUDA availability through the installed ML runtime
-   display CPU information as fallback
-   clearly warn when available VRAM is insufficient for the selected
    model/resolution
-   allow CPU fallback where technically supported
-   never claim GPU acceleration if the actual inference backend is
    using CPU

The application should perform a startup capability check rather than
waiting for inference to fail.

------------------------------------------------------------------------

## Processing States

The UI should clearly communicate progress:

``` text
1. Loading image
2. Generating depth
3. Processing depth
4. Simulating camera movement
5. Detecting disocclusions
6. Generating background
7. Preparing viewer
8. Preview ready
```

Long-running AI operations must not freeze the GUI.

------------------------------------------------------------------------

## Regeneration Logic

Avoid unnecessary AI inference.

Example:

``` text
Change parallax strength
    -> regenerate viewer only

Change camera movement range
    -> regenerate disocclusion/background only if required

Change depth strength
    -> regenerate viewer; optionally regenerate background if geometry changes materially

Regenerate background seed
    -> rerun inpainting only

Change depth model
    -> rerun depth + downstream processing

Change inpainting model
    -> rerun inpainting + downstream viewer generation
```

The application should cache intermediate results.

------------------------------------------------------------------------

## Project/Temporary Data

A processing session may contain:

``` text
project/
├── source/
│   └── original.jpg
├── depth/
│   ├── depth.npy
│   └── depth.png
├── disocclusion/
│   └── mask.png
├── background/
│   └── completed.webp
├── preview/
│   ├── index.html
│   ├── viewer.js
│   └── assets/
└── metadata.json
```

The exact project persistence model can be finalized later.

------------------------------------------------------------------------

## Offline-First / Privacy

The application should be designed for local processing.

After models are downloaded:

-   photo processing should happen locally
-   no image uploads
-   no telemetry
-   no mandatory cloud service
-   no API key required for core functionality
-   exported HTML should work independently of the desktop application

Network access should primarily be required for explicit model downloads
and application updates if updates are implemented later.

------------------------------------------------------------------------

## Performance Considerations

AI inference is the expensive portion.

The browser renderer should remain lightweight.

Important optimization targets:

-   use GPU inference when available
-   resize extremely large source images to a configurable processing
    resolution
-   cache depth output
-   cache inpainting output
-   use compressed web assets for export
-   use WebP/AVIF where browser compatibility permits
-   avoid repeatedly running AI models when only viewer settings changed

The exported viewer should prioritize smooth interaction over maximum
source-image resolution.

------------------------------------------------------------------------

## MVP Scope

### MVP 1

-   Python desktop GUI
-   Open single image
-   GPU detection
-   Model storage setting
-   Temporary files setting
-   Marigold V2 download/installation
-   Inference to depth map
-   Basic 2.5D projection
-   HTML/WebGL viewer
-   Embedded HTML preview
-   HTML export

### MVP 2

-   Inpainting model download/installation
-   Disocclusion mask generation
-   AI background inpainting
-   Seamless parallax over a controlled camera range
-   Inpainting regeneration controls

### MVP 3

-   Advanced renderer controls
-   Touch/device orientation
-   Automatic parallax motion
-   Better depth refinement
-   Better disocclusion handling
-   Multiple inpainting/depth model support
-   ZIP export
-   Project/session saving

------------------------------------------------------------------------

## Non-Goals

The initial project should not attempt to:

-   reproduce Facebook's proprietary 3D Photo format
-   create an actual volumetric 3D model
-   generate a full 3D mesh suitable for Blender
-   perform unrestricted camera movement
-   guarantee perfect reconstruction of unseen objects
-   require cloud inference
-   build a social platform
-   provide an online image-processing service

The target is a **high-quality 2.5D interactive photograph**.

------------------------------------------------------------------------

## Technical Architecture

Suggested separation:

``` text
src/
├── app/
│   ├── gui/
│   └── settings/
├── ai/
│   ├── depth/
│   └── inpainting/
├── processing/
│   ├── depth_processing/
│   ├── projection/
│   ├── disocclusion/
│   └── compositing/
├── preview/
│   ├── webview/
│   └── temp/
├── export/
│   └── html/
├── hardware/
│   └── gpu_detection/
└── models/
    └── model_manager/
```

Browser-side viewer:

``` text
web/
├── index.html
├── viewer.js
├── renderer.js
└── shaders/
```

Python should handle:

-   AI inference
-   image/depth processing
-   model management
-   GPU detection
-   project generation
-   temporary-file management
-   export packaging

JavaScript should handle:

-   3D rendering
-   camera movement
-   interaction
-   browser-side animation
-   exported viewer functionality

------------------------------------------------------------------------

## Key Design Principle

The application should separate **content generation** from **content
playback**.

``` text
Python + AI
    =
Generate the 2.5D scene

HTML + WebGL
    =
Play the 2.5D scene smoothly
```

This makes the expensive desktop processing a one-time operation while
allowing the final result to be embedded on ordinary websites without
Python, CUDA, or AI models.
