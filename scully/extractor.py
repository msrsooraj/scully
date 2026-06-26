from pathlib import Path

import cv2
import numpy as np
import rawpy


def extract_preview(path: Path) -> bytes:
    with rawpy.imread(str(path)) as raw:
        thumb = raw.extract_thumb()

    if thumb.format == rawpy.ThumbFormat.JPEG:
        return bytes(thumb.data)

    # BITMAP fallback: encode as JPEG in memory
    bgr = cv2.cvtColor(thumb.data, cv2.COLOR_RGB2BGR)
    _, buf = cv2.imencode(".jpg", bgr)
    return bytes(buf)
