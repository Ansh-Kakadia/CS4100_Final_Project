import numpy as np
from tqdm import tqdm


class ColorEncoder:
    """
    Encodes a fashion item as a flat vector of its dominant RGB colors.

    If a precomputed color_lookup is provided (item_id -> (dominant, secondary)),
    uses those directly (fast path). Otherwise falls back to rembg + KMeans on
    the raw image (slow path).

    Output shape:
      - With lookup: (6,) float32  — dominant [R,G,B] + secondary [R,G,B], normalized to [0, 1]
      - Without lookup: (k * 3,) float32, normalized to [0, 1]
    """

    def __init__(
        self,
        images_dir: str,
        k: int = 3,
        color_lookup: dict[int, tuple[list[int], list[int]]] | None = None,
    ):
        self.images_dir = images_dir
        self.k = k
        self.color_lookup = color_lookup or {}
        self.output_dim = 6 if self.color_lookup else k * 3

    def encode(self, item_id: int) -> np.ndarray:
        if self.color_lookup:
            entry = self.color_lookup.get(item_id)
            if entry is not None:
                dominant, secondary = entry
                return np.array(dominant + secondary, dtype=np.float32) / 255.0
            return np.zeros(6, dtype=np.float32)

        try:
            from src.data.image_dominant_colors import get_most_dominant_colors_kaggle
            colors = get_most_dominant_colors_kaggle(str(item_id), self.k)
            return colors.flatten().astype(np.float32) / 255.0
        except Exception:
            return np.zeros(self.output_dim, dtype=np.float32)

    def encode_batch(self, item_ids: list[int]) -> np.ndarray:
        results = np.zeros((len(item_ids), self.output_dim), dtype=np.float32)
        for i, item_id in enumerate(tqdm(item_ids, desc="Encoding colors")):
            results[i] = self.encode(item_id)
        return results
