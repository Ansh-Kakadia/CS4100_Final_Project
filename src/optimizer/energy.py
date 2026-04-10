import math
import numpy as np

from src.data.item import FashionItem
from src.optimizer import color_harmony

COLOR_LOOKUP: dict[int, tuple[list[int], list[int]]] = {}


def set_color_lookup(lookup: dict[int, tuple[list[int], list[int]]]) -> None:
    """Populate the module-level color lookup used by energy scoring."""
    global COLOR_LOOKUP
    COLOR_LOOKUP = lookup


def compute(outfit: dict[str, FashionItem]) -> float:
    """Score an outfit. Lower is better (0 = perfect, 1 = worst).

    Args: outfit maps slot name → FashionItem

    Returns a loat in [0, 1].
    """
    items = list(outfit.values())

    color_score = _color_harmony(items)
    usage_score = _usage_coherence(items)
    season_score = _season_coherence(items)

    return 0.5 * color_score + 0.3 * usage_score + 0.2 * season_score


def _color_harmony(items: list[FashionItem]) -> float:
    colors = [
        COLOR_LOOKUP[item.item_id]
        for item in items
        if item.item_id in COLOR_LOOKUP
    ]
    return color_harmony.score(colors)


def _usage_coherence(items: list[FashionItem]) -> float:
    formality = {
        "Formal": 1.0,
        "Smart Casual": 0.8,
        "Ethnic": 0.7,
        "Casual": 0.5,
        "Travel": 0.3,
        "Home": 0.2,
        "Sports": 0.1,
    }
    scores = [formality[item.usage] for item in items if item.usage in formality]
    if len(scores) < 2:
        return 0.0
    return float(np.std(scores))


def _season_coherence(items: list[FashionItem]) -> float:
    angles = {
        "Spring": 0.0,
        "Summer": 90.0,
        "Fall": 180.0,
        "Winter": 270.0,
    }
    radians = [math.radians(angles[item.season]) for item in items if item.season in angles]
    if len(radians) < 2:
        return 0.0
    sin_mean = float(np.mean([math.sin(r) for r in radians]))
    cos_mean = float(np.mean([math.cos(r) for r in radians]))
    r = math.sqrt(sin_mean**2 + cos_mean**2)
    return 1.0 - r  # circular variance: 0 = all same season, 1 = maximally spread
