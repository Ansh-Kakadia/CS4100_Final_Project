import requests
from PIL import Image
from io import BytesIO
import json
import csv
from image_dominant_colors import get_most_dominant_colors
from tqdm import tqdm
from datasets import load_from_disk


def get_image_from_url(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

REDUCED_SIZE = (100,100)

def add_color_to_kaggle(csv_file_path, json_file_path):
    
    with open(csv_file_path, 'r') as f:
        data = list(csv.DictReader(f))
        

    for clothing_item in tqdm(data):
        
        try:
            img_path = "./fashion_items/images/" + clothing_item['id'] + ".jpg"
            image = Image.open(img_path)
            image.thumbnail(REDUCED_SIZE)
            c1,c2 = get_most_dominant_colors(image, 2)
            clothing_item["dominant_color"] = c1.tolist()
            clothing_item["secondary_color"] = c2.tolist()
        except Exception as e: 
            print(f'Skipping item: {clothing_item['id']} {e}')
        
        

    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=2)
        
if __name__ == "__main__":
    add_color_to_kaggle("fashion_items/styles.csv", "fashion_items/styles.json")