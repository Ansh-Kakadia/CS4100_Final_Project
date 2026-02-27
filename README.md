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

<<<<<<< HEAD
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
=======
## General Plan

We plan ao make an AI system that uses Sinulated Annealing (or other local search techniques) to create an outfit from a given article of clothing.

We are using this [Kaggle dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small/versions/1?resource=download). 

The system should be split into the following parts:
- A data cleaner, which organizes the data from the data set into a format the search and view can work with
- A search component, which first creates a random outfit with a given article of clothing, then locally searches the outfit space using some outfit huristic
- A view, which shows the initial and final products, and possibly some states in between

>>>>>>> 168523f6aff78d35b431e94c43a6061db17ee88c
