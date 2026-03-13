from PIL import Image
from rembg import remove
import numpy as np
from sklearn.cluster import KMeans


def get_most_dominant_colors(image_id: str, k : int):
    '''returns the top k dominant colors of the article of clothing using k-means clustering''' 
    img_path = "./fashion_items/images/" + image_id + ".jpg"
    
    image = Image.open(img_path)
    image_bg_removed = remove(image)
    
    rgba_pixels = np.array(image_bg_removed)
    print(rgba_pixels)
    filter_transparant = rgba_pixels[:,:,3] > 128
    rgb_pixels = rgba_pixels[filter_transparant][:,:3]
    
    kmeans = KMeans(k, n_init=10)
    kmeans.fit(rgb_pixels)
    counts = np.bincount(kmeans.labels_)
    sorted_colors = kmeans.cluster_centers_[np.argsort(-counts)]
    return sorted_colors.astype(int)
    

#Unit test for an item
def test():
    result = get_most_dominant_colors("1556", 4)
    for i, color in enumerate(result):
        r, g, b = color
        swatch = f"\033[48;2;{r};{g};{b}m     \033[0m"  # colored block
        print(f"Color {i+1}: {swatch}  RGB({r}, {g}, {b})")

if __name__ == "__main__":   
    test()