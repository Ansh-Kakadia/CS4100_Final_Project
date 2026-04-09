import json
import os

_MAPPING_PATH = os.path.join(os.path.dirname(__file__), "slot_mapping.json")

with open(_MAPPING_PATH) as f:
    _mapping = json.load(f)

_kaggle_to_polyvore: dict[str, list[int]] = _mapping["kaggle_to_polyvore"]
_polyvore_to_kaggle: dict[str, str] = _mapping["polyvore_to_kaggle"]


def get_polyvore_ids(kaggle_subcategory: str) -> list[int]:
    """
    Returns the Polyvore category IDs that correspond to a Kaggle subCategory.
    Used to find Polyvore outfit blueprints containing the user's item type.
    Returns an empty list if no mapping exists.
    """
    return _kaggle_to_polyvore.get(kaggle_subcategory, [])


def get_kaggle_subcategory(polyvore_category_id: int) -> str | None:
    """
    Returns the Kaggle subCategory that best matches a Polyvore category ID.
    Used to fill outfit slots with Kaggle items.
    Returns None if the Polyvore category has no Kaggle equivalent.
    """
    return _polyvore_to_kaggle.get(str(polyvore_category_id))


def get_fillable_slots(outfit_items: list[dict], anchor_category_id: int) -> list[dict]:
    """
    Given a list of Polyvore outfit items and the anchor's Polyvore category ID,
    returns the non-anchor slots that can be filled with Kaggle items.

    Each returned dict has:
      - polyvore_category_id: int
      - kaggle_subcategory: str
    """
    slots = []
    for item in outfit_items:
        cat_id = item.get("categoryid")
        if cat_id is None or cat_id == anchor_category_id:
            continue
        kaggle_sub = get_kaggle_subcategory(cat_id)
        if kaggle_sub is not None:
            slots.append({
                "polyvore_category_id": cat_id,
                "kaggle_subcategory": kaggle_sub,
            })
    return slots


def find_matching_outfits(outfits: list[dict], kaggle_subcategory: str) -> list[dict]:
    """
    Filters a list of Polyvore outfits to those containing at least one item
    whose category maps to the given Kaggle subCategory.

    Returns a list of (outfit, matched_polyvore_category_id) tuples.
    """
    polyvore_ids = set(get_polyvore_ids(kaggle_subcategory))
    if not polyvore_ids:
        return []

    results = []
    for outfit in outfits:
        for item in outfit.get("items", []):
            cat_id = item.get("categoryid")
            if cat_id in polyvore_ids:
                results.append((outfit, cat_id))
                break
    return results
