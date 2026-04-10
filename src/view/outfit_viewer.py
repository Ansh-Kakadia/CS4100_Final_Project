import os
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from src.data.item import FashionItem


def show_outfit(
    outfit: dict[str, FashionItem],
    images_dir: str,
    color_lookup: dict[int, tuple[list[int], list[int]]] | None = None,
    title: str = "Outfit",
) -> None:
    """
    Display a grid of outfit items using their product images.
    Falls back to a colored swatch (dominant color) when no image is available.
    """
    slots = list(outfit.keys())
    n = len(slots)
    cols = min(n, 4)
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3.5))
    fig.suptitle(title, fontsize=14, fontweight="bold")

    # Normalize axes to a flat list
    if n == 1:
        axes_flat = [axes]
    elif rows == 1:
        axes_flat = list(axes)
    else:
        axes_flat = list(np.array(axes).flatten())

    for idx, slot in enumerate(slots):
        ax = axes_flat[idx]
        item = outfit[slot]
        img_path = os.path.join(images_dir, f"{item.item_id}.jpg")

        if os.path.exists(img_path):
            try:
                img = Image.open(img_path).convert("RGB")
                ax.imshow(img)
                ax.axis("off")
            except Exception:
                _draw_swatch(ax, item, color_lookup)
        else:
            _draw_swatch(ax, item, color_lookup)

        label = f"{slot}\n{item.display_name[:28]}"
        if len(item.display_name) > 28:
            label += "…"
        label += f"\n{item.usage} · {item.season}"
        ax.set_title(label, fontsize=7, pad=3)

    # Hide unused axes
    for idx in range(n, len(axes_flat)):
        axes_flat[idx].axis("off")

    plt.tight_layout()
    plt.show()


def compare_outfits(
    before: dict[str, FashionItem],
    after: dict[str, FashionItem],
    images_dir: str,
    color_lookup: dict[int, tuple[list[int], list[int]]] | None = None,
) -> None:
    """
    Side-by-side comparison of two outfits (e.g. before/after optimization).
    Rows: top = before, bottom = after.
    """
    slots = list(after.keys())
    n = len(slots)
    fig, axes = plt.subplots(2, n, figsize=(n * 3, 7))
    fig.suptitle("Before (top) → After optimization (bottom)", fontsize=13, fontweight="bold")

    for col, slot in enumerate(slots):
        for row, outfit_dict in enumerate([before, after]):
            ax = axes[row][col] if n > 1 else axes[row]
            item = outfit_dict.get(slot)
            if item is None:
                ax.axis("off")
                continue

            img_path = os.path.join(images_dir, f"{item.item_id}.jpg")
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path).convert("RGB")
                    ax.imshow(img)
                    ax.axis("off")
                except Exception:
                    _draw_swatch(ax, item, color_lookup)
            else:
                _draw_swatch(ax, item, color_lookup)

            label = f"{slot}\n{item.display_name[:22]}"
            ax.set_title(label, fontsize=7, pad=2)

    plt.tight_layout()
    plt.show()


def plot_energy_history(history: list[float]) -> None:
    """Plot the simulated annealing energy curve."""
    plt.figure(figsize=(8, 4))
    plt.plot(history, linewidth=1)
    plt.xlabel("Iteration")
    plt.ylabel("Energy (lower = better)")
    plt.title("Simulated Annealing — Energy History")
    plt.tight_layout()
    plt.show()


def _draw_swatch(
    ax,
    item: FashionItem,
    color_lookup: dict[int, tuple[list[int], list[int]]] | None,
) -> None:
    """Draw a colored rectangle swatch as a fallback when no image is available."""
    dom_rgb = [179, 179, 179]  # default grey

    if color_lookup and item.item_id in color_lookup:
        dom_rgb = color_lookup[item.item_id][0]

    face_color = (dom_rgb[0] / 255.0, dom_rgb[1] / 255.0, dom_rgb[2] / 255.0)
    text_color = "white" if sum(dom_rgb) < 382 else "black"

    ax.set_facecolor(face_color)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.5, 0.5,
        item.article_type,
        ha="center", va="center",
        fontsize=8,
        color=text_color,
    )
