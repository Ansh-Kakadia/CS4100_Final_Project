""" 
using sklearn maybe?
using cosine as the metric instead of euclidean?
    it measures the angle between vectors (direction) rather than        
    magnitude since color vectors are normalized to [0,1] and metadata is one-hot, cosine tends to work      
    better here 
output indices is a (N, 20) array where each row is the 20 nearest neighbors for that item - save to cache/knn_graph.json
"""
import sklearn.neighbors
import numpy as np
import json
import os

from src.embeddings.embedder import ItemEmbedder

def build_knn(embeddings: np.ndarray, k: int = 20):
    """Builds a KNN graph for the given embeddings."""
    knn = sklearn.neighbors.NearestNeighbors(n_neighbors=k, metric="cosine")
    knn.fit(embeddings)
    return knn.kneighbors(embeddings, return_distance=False)