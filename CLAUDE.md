# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Scully is a fast, offline photo culling tool for wildlife photographers. It identifies blurry photos, groups duplicates, and optionally evaluates subject sharpness using object detection. The project is early-stage (pre-v1.0); architecture and APIs are expected to evolve.

## Commands

This project uses `uv` for package management (Python 3.14 required).

```bash
uv run main.py          # Run the entry point
uv add <package>        # Add a dependency
uv sync                 # Install dependencies
```

## Architecture

The project is built **library first** — the image-processing engine is decoupled from any UI, so multiple frontends can share the same core.

**Planned library modules** (not yet implemented):

| Module | Responsibility |
|---|---|
| `scully/extractor.py` | Extract embedded JPEG previews from RAW files |
| `scully/sharpness.py` | Whole-image sharpness scoring (traditional CV) |
| `scully/duplicates.py` | Near-duplicate detection |
| `scully/detector.py` | Optional YOLO subject detection |
| `scully/pipeline.py` | Orchestrates the full processing pipeline |
| `scully/models.py` | Shared data models |

**Planned frontends** powered by the same library: CLI, FastAPI (REST API), and a Tauri + React desktop app.

**Processing pipeline order:**
RAW images → extract embedded JPEG → whole-image sharpness → duplicate detection → (optional) YOLO subject detection → subject sharpness → classification & report

## Key Design Constraints

- **Offline first** — no network calls during image processing.
- **Non-destructive** — Scully never modifies or deletes original files.
- **Use embedded JPEG previews** inside RAW files rather than decoding the RAW directly; this is the core performance strategy.
- **Traditional CV over AI by default** — use OpenCV/classical methods first; bring in YOLO only where it provides a clear benefit (subject detection).

## Planned Stack

- **Core:** Python, OpenCV, ExifTool, SQLite
- **AI (optional):** Ultralytics YOLO
- **API:** FastAPI
- **Desktop:** Tauri + React
