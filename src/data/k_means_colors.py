import numpy as np
from PIL.Image import Image
import random





class KMeansColors:
    def __init__(self, n_clusters, n_init=1, max_iter=50):
        self.n_clusters = n_clusters
        self.tries = n_init
        self.max_iter = max_iter
        
    def fit(self, rgb_pixels):
        
        centroids = random.sample(rgb_pixels, self.n_clusters)
        
        for i in range(self.max_iter):
            