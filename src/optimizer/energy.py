from src.data.item import FashionItem
from src.optimizer import color_harmony


# TODO: decide with teammates whether dominant_color/secondary_color get added to
# FashionItem or passed in as a separate color lookup dict: {item_id: (dominant, secondary)}
COLOR_LOOKUP: dict[int, tuple[list[int], list[int]]] = {}


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
    # TODO: replace COLOR_LOOKUP with however teammates expose color data
    colors = [
        COLOR_LOOKUP[item.item_id]
        for item in items
        if item.item_id in COLOR_LOOKUP
    ]
    return color_harmony.score(colors)


def _usage_coherence(items: list[FashionItem]) -> float:
    # TODO: implement — map item.usage → formality score, return std deviation
    pass


def _season_coherence(items: list[FashionItem]) -> float:
    # TODO: implement — map item.season → angle, return circular variance
    pass
