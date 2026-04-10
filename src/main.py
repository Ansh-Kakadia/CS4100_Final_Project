import argparse
import json
from pathlib import Path

from src.data.loader import FashionDataset
from src.matching.outfit_finder import find_best_outfit
from src.matching.slot_filler import fill_slots, load_color_lookup
from src.optimizer.algorithm import run
from src.optimizer.energy import set_color_lookup
from src.optimizer.neighbor import NeighborFinder
from src.view.outfit_viewer import show_outfit, compare_outfits, plot_energy_history
from src.optimizer import energy

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KAGGLE_CSV = PROJECT_ROOT / "fashion_items" / "styles.csv"
KAGGLE_IMAGES = PROJECT_ROOT / "fashion_items" / "images"
POLYVORE_JSON = PROJECT_ROOT / "polyvore_dataset" / "valid_no_dup_cleaned_with_categories.json"
KAGGLE_COLOR_JSON = PROJECT_ROOT / "fashion_items" / "styles.json"
KNN_GRAPH_JSON = PROJECT_ROOT / "cache" / "knn_graph.json"


def load_polyvore_outfits(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_resources():
    print("Loading dataset...")
    dataset = FashionDataset(
        csv_path=str(KAGGLE_CSV),
        images_dir=str(KAGGLE_IMAGES),
    )

    print("Loading Polyvore outfits...")
    polyvore_outfits = load_polyvore_outfits(POLYVORE_JSON)

    print("Loading Kaggle color lookup...")
    color_lookup = load_color_lookup(str(KAGGLE_COLOR_JSON))

    print("Loading KNN graph...")
    finder = NeighborFinder(str(KNN_GRAPH_JSON), dataset.id_to_item)

    return dataset, polyvore_outfits, color_lookup, finder


def get_anchor_item(dataset: FashionDataset, item_id: int):
    item = dataset.id_to_item.get(item_id)
    if item is None:
        raise ValueError(f"Item ID {item_id} was not found in the Kaggle dataset.")
    return item


def run_pipeline(item_id: int):
    dataset, polyvore_outfits, color_lookup, finder = load_resources()

    # Initialize optimizer color scoring
    set_color_lookup(color_lookup)

    anchor_item = get_anchor_item(dataset, item_id)
    print(f"Selected item: {anchor_item.display_name} (ID {anchor_item.item_id})")

    match = find_best_outfit(polyvore_outfits, anchor_item, color_lookup)
    if match is None:
        raise ValueError(
            f"No matching Polyvore outfit found for subcategory '{anchor_item.sub_category}'."
        )

    best_template, anchor_category_id = match
    print(f"Matched Polyvore anchor category: {anchor_category_id}")

    initial_outfit = fill_slots(
        polyvore_outfit=best_template,
        anchor_item=anchor_item,
        anchor_category_id=anchor_category_id,
        dataset=dataset,
        color_lookup=color_lookup,
    )
    print(f"Built initial outfit with {len(initial_outfit)} slots.")

    optimized_outfit, history = run(initial_outfit, finder)

    print("Optimization complete.")
    print("Initial:", {slot: item.item_id for slot, item in initial_outfit.items()})
    print("Optimized:", {slot: item.item_id for slot, item in optimized_outfit.items()})
    print("History length:", len(history))
    print("History first 10:", history[:10])

    print("Initial energy:", energy.compute(initial_outfit))
    print("Final energy:", energy.compute(optimized_outfit))

    show_outfit(
        initial_outfit,
        images_dir=str(KAGGLE_IMAGES),
        color_lookup=color_lookup,
        title="Initial Kaggle Outfit",
    )

    compare_outfits(
        initial_outfit,
        optimized_outfit,
        images_dir=str(KAGGLE_IMAGES),
        color_lookup=color_lookup,
    )

    show_outfit(
        optimized_outfit,
        images_dir=str(KAGGLE_IMAGES),
        color_lookup=color_lookup,
        title="Optimized Outfit",
    )

    plot_energy_history(history)

    return {
        "anchor_item": anchor_item,
        "polyvore_template": best_template,
        "anchor_category_id": anchor_category_id,
        "initial_outfit": initial_outfit,
        "optimized_outfit": optimized_outfit,
        "history": history,
    }


def main():
    parser = argparse.ArgumentParser(description="Run the outfit generation pipeline.")
    parser.add_argument("item_id", type=int, help="Kaggle item ID to use as the anchor item")
    args = parser.parse_args()

    run_pipeline(args.item_id)


if __name__ == "__main__":
    main()