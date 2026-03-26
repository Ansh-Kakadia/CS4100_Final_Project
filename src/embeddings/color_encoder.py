import numpy as np
from tqdm import tqdm

from src.data.embedding.image_dominant_colors import get_most_dominant_colors


class ColorEncoder:
    """
    Encodes a fashion item as a flat vector of its dominant RGB colors.
    Delegates color extraction to get_most_dominant_colors (KMeans + rembg background removal).

    Output shape: (k * 3,) float32, values normalized to [0, 1].

    Future extension: additional encoders (e.g. HOG) can be concatenated
    in build_embeddings.py before saving to cache.
    """

    def __init__(self, images_dir: str, k: int = 3):
        self.images_dir = images_dir
        self.k = k
        self.output_dim = k * 3

    def encode(self, item_id: int) -> np.ndarray:
        try:
            colors = get_most_dominant_colors(str(item_id), self.k, self.images_dir)
            # colors: (k, 3) int array, values 0-255
            return colors.flatten().astype(np.float32) / 255.0
        except Exception:
            return np.zeros(self.output_dim, dtype=np.float32)

    def encode_batch(self, item_ids: list[int]) -> np.ndarray:
        results = np.zeros((len(item_ids), self.output_dim), dtype=np.float32)
        for i, item_id in enumerate(tqdm(item_ids, desc="Encoding colors")):
            results[i] = self.encode(item_id)
        return results
