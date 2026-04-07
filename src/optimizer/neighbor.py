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
        
        candidate_ids = [
              int(nid) for nid in neighbors
              if int(nid) in self._id_to_item
          ] # random neighbor that exists in our item index
        if not candidate_ids:
            return outfit # no candidates so we keep it the same
        
        found_item = self._id_to_item[random.choice(candidate_ids)]
        return {**outfit, slot: found_item}
        