import numpy as np

from src.data.item import FashionItem
from src.embeddings.color_encoder import ColorEncoder
from src.embeddings.data_encoder import DataEncoder


class ItemEmbedder:
    def __init__(self, images_dir: str, k: int = 3, color_lookup: dict | None = None):
        self.color_encoder = ColorEncoder(images_dir, k, color_lookup=color_lookup)
        self.data_encoder = DataEncoder()

    def embed(self, items: list[FashionItem]) -> np.ndarray:
        item_ids = [item.item_id for item in items]
        color_vectors = self.color_encoder.encode_batch(item_ids)
        data_vectors = self.data_encoder.encode_batch(items)
        return np.hstack([color_vectors, data_vectors])
