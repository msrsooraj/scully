from dataclasses import dataclass, field
from pathlib import Path

from .duplicates import compute_hash, group_duplicates
from .extractor import extract_preview
from .models import RawImage
from .sharpness import score

RAW_EXTENSIONS = {
    ".cr2", ".cr3",   # Canon
    ".nef", ".nrw",   # Nikon
    ".arw", ".srf",   # Sony
    ".raf",           # Fujifilm
    ".orf",           # Olympus
    ".rw2",           # Panasonic
    ".pef",           # Pentax
    ".dng",           # Adobe / Leica / misc
    ".mrw",           # Minolta
    ".srw",           # Samsung
    ".x3f",           # Sigma
}


@dataclass
class PipelineOptions:
    sharpness: bool = True
    duplicates: bool = True
    duplicate_threshold: int = 10
    # Phase 2: detect: bool = False


def discover(directory: Path) -> list[Path]:
    return sorted(
        p for p in directory.rglob("*")
        if p.suffix.lower() in RAW_EXTENSIONS
    )


def process(path: Path, options: PipelineOptions) -> RawImage:
    image = RawImage(path=path)
    preview = extract_preview(path)
    if options.sharpness:
        image.sharpness = score(preview)
    if options.duplicates:
        image.perceptual_hash = compute_hash(preview)
    return image


def run(directory: Path, options: PipelineOptions | None = None) -> list[RawImage]:
    if options is None:
        options = PipelineOptions()
    paths = discover(directory)
    results = [process(p, options) for p in paths]
    if options.duplicates:
        group_duplicates(results, threshold=options.duplicate_threshold)
    return results
