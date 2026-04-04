# TODO

## Step 1: `src/data/polyvore_category_map.py`
Hardcoded dict mapping Polyvore `categoryid` → Kaggle `subCategory`. This is the bridge between the two datasets — without it, the outfit finder has no way to know that categoryid `27` (jeans) maps to Kaggle's `Bottomwear`. Also needs the reverse mapping (Kaggle `subCategory` → set of Polyvore categoryids) for the outfit finder.

## Step 2: `src/matching/outfit_finder.py`
Given a Kaggle item ID:
- Map its `subCategory` → set of Polyvore categoryids
- Filter the 1,497 Polyvore outfits to those containing an item in that category
- Score each by cosine similarity between that outfit's matching item color and the input item's color
- Return the top matching Polyvore outfit as the template

## Step 3: `src/matching/slot_filler.py`
Given the chosen Polyvore template and the user's input item:
- Lock the user's item into its slot
- For each other Polyvore item in the outfit, map its `categoryid` → Kaggle `subCategory`, then find the nearest Kaggle item by color cosine similarity within that subCategory
- Return a complete Kaggle outfit dict ready for the optimizer

## Step 4: `src/optimizer/color_harmony.py`, `energy.py`, `neighbor.py`, `sa.py`

### `src/optimizer/color_harmony.py`
Scores how well the colors in an outfit work together. Takes a list of `(dominant_color, secondary_color)` RGB tuples (one per item) and returns a float in [0, 1] where 0 = perfect harmony, 1 = clashing.

Algorithm (all in HSV space):
1. Convert each `dominant_color` RGB → HSV
2. Separate neutrals (saturation < 0.15) from chromatic items
3. For chromatic items, compute all pairwise circular hue distances (0°–180°)
4. Match against harmony patterns:
   - All neutrals → 0.0 (perfect)
   - Max hue distance ≤ 30° → 0.0 (analogous, e.g. all warm browns)
   - All distances ≥ 150° → 0.1 (complementary, e.g. navy + orange)
   - Max hue distance ≤ 60° → 0.3 (wide analogous, acceptable)
   - Otherwise → `max_distance / 180.0` (penalty scales with clash)
5. Secondary term: brightness contrast — std deviation of V values across items,
   want moderate contrast (not all dark, not all light). Score: `abs(std_V - 0.3) / 0.3`
6. Final: `0.7 * hue_score + 0.3 * brightness_score`

### `src/optimizer/energy.py`
Combines scoring terms into a single outfit energy value (lower = better):
- Color harmony (0.5 weight) — calls `color_harmony.py`
- Usage coherence (0.3 weight) — std deviation of formality scores across items
  (Formal=1.0, Smart Casual=0.75, Casual=0.5, Sports=0.1, etc.)
- Season coherence (0.2 weight) — circular variance of season angles
  (Spring=0°, Summer=90°, Fall=180°, Winter=270°)

### `src/optimizer/neighbor.py`
Proposes a new outfit by swapping one slot's item with a color-similar Kaggle neighbor.

### `src/optimizer/sa.py`
Standard SA loop, takes the filled outfit as starting point, returns `(best_outfit, energy_history)`.

## Step 5: `src/view/outfit_viewer.py` + `src/main.py`
- `outfit_viewer.py`: Matplotlib grid showing each slot — image if available, colored swatch fallback using `dominant_color`
- `main.py`: entry point that takes a Kaggle item ID, runs the full pipeline, and displays Polyvore template → Kaggle substitution → optimized result
