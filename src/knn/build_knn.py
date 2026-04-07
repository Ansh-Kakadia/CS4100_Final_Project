import numpy as np
import json
import os
import torch


def build_knn(embeddings: np.ndarray, k: int = 20):
    """Builds a KNN graph using cosine similarity."""

    embeddings = embeddings.astype(np.float32)

    # Normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1e-8, norms)
    normalized = embeddings / norms

    # Cosine similarity
    similarity = normalized @ normalized.T

    # Remove self-similarity
    np.fill_diagonal(similarity, -np.inf)

    # Top-k neighbors
    k = min(k, embeddings.shape[0] - 1)
    neighbor_indices = np.argsort(-similarity, axis=1)[:, :k]

    return neighbor_indices


def save_knn_graph(item_ids, neighbor_indices, output_path):
    graph = {}
    for i, item_id in enumerate(item_ids):
        graph[str(item_id)] = [str(item_ids[j]) for j in neighbor_indices[i]]

    with open(output_path, "w") as f:
        json.dump(graph, f, indent=2)


if __name__ == "__main__":
    cache_dir = "./cache"
    embeddings_path = os.path.join(cache_dir, "embeddings.pt")
    item_ids_path = os.path.join(cache_dir, "item_ids.json")
    output_path = os.path.join(cache_dir, "knn_graph.json")

    embeddings = torch.load(embeddings_path).numpy()

    with open(item_ids_path, "r") as f:
        item_ids = json.load(f)

    neighbor_indices = build_knn(embeddings, k=20)
    save_knn_graph(item_ids, neighbor_indices, output_path)

    print(f"Saved KNN graph to {output_path}")
