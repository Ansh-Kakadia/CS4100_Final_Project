import json
import os

DATASET_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DATASET_DIR, "category_id_map.json")) as f:
    category_map = json.load(f)

FILES = [
    "train_no_dup.json",
    "valid_no_dup.json",
    "valid_no_dup_cleaned.json",
    "test_no_dup.json",
]

for filename in FILES:
    path = os.path.join(DATASET_DIR, filename)
    if not os.path.exists(path):
        print(f"Skipping {filename} (not found)")
        continue

    with open(path) as f:
        data = json.load(f)

    missing_ids = set()
    for outfit in data:
        for item in outfit.get("items", []):
            cid = str(item.get("categoryid"))
            item["category"] = category_map.get(cid, f"Unknown ({cid})")
            if cid not in category_map:
                missing_ids.add(cid)

    out_path = path.replace(".json", "_with_categories.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Wrote {out_path}")
    if missing_ids:
        print(f"  Warning: unmapped category IDs: {sorted(missing_ids, key=int)}")
