# Data Cleansing Log

## Source Dataset

**Kaggle: Fashion Product Images (Small)**
- Downloaded via `src/init_dataset.py` using `kagglehub`
- Raw file: `fashion_items/styles.csv`
- Raw size: **44,424 rows**, 10 columns

---

## Columns

| Column | Description |
|---|---|
| id | Unique item ID (matches image filename) |
| gender | Men / Women / Boys / Girls / Unisex |
| masterCategory | Top-level category |
| subCategory | Second-level category |
| articleType | Specific product type (e.g. Shirts, Jeans) |
| baseColour | Primary color label |
| season | Summer / Winter / Fall / Spring |
| year | Year of listing |
| usage | Casual / Formal / Sports / ... |
| productDisplayName | Full product name string |

---

## Filtering Steps (styles.csv → styles_filtered.csv)

Reproducible script: `data_cleansing/filter_styles.py`

### Step 1 — Remove excluded master categories

These master categories are outside the scope of a fashion outfit recommender (non-wearable or non-product entries):

| Master Category | Subcategories | Rows Removed | Reason |
|---|---|---|---|
| Personal Care | Fragrance, Lips, Nails, Makeup, Skin Care, Skin, Eyes, Hair, Bath and Body, Beauty Accessories, Perfumes | 2,403 | Not wearable fashion items |
| Free Items | Free Gifts, Vouchers | 105 | Promotional placeholders, not real products |
| Home | Home Furnishing | 1 | Unrelated to personal fashion |

### Step 2 — Remove excluded subcategories

A small number of subcategories under otherwise-kept master categories were also removed:

| Master Category | Subcategory | Rows Removed | Reason |
|---|---|---|---|
| Accessories | Umbrellas | 6 | Not a wearable fashion item |
| Accessories | Water Bottle | 7 | Not a wearable fashion item |
| Accessories | Perfumes | 1 | Not a wearable fashion item |

### Result

| | Count |
|---|---|
| Before filtering | 44,424 |
| Removed (master category) | 2,509 |
| Removed (subcategory) | 14 |
| **After filtering** | **41,901** |

---

## Remaining Categories

| Master Category | Subcategories |
|---|---|
| Apparel | Topwear, Bottomwear, Innerwear, Dress, Loungewear and Nightwear, Saree, Apparel Set, Socks |
| Footwear | Shoes, Sandal, Flip Flops |
| Accessories | Bags, Watches, Jewellery, Eyewear, Wallets, Belts, Socks, Headwear, Ties, Scarves, Gloves, Mufflers, Stoles, Cufflinks, Shoe Accessories, Sports Accessories, Accessories |
| Sporting Goods | Sports Equipment, Wristbands |

---

## Notes

- All removed items had valid image files on disk — this was a semantic filter, not a broken-data fix.
- Image validation (checking that `fashion_items/images/{id}.jpg` exists) is handled separately at load time in `src/data/loader.py`.
- The `loader.py` also applies a `MIN_SLOT_SIZE = 50` filter at runtime, dropping any subCategory slot with fewer than 50 items from the active dataset.
