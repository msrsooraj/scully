from dataclasses import dataclass
from pathlib import Path


@dataclass
class RawImage:
    path: Path
    sharpness: float | None = None
    perceptual_hash: str | None = None
    duplicate_group: int | None = None
