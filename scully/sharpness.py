import cv2
import numpy as np


def score(image_data: bytes) -> float:
    arr = np.frombuffer(image_data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not decode image data")
    return float(cv2.Laplacian(img, cv2.CV_64F).var())
