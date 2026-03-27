import json
import numpy as np

from src.data.item import FashionItem


class DataEncoder:
    def __init__(self):
        self.colour_vocab: list[str] = []
        self.season_vocab: list[str] = []
        self.usage_vocab: list[str] = []
        self.output_dim: int = 0

    def fit(self, items: list[FashionItem]) -> "DataEncoder":
        self.colour_vocab = sorted({item.base_colour for item in items if item.base_colour})
        self.season_vocab = sorted({item.season for item in items if item.season})
        self.usage_vocab = sorted({item.usage for item in items if item.usage})
        self.output_dim = len(self.colour_vocab) + len(self.season_vocab) + len(self.usage_vocab)
        return self

    def encode(self, item: FashionItem) -> np.ndarray:
        vec = np.zeros(self.output_dim, dtype=np.float32)
        offset = 0

        if item.base_colour in self.colour_vocab:
            vec[offset + self.colour_vocab.index(item.base_colour)] = 1.0
        offset += len(self.colour_vocab)

        if item.season in self.season_vocab:
            vec[offset + self.season_vocab.index(item.season)] = 1.0
        offset += len(self.season_vocab)

        if item.usage in self.usage_vocab:
            vec[offset + self.usage_vocab.index(item.usage)] = 1.0

        return vec

    def encode_batch(self, items: list[FashionItem]) -> np.ndarray:
        results = np.zeros((len(items), self.output_dim), dtype=np.float32)
        colour_index = {c: i for i, c in enumerate(self.colour_vocab)}
        season_index = {s: i for i, s in enumerate(self.season_vocab)}
        usage_index = {u: i for i, u in enumerate(self.usage_vocab)}
        colour_offset = 0
        season_offset = len(self.colour_vocab)
        usage_offset = season_offset + len(self.season_vocab)

        for i, item in enumerate(items):
            if item.base_colour in colour_index:
                results[i, colour_offset + colour_index[item.base_colour]] = 1.0
            if item.season in season_index:
                results[i, season_offset + season_index[item.season]] = 1.0
            if item.usage in usage_index:
                results[i, usage_offset + usage_index[item.usage]] = 1.0

        return results

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump({
                "colours": self.colour_vocab,
                "seasons": self.season_vocab,
                "usages": self.usage_vocab,
            }, f, indent=2)

    @classmethod
    def load(cls, path: str) -> "DataEncoder":
        with open(path) as f:
            data = json.load(f)
        encoder = cls()
        encoder.colour_vocab = data["colours"]
        encoder.season_vocab = data["seasons"]
        encoder.usage_vocab = data["usages"]
        encoder.output_dim = len(encoder.colour_vocab) + len(encoder.season_vocab) + len(encoder.usage_vocab)
        return encoder
