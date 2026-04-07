"""
filter_styles.py
----------------
Reproducible pipeline that takes the raw Kaggle styles.csv and produces
styles_filtered.csv used throughout the project.

Run from the project root:
    python data_cleansing/filter_styles.py
"""

import pandas as pd

INPUT_PATH  = "fashion_items/styles.csv"
OUTPUT_PATH = "fashion_items/styles_filtered.csv"

# ── Step 1: Excluded master categories ────────────────────────────────────────
# These entire categories are outside the scope of a fashion outfit recommender.
EXCLUDED_MASTER_CATEGORIES = [
    "Personal Care",   # skincare, makeup, fragrance — not wearable fashion items
    "Free Items",      # promotional vouchers and free gifts — not real products
    "Home",            # home furnishings — unrelated to personal fashion
]

# ── Step 2: Excluded subcategories ────────────────────────────────────────────
# A small number of subcategories under otherwise-kept master categories are
# also non-wearable and were removed.
EXCLUDED_SUBCATEGORIES = [
    "Umbrellas",       # Accessories > Umbrellas    (6 items)  — not worn
    "Water Bottle",    # Accessories > Water Bottle (7 items)  — not worn
    "Perfumes",        # Accessories > Perfumes     (1 item)   — not worn
]


def filter_styles(input_path: str = INPUT_PATH, output_path: str = OUTPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path, on_bad_lines="skip")
    original_count = len(df)

    # Step 1 — drop excluded master categories
    mask_master = df["masterCategory"].isin(EXCLUDED_MASTER_CATEGORIES)
    n_master = int(mask_master.sum())
    df = df[~mask_master]

    # Step 2 — drop excluded subcategories
    mask_sub = df["subCategory"].isin(EXCLUDED_SUBCATEGORIES)
    n_sub = int(mask_sub.sum())
    df = df[~mask_sub]

    final_count = len(df)

    df.to_csv(output_path, index=False)

    print(f"Input  : {input_path}  ({original_count} rows)")
    print(f"Output : {output_path} ({final_count} rows)")
    print(f"  Removed by master category filter : {n_master}")
    print(f"  Removed by subcategory filter     : {n_sub}")
    print(f"  Total removed                     : {original_count - final_count}")

    return df


if __name__ == "__main__":
    filter_styles()
