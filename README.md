# Fashion Outfit Optimizer


## Beginner's Guide

To setup this project, take the following steps:

- Navigate to the project directory in your terminal

- Create your virtual environment with the command 
    - `python -m venv venv`

- Activate your virtual environment with one of the 
    - Windows: `.\venv\Scripts\activate`
    - Mac/Linux: `source venv/bin/activate`

- Run the following command in the terminal to install the correct dependencies
    - `pip install -r requirements.txt`

- Then run the `init_dataset.py` file

- To add the Polyvore dataset, you should uncompress `polyvore_dataset/polyvore.tar.gz` to `polyvore_dataset`

- Build embeddings (one-time, slow): `python src/embeddings/build_embeddings.py`

- Build KNN graph (one-time): `python src/knn/build_knn.py`

- Run the optimizer: `python src/main.py --gender Men`

---

## Project Structure

```
src/
├── data/
│   ├── item.py              # FashionItem dataclass
│   └── loader.py            # FashionDataset — parses CSV, indexes by slot
├── embeddings/
│   ├── image_encoder.py     # ResNet-18 feature extractor (512-d)
│   ├── meta_encoder.py      # One-hot encoder for colour/usage/season (~57-d)
│   └── build_embeddings.py  # CLI: encodes all items → cache/embeddings.pt
├── knn/
│   └── build_knn.py         # CLI: builds K=20 NN graph → cache/knn_graph.json
├── optimizer/
│   ├── energy.py            # OutfitEnergy: weighted sum of 4 terms
│   ├── neighbor.py          # NeighborGenerator: proposes KNN-based moves
│   └── sa.py                # SimulatedAnnealing loop
├── view/
│   ├── temp_view.py         # Quick single-image viewer
│   └── outfit_viewer.py     # Matplotlib grid of full outfit
├── init_dataset.py          # Download dataset from Kaggle
└── main.py                  # Entry point: load → SA → visualize

cache/                       # Auto-generated, gitignored
├── embeddings.pt            # [N, 569] float32 tensor of all item embeddings
├── item_ids.json            # Ordered item IDs matching embedding rows
└── knn_graph.json           # {item_id: [neighbor_id, ...]} per slot

fashion_items/               # Downloaded dataset, gitignored
├── images/                  # {id}.jpg product photos
└── styles.csv               # Item metadata (colour, usage, season, etc.)
```
