import numpy as np

from src.data.item import FashionItem
from src.data.slot_mapper import find_matching_outfits


def _cosine_sim(a: list[int], b: list[int]) -> float:
    arr_a = np.array(a, dtype=np.float32)
    arr_b = np.array(b, dtype=np.float32)
    denom = np.linalg.norm(arr_a) * np.linalg.norm(arr_b)
    return 0.0 if denom == 0 else float(np.dot(arr_a, arr_b) / denom)


def find_best_outfit(
    polyvore_outfits: list[dict],
    anchor_item: FashionItem,
    color_lookup: dict[int, tuple[list[int], list[int]]],
) -> tuple[dict, int] | None:
    """
    Given a list of Polyvore outfits and a Kaggle anchor item, finds the outfit
    whose anchor slot most closely matches the anchor item's dominant color.

    Returns (outfit, matched_polyvore_category_id) or None if no match found.
    """
    candidates = find_matching_outfits(polyvore_outfits, anchor_item.sub_category)
    if not candidates:
        return None

    anchor_color = color_lookup.get(anchor_item.item_id)
    if anchor_color is None:
        # No color data for anchor — just return the first matching outfit
        return candidates[0]

    best_outfit, best_cat_id = None, None
    best_score = -1.0

    for outfit, cat_id in candidates:
        # Find the Polyvore item in this outfit that maps to our anchor slot
        for pv_item in outfit.get("items", []):
            if pv_item.get("categoryid") == cat_id:
                ref_color = pv_item.get("dominant_color")
                if ref_color is not None:
                    sim = _cosine_sim(anchor_color[0], ref_color)
                    if sim > best_score:
                        best_score = sim
                        best_outfit = outfit
                        best_cat_id = cat_id
                break

    # Fall back to first candidate if no Polyvore item had color data
    if best_outfit is None:
        return candidates[0]

    return best_outfit, best_cat_id
