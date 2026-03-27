import os
from PIL import Image
from rembg import remove
import numpy as np
from sklearn.cluster import KMeans

def get_most_dominant_colors(image: Image.Image, k: int):
    '''returns the top k dominant colors of the given clothing image'''
    image_bg_removed = remove(image)
    
    rgba_pixels = np.array(image_bg_removed)
    filter_transparant = rgba_pixels[:,:,3] > 128
    rgb_pixels = rgba_pixels[filter_transparant][:,:3]
    
    kmeans = KMeans(k, n_init=10)
    kmeans.fit(rgb_pixels)
    counts = np.bincount(kmeans.labels_)
    sorted_colors = kmeans.cluster_centers_[np.argsort(-counts)]
    return sorted_colors.astype(int)



def get_most_dominant_colors_kaggle(image_id: str, k : int):
    '''returns the top k dominant colors of the article of clothing from 
    
    the kaggle dataset using k-means clustering''' 
    
    img_path = "./fashion_items/images/" + image_id + ".jpg"
    
    image = Image.open(img_path)
    
    return get_most_dominant_colors(image,k)
    
    

#Unit test for most_dominant_colors
def test_dom_colors():
    result = get_most_dominant_colors_kaggle("59925", 4)
    for i, color in enumerate(result):
        r, g, b = color
        swatch = f"\033[48;2;{r};{g};{b}m     \033[0m"  # colored block
        print(f"Color {i+1}: {swatch}  RGB({r}, {g}, {b})")

if __name__ == "__main__":   
    test_dom_colors()