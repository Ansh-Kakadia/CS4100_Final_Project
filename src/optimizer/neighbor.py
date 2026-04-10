import json
import random
from src.data.item import FashionItem

class NeighborFinder:
    def __init__(self, knn_graph_path: str, id_to_item: dict[int, FashionItem]):
        with open(knn_graph_path, "r") as f:
            self.knn_graph = dict[str, list[str]](json.load(f))
        self._id_to_item = id_to_item

    def get_neighbors(self, outfit: dict[str, FashionItem]) -> dict[str, FashionItem]:
        slot = random.choice(list(outfit.keys()))
        current =  outfit[slot]
        
        neighbors = self.knn_graph.get(str(current.item_id), [])
        if not neighbors:
            return outfit # no neighbors so we keep it the same
        
        candidate_items = []

        for nid in neighbors:
            nid_int = int(nid)
            if nid_int not in self._id_to_item:
                continue

            candidate = self._id_to_item[nid_int]

            # keep same subcategory
            if candidate.sub_category != current.sub_category:
                continue

            # keep same gender
            if candidate.gender != current.gender:
                continue

            candidate_items.append(candidate)
        
        if not candidate_items:
            return outfit # no valid replacements, keep the same outfit
        
        found_item = random.choice(candidate_items)
        return {**outfit, slot: found_item}
        