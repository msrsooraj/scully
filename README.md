# Scully

A fast, offline photo culling tool for wildlife photographers.

Scully helps photographers quickly review thousands of RAW images by
identifying blurry photos, grouping duplicates, and optionally
evaluating subject sharpness using object detection.

The project is designed to be transparent, fast, and non-destructive.
Traditional computer vision is used wherever possible, with AI reserved
for cases where it provides a meaningful improvement.

> **⚠️ Work in Progress**
>
> This project is in its early stages of development. The architecture,
> APIs, project structure, and features are expected to evolve. Nothing
> should be considered stable until a v1.0 release.

------------------------------------------------------------------------

## Planned Features

-   Extract embedded JPEG previews from RAW images
-   Whole-image sharpness scoring using traditional computer vision
-   Duplicate and near-duplicate detection
-   Optional AI-assisted subject detection (YOLO)
-   Subject-specific sharpness scoring
-   CSV and HTML reports
-   Interactive desktop application
-   Cross-platform support (macOS, Windows and Linux)

------------------------------------------------------------------------

## Design Goals

-   Offline first
-   Fast processing
-   Non-destructive workflow
-   Transparent scoring
-   Modular architecture
-   Cross-platform

Whenever possible, Scully analyzes the embedded JPEG preview inside
RAW files instead of decoding the RAW image itself. This keeps
processing fast and avoids compatibility issues with newly released
camera formats.

------------------------------------------------------------------------

## Planned Processing Pipeline

``` text
RAW Images
    │
    ▼
Extract Embedded JPEG
    │
    ▼
Whole Image Sharpness
    │
    ▼
Duplicate Detection
    │
    ▼
(Optional) YOLO Subject Detection
    │
    ▼
Subject Sharpness Analysis
    │
    ▼
Classification & Report
```

------------------------------------------------------------------------

## Project Architecture

The project is being developed **library first**.

The image-processing engine is independent of the user interface,
allowing multiple frontends to reuse the same implementation.

``` text
scully/
├── extractor.py
├── sharpness.py
├── duplicates.py
├── detector.py
├── pipeline.py
└── models.py
```

The library will power several interfaces:

``` text
                 Python Library
                        │
        ┌───────────────┼───────────────┐
        │               │               │
      CLI            FastAPI      Desktop UI
```

This separation makes the algorithms reusable, testable, and independent
of any particular UI framework.

------------------------------------------------------------------------

## Planned Technology Stack

### Backend

-   Python
-   OpenCV
-   Ultralytics YOLO
-   ExifTool
-   SQLite

### API

-   FastAPI

### Desktop

-   React
-   Tauri

------------------------------------------------------------------------

## Roadmap

### Phase 1

-   CLI application
-   JPEG extraction
-   Sharpness scoring
-   Duplicate detection
-   CSV report

### Phase 2

-   Optional YOLO-based subject detection
-   Subject sharpness scoring
-   HTML report

### Phase 3

-   Desktop application
-   Thumbnail browser
-   Filter by sharp/blurry/duplicates
-   Move selected images into separate folders

### Future Ideas

-   Incremental scans
-   Background processing
-   GPU acceleration
-   Adjustable scoring thresholds
-   Plugin architecture
-   Additional AI models

------------------------------------------------------------------------

## Contributing

Contributions, bug reports, feature requests, and discussions are
welcome.

The project is intentionally being built in small, well-tested stages
before expanding into a full desktop application.

------------------------------------------------------------------------

## License

Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

See the `LICENSE` file for details.
