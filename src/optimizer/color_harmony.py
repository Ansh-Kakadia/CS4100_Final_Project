import colorsys
import numpy as np


def _rgb_to_hsv(rgb: list[int]) -> tuple[float, float, float]:
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)


def _circular_hue_distance(h1: float, h2: float) -> float:
    """Returns the smallest angular distance between two hues (both in [0, 1]) in degrees"""
    diff = abs(h1 - h2) * 360
    return min(diff, 360 - diff)


def _hue_score(hues: list[float], saturations: list[float]) -> float:
    """Score the hue spread of chromatic items (saturation >= 0.15).
    Returns a value in [0, 1] where 0 = harmonious, 1 = clashing."""
    chromatic_hues = [h for h, s in zip(hues, saturations) if s >= 0.15]

    if len(chromatic_hues) <= 1:
        return 0.0  # neutrals or single chromatic item = good thing

    pairs = [
        _circular_hue_distance(chromatic_hues[i], chromatic_hues[j])
        for i in range(len(chromatic_hues))
        for j in range(i + 1, len(chromatic_hues))
    ]
    max_dist = max(pairs)

    if max_dist <= 30:
        return 0.0   # analogous — great
    if max_dist >= 150:
        return 0.1   # complementary — harder to style but still good
    if max_dist <= 60:
        return 0.3   # wide analogous — acceptable
    return max_dist / 180.0  # clashing too much


def _brightness_score(values: list[float]) -> float:
    """Penalizes outfits where all items are stuck in the mid-range with no contrast.
    All-dark and all-light outfits are valid style choices and score 0.
    Returns a value in [0, 1]."""
    if len(values) <= 1:
        return 0.0
    mean_v = float(np.mean(values))
    std_v = float(np.std(values))
    # If the outfit is consistently dark or consistently light, score 0 because monochrome is generally nice (all black, all white)
    if mean_v < 0.2 or mean_v > 0.8:
        return 0.0
    # In the mid-range, low contrast (low std) isn't as nice to look at
    return max(0.0, 1.0 - std_v / 0.3)


def score(colors: list[tuple[list[int], list[int]]]) -> float:
    """Score the color harmony of an outfit.

    Args: list of (dominant_color, secondary_color) pairs, one per item - each color is an RGB list e.g. [255, 128, 0].

    Returns a float in [0, 1]. Lower is better (0 = perfect harmony, 1 = clashing). """
   
    if not colors:
        return 0.0

    dominant_hsv = [_rgb_to_hsv(dom) for dom, _ in colors]
    hues =        [hsv[0] for hsv in dominant_hsv]
    saturations = [hsv[1] for hsv in dominant_hsv]
    values =      [hsv[2] for hsv in dominant_hsv]

    hue_s =        _hue_score(hues, saturations)
    brightness_s = _brightness_score(values)

    return 0.7 * hue_s + 0.3 * brightness_s


# --- quick testing ---
if __name__ == "__main__":
    outfits = {
        "Analogous warm browns (expect ~0.0)": [
            ([69, 69, 74],   [50, 50, 55]),   # dark grey
            ([13, 13, 13],   [10, 10, 10]),   # black
            ([15, 17, 23],   [10, 12, 18]),   # near-black
        ],
        "Warm beige analogous (expect ~0.0)": [
            ([227, 221, 208], [200, 195, 180]),
            ([206, 171, 151], [180, 150, 130]),
            ([171, 138, 109], [150, 120,  90]),
        ],
        "Yellow top + navy bottoms (expect ~0.1 complementary)": [
            ([241, 232, 157], [220, 210, 140]),  # yellow
            ([30,  72,  114], [25,  60, 100]),   # navy
            ([42,  62,   97], [35,  55,  85]),   # dark blue
        ],
        "Random clashing (expect high)": [
            ([255,   0,   0], [200,   0,   0]),  # red
            ([0,   255,   0], [0,   200,   0]),  # green
            ([0,     0, 255], [0,     0, 200]),  # blue
        ],
    }

    for name, colors in outfits.items():
        s = score(colors)
        print(f"{name}")
        print(f"  score = {s:.3f}\n")
