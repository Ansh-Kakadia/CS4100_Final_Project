import json
import os
import torch

from src.data.loader import FashionDataset
from src.embeddings.embedder import ItemEmbedder
from src.matching.slot_filler import load_color_lookup


def build_embeddings(csv_path: str, images_dir: str, color_json_path: str, gender: str = None, output_dir: str = "./cache"):
    os.makedirs(output_dir, exist_ok=True)

    dataset = FashionDataset(csv_path, images_dir, gender)
    items = dataset.items

    color_lookup = load_color_lookup(color_json_path)
    embedder = ItemEmbedder(images_dir, color_lookup=color_lookup)
    embedder.data_encoder.fit(items)
    embedder.data_encoder.save(os.path.join(output_dir, "data_vocab.json"))

    embeddings = embedder.embed(items)

    torch.save(torch.from_numpy(embeddings), os.path.join(output_dir, "embeddings.pt"))
    with open(os.path.join(output_dir, "item_ids.json"), "w") as f:
        json.dump([item.item_id for item in items], f)

    print(f"Shape: {embeddings.shape}")
    print(f"Saved {len(items)} items to {output_dir}")


if __name__ == "__main__":
    build_embeddings(
        csv_path="./fashion_items/styles.csv",
        images_dir="./fashion_items/images",
        color_json_path="./fashion_items/styles.json",
    )
