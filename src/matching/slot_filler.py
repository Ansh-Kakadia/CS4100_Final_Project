import json
import numpy as np

from src.data.item import FashionItem
from src.data.loader import FashionDataset
from src.data.slot_mapper import get_fillable_slots


def _cosine_sim(a: list[int], b: list[int]) -> float:
    arr_a = np.array(a, dtype=np.float32)
    arr_b = np.array(b, dtype=np.float32)
    denom = np.linalg.norm(arr_a) * np.linalg.norm(arr_b)
    
    return 0.0 if denom == 0 else float(np.dot(arr_a, arr_b) / denom)


def load_color_lookup(styles_json_path: str) -> dict[int, tuple[list[int], list[int]]]:
    """
    Loads dominant/secondary color data for all Kaggle items.
    Returns {item_id: (dominant_color, secondary_color)}.
    Items without color data are excluded.
    """
    with open(styles_json_path) as f:
        data = json.load(f)

    lookup: dict[int, tuple[list[int], list[int]]] = {}
    for row in data:
        if row.get("dominant_color") and row.get("secondary_color"):
            try:
                lookup[int(row["id"])] = (row["dominant_color"], row["secondary_color"])
            except (KeyError, ValueError):
                pass
    return lookup


def fill_slots(
    polyvore_outfit: dict,
    anchor_item: FashionItem,
    anchor_category_id: int,
    dataset: FashionDataset,
    color_lookup: dict[int, tuple[list[int], list[int]]],
) -> dict[str, FashionItem]:
    """
    Given a Polyvore outfit template and a locked anchor Kaggle item, fills every
    other slot with the Kaggle item whose dominant color best matches the
    corresponding Polyvore item's dominant color.

    Returns a dict mapping kaggle_subcategory to FashionItem, including the anchor.
    """
    outfit: dict[str, FashionItem] = {}

    
    outfit[anchor_item.sub_category] = anchor_item

    fillable = get_fillable_slots(polyvore_outfit["items"], anchor_category_id)

    for slot in fillable:
        polyvore_cat_id: int = slot["polyvore_category_id"]
        kaggle_sub: str = slot["kaggle_subcategory"]

        # Find the reference Polyvore item so we can match its color
        reference_color: list[int] | None = None
        for pv_item in polyvore_outfit["items"]:
            if pv_item.get("categoryid") == polyvore_cat_id:
                reference_color = pv_item.get("dominant_color")
                break

        candidates: list[FashionItem] = dataset.by_slot.get(kaggle_sub, [])
        if not candidates:
            continue

        if reference_color is None:
            # pick the first candidate
            outfit[kaggle_sub] = candidates[0]
            continue

        best_item = max(
            (c for c in candidates if c.item_id in color_lookup),
            key=lambda c: _cosine_sim(color_lookup[c.item_id][0], reference_color),
            default=None,
        )

        if best_item is None:
            # pick the first candidate
            outfit[kaggle_sub] = candidates[0]
        else:
            outfit[kaggle_sub] = best_item

    return outfit
