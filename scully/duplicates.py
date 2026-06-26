import io

import imagehash
from PIL import Image

from .models import RawImage


def compute_hash(image_data: bytes) -> str:
    img = Image.open(io.BytesIO(image_data))
    return str(imagehash.phash(img))


def group_duplicates(images: list[RawImage], threshold: int = 10) -> None:
    """Mutates images in-place, setting duplicate_group on near-duplicates."""
    indexed = [(i, img) for i, img in enumerate(images) if img.perceptual_hash is not None]
    if not indexed:
        return

    original_indices, valid = zip(*indexed)
    hashes = [imagehash.hex_to_hash(img.perceptual_hash) for img in valid]
    n = len(hashes)

    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        parent[find(x)] = find(y)

    for i in range(n):
        for j in range(i + 1, n):
            if hashes[i] - hashes[j] <= threshold:
                union(i, j)

    groups: dict[int, list[int]] = {}
    for local_idx in range(n):
        groups.setdefault(find(local_idx), []).append(local_idx)

    group_id = 0
    for members in groups.values():
        if len(members) > 1:
            for local_idx in members:
                images[original_indices[local_idx]].duplicate_group = group_id
            group_id += 1
