import json
import os
from PIL import Image
import matplotlib.pyplot as plt


def load_image(item_id: str):
    path = f"./fashion_items/images/{item_id}.jpg"
    if not os.path.exists(path):
        return None
    return Image.open(path)


def main():
    # Load KNN graph
    with open("./cache/knn_graph.json", "r") as f:
        knn_graph = json.load(f)

    # Pick an item to inspect
    query_id = list(knn_graph.keys())[7]  # can manually set - e.g., "15970"
    neighbor_ids = knn_graph[query_id][:5]

    print("Query:", query_id)
    print("Neighbors:", neighbor_ids)

    ids = [query_id] + neighbor_ids

    # Create plot
    fig, axes = plt.subplots(1, len(ids), figsize=(20, 5))

    for i, (ax, item_id) in enumerate(zip(axes, ids)):
        img = load_image(item_id)

        if img is not None:
            ax.imshow(img)
        else:
            ax.text(0.5, 0.5, "Missing", ha='center', va='center')

        if i == 0:
            ax.set_title(f"QUERY\n{item_id}")
        else:
            ax.set_title(f"NN\n{item_id}")

        ax.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()