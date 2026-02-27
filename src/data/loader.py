import os
import pandas as pd
from .item import FashionItem

MIN_SLOT_SIZE = 50


class FashionDataset:
    def __init__(self, csv_path: str, images_dir: str, gender: str = None):
        df = pd.read_csv(csv_path, on_bad_lines="skip")

        # Keep only rows whose image exists on disk
        df = df[df["id"].apply(
            lambda x: os.path.exists(os.path.join(images_dir, f"{x}.jpg"))
        )]

        # Optional gender filter
        if gender:
            df = df[df["gender"] == gender]

        # Drop rows missing critical fields
        df = df.dropna(subset=["subCategory", "masterCategory"])

        self.images_dir = images_dir

        # Build item list
        self.items: list[FashionItem] = []
        for _, row in df.iterrows():
            self.items.append(FashionItem(
                item_id=int(row["id"]),
                gender=str(row.get("gender", "")),
                master_category=str(row.get("masterCategory", "")),
                sub_category=str(row.get("subCategory", "")),
                article_type=str(row.get("articleType", "")),
                base_colour=str(row.get("baseColour", "")),
                season=str(row.get("season", "")),
                year=int(row["year"]) if pd.notna(row.get("year")) else 0,
                usage=str(row.get("usage", "")),
                display_name=str(row.get("productDisplayName", "")),
            ))

        # Index by slot (subCategory)
        self.by_slot: dict[str, list[FashionItem]] = {}
        for item in self.items:
            self.by_slot.setdefault(item.sub_category, []).append(item)

        # Filter out slots that are too small
        self.by_slot = {
            slot: items
            for slot, items in self.by_slot.items()
            if len(items) >= MIN_SLOT_SIZE
        }

        # Flat lookup maps
        self.id_to_item: dict[int, FashionItem] = {
            item.item_id: item for item in self.items
        }
        # id_to_index maps item_id → row index in the embedding matrix (set later)
        self.id_to_index: dict[int, int] = {}

    def get_slots(self) -> list[str]:
        return sorted(self.by_slot.keys())

    def print_slot_summary(self):
        print(f"{'Slot':<25} {'Count':>6}")
        print("-" * 33)
        for slot in sorted(self.by_slot, key=lambda s: -len(self.by_slot[s])):
            print(f"{slot:<25} {len(self.by_slot[slot]):>6}")
        print(f"\nTotal items (in valid slots): {sum(len(v) for v in self.by_slot.values())}")
