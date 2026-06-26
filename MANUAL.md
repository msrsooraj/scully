# Scully User Manual

Scully scans a folder of RAW images, scores each one for sharpness, detects near-duplicates, and writes a CSV report. It never moves, copies, or modifies your files.

---

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager

Install dependencies:

```bash
uv sync
```

---

## Basic Usage

```bash
uv run main.py <directory>
```

Scully will scan `<directory>` recursively for RAW files, process them, and write `report.csv` in the current working directory.

---

## Options

| Flag | Default | Description |
|---|---|---|
| `--output <path>` | `report.csv` | Path for the CSV report |
| `--sharpness` | off | Run sharpness scoring |
| `--duplicates` | off | Run duplicate detection |
| `--duplicate-threshold <n>` | `10` | Hash distance below which two images are considered duplicates (lower = stricter). Only relevant when `--duplicates` is used. |

Passing no step flags runs the full pipeline. Passing one or more step flags runs only those steps.

**Examples:**

```bash
# Full pipeline (no flags)
uv run main.py ~/Photos/birds

# Sharpness only
uv run main.py ~/Photos/birds --sharpness

# Duplicates only
uv run main.py ~/Photos/birds --duplicates

# Both explicitly, with a custom output and stricter threshold
uv run main.py ~/Photos/birds --sharpness --duplicates --output ~/Desktop/cull.csv --duplicate-threshold 5
```

---

## Supported RAW Formats

Canon `.cr2` `.cr3` · Nikon `.nef` `.nrw` · Sony `.arw` `.srf` · Fujifilm `.raf` · Olympus `.orf` · Panasonic `.rw2` · Pentax `.pef` · Minolta `.mrw` · Samsung `.srw` · Sigma `.x3f` · Adobe/Leica `.dng`

---

## Reading the Report

The CSV has three columns:

| Column | Description |
|---|---|
| `path` | Absolute path to the RAW file |
| `sharpness` | Laplacian variance score — higher means sharper |
| `duplicate_group` | Integer group ID shared by near-duplicate images; empty if the image has no duplicates |

### Sharpness scores

Scully uses the **variance of the Laplacian** on the embedded JPEG preview. There is no universal "good" threshold — it depends on your camera, lens, and preview resolution. A practical approach:

1. Open the CSV in a spreadsheet.
2. Sort by `sharpness` ascending to find the blurriest images.
3. Compare a few known-sharp and known-blurry pairs to calibrate your own cutoff.

### Duplicate groups

Images that share a `duplicate_group` number were taken in rapid succession or are near-identical (burst shots, accidental double-captures). Use the `--duplicate-threshold` flag to tune sensitivity:

- **Lower value (e.g. 5)** — only flags images that are extremely similar.
- **Higher value (e.g. 15)** — flags images that differ more (different exposures of the same scene).

The default of `10` works well for typical burst sequences.

---

## Skipped Files

If a RAW file cannot be processed (corrupt file, no embedded preview, unsupported variant), Scully prints a warning and continues. The file will not appear in the report.
