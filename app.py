import math
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from src.data.loader import FashionDataset
from src.main import (
    KAGGLE_CSV,
    KAGGLE_IMAGES,
    POLYVORE_JSON,
    KAGGLE_COLOR_JSON,
    KNN_GRAPH_JSON,
    load_polyvore_outfits,
    get_anchor_item,
)
from src.matching.outfit_finder import find_best_outfit
from src.matching.slot_filler import fill_slots, load_color_lookup
from src.optimizer.algorithm import run as optimize_outfit
from src.optimizer.energy import set_color_lookup
from src.optimizer.neighbor import NeighborFinder
from src.optimizer import energy

'''
Run this app with: streamlit run app.py
'''

st.set_page_config(
    page_title="Outfit Optimization Demo",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        .small-note {
            color: #9ca3af;
            font-size: 0.92rem;
        }
        .changed-label {
            font-weight: 600;
            color: #93c5fd;
            margin-top: 0.4rem;
            margin-bottom: 0.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_resources_cached():
    dataset = FashionDataset(
        csv_path=str(KAGGLE_CSV),
        images_dir=str(KAGGLE_IMAGES),
    )
    polyvore_outfits = load_polyvore_outfits(POLYVORE_JSON)
    color_lookup = load_color_lookup(str(KAGGLE_COLOR_JSON))
    finder = NeighborFinder(str(KNN_GRAPH_JSON), dataset.id_to_item)
    return dataset, polyvore_outfits, color_lookup, finder


def get_image_path(item_id: int) -> Optional[Path]:
    base = Path(KAGGLE_IMAGES)
    for ext in ["jpg", "jpeg", "png", "webp"]:
        candidate = base / f"{item_id}.{ext}"
        if candidate.exists():
            return candidate
    return None


def energy_breakdown(outfit: dict) -> dict[str, float]:
    items = list(outfit.values())
    return {
        "total": float(energy.compute(outfit)),
        "color": float(energy._color_harmony(items)),
        "usage": float(energy._usage_coherence(items)),
        "season": float(energy._season_coherence(items)),
    }


def pct_improvement(initial_value: float, final_value: float) -> float:
    if math.isclose(initial_value, 0.0):
        return 0.0
    return ((initial_value - final_value) / initial_value) * 100.0


def run_pipeline_without_plots(item_id: int):
    dataset, polyvore_outfits, color_lookup, finder = load_resources_cached()
    set_color_lookup(color_lookup)

    anchor_item = get_anchor_item(dataset, item_id)
    match = find_best_outfit(polyvore_outfits, anchor_item, color_lookup)
    if match is None:
        raise ValueError(
            f"No matching Polyvore outfit found for subcategory '{anchor_item.sub_category}'."
        )

    best_template, anchor_category_id = match
    initial_outfit = fill_slots(
        polyvore_outfit=best_template,
        anchor_item=anchor_item,
        anchor_category_id=anchor_category_id,
        dataset=dataset,
        color_lookup=color_lookup,
    )

    optimized_outfit, history = optimize_outfit(
        initial_outfit,
        finder,
        locked_id=anchor_item.item_id,
    )

    return {
        "anchor_item": anchor_item,
        "anchor_category_id": anchor_category_id,
        "polyvore_template": best_template,
        "initial_outfit": initial_outfit,
        "optimized_outfit": optimized_outfit,
        "history": history,
    }


def render_item_card(item, slot_name: str, changed: bool = False):
    image_path = get_image_path(item.item_id)

    if changed:
        with st.container(border=True):
            if image_path is not None:
                st.image(str(image_path), use_container_width=True)
            else:
                st.markdown("<div class='small-note'>Image not found</div>", unsafe_allow_html=True)

            st.markdown("<div class='changed-label'>Changed</div>", unsafe_allow_html=True)
            st.markdown(f"**{item.display_name}**")
            st.caption(f"{slot_name} • {item.base_colour}")
    else:
        if image_path is not None:
            st.image(str(image_path), use_container_width=True)
        else:
            st.markdown("<div class='small-note'>Image not found</div>", unsafe_allow_html=True)

        st.markdown(f"**{item.display_name}**")
        st.caption(f"{slot_name} • {item.base_colour}")


def render_outfit_grid(outfit: dict, changed_slots: set[str], optimized: bool = False):
    slots = list(outfit.keys())
    for row_start in range(0, len(slots), 3):
        row_slots = slots[row_start: row_start + 3]
        cols = st.columns(len(row_slots))
        for col, slot in zip(cols, row_slots):
            with col:
                changed = optimized and slot in changed_slots
                render_item_card(outfit[slot], slot_name=slot, changed=changed)


def build_breakdown_table(initial_scores: dict[str, float], final_scores: dict[str, float]) -> pd.DataFrame:
    rows = []
    for key, label in [
        ("total", "Total energy"),
        ("color", "Color harmony"),
        ("usage", "Usage coherence"),
        ("season", "Season coherence"),
    ]:
        rows.append(
            {
                "Metric": label,
                "Initial": round(initial_scores[key], 4),
                "Optimized": round(final_scores[key], 4),
                "Change": round(final_scores[key] - initial_scores[key], 4),
            }
        )
    return pd.DataFrame(rows)


def build_item_options(dataset: FashionDataset, limit: int = 200):
    options = []

    for item_id, item in dataset.id_to_item.items():
        image_path = get_image_path(item_id)
        if image_path is None:
            continue

        label = f"{item.display_name} (ID: {item_id})"
        options.append((label, item_id))

        if len(options) >= limit:
            break

    return options


st.title("Outfit Optimization Demo")
st.write(
    "Choose an anchor item to generate an initial outfit and compare it with the optimized result."
)

with st.expander("What the optimization score measures"):
    st.markdown(
        """
- **Color harmony (50%)**
- **Usage coherence (30%)**
- **Season coherence (20%)**

The optimized outfit is the one with a lower energy score under this objective function.
That does not always guarantee that it looks better to a human viewer.
        """
    )

dataset, _, _, _ = load_resources_cached()
item_options = build_item_options(dataset)

selected_label = st.selectbox(
    "Choose an anchor item",
    options=[label for label, _ in item_options],
)

selected_id_int = next(item_id for label, item_id in item_options if label == selected_label)

run_clicked = st.button("Run demo", type="primary")

if run_clicked:
    try:
        with st.spinner("Running pipeline and optimizing outfit..."):
            result = run_pipeline_without_plots(selected_id_int)

        anchor_item = result["anchor_item"]
        initial_outfit = result["initial_outfit"]
        optimized_outfit = result["optimized_outfit"]
        history = result["history"]

        changed_slots = {
            slot
            for slot in initial_outfit
            if initial_outfit[slot].item_id != optimized_outfit[slot].item_id
        }

        initial_scores = energy_breakdown(initial_outfit)
        final_scores = energy_breakdown(optimized_outfit)
        improvement = pct_improvement(initial_scores["total"], final_scores["total"])

        st.markdown("---")
        st.markdown("## Anchor item")

        anchor_cols = st.columns([0.7, 2.3])

        with anchor_cols[0]:
            anchor_path = get_image_path(anchor_item.item_id)
            if anchor_path is not None:
                st.image(str(anchor_path), width=220)

        with anchor_cols[1]:
            st.markdown(f"### {anchor_item.display_name}")
            st.write(
                f"ID {anchor_item.item_id} • "
                f"{anchor_item.sub_category} • "
                f"{anchor_item.base_colour} • "
                f"{anchor_item.usage}"
            )

        metric_cols = st.columns(3)
        metric_cols[0].metric("Initial energy", f"{initial_scores['total']:.4f}")
        metric_cols[1].metric("Final energy", f"{final_scores['total']:.4f}")
        metric_cols[2].metric("Items changed", str(len(changed_slots)))
        st.caption(f"Energy improvement: {improvement:.1f}%")

        st.markdown("---")
        st.markdown("## Outfit comparison")
        st.caption("Items labeled 'Changed' were replaced during optimization.")

        compare_cols = st.columns(2)

        with compare_cols[0]:
            st.markdown("### Initial outfit")
            render_outfit_grid(initial_outfit, changed_slots, optimized=False)

        with compare_cols[1]:
            st.markdown("### Optimized outfit")
            render_outfit_grid(optimized_outfit, changed_slots, optimized=True)

        st.markdown("## Changes made by the optimizer")

        if changed_slots:
            for slot in sorted(changed_slots):
                before_item = initial_outfit[slot]
                after_item = optimized_outfit[slot]
                st.markdown(
                    f"- **{slot}**: {before_item.display_name} → {after_item.display_name}"
                )
        else:
            st.write("No items were changed in this run.")

        st.markdown("## Simulated Annealing Energy History")
        st.line_chart(history)
        st.caption("Energy history across simulated annealing iterations.")

        st.markdown("## Score breakdown")
        st.dataframe(
            build_breakdown_table(initial_scores, final_scores),
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "Lower energy means the outfit is better under the model's objective function. "
            "That may reflect stronger color, usage, or season coherence even when the visual improvement is not dramatic."
        )

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Something went wrong while running the demo: {e}")