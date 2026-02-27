from dataclasses import dataclass


@dataclass(frozen=True)
class FashionItem:
    item_id: int
    gender: str
    master_category: str
    sub_category: str
    article_type: str
    base_colour: str
    season: str
    year: int
    usage: str
    display_name: str
