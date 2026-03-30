import requests
from PIL import Image
from io import BytesIO
import json
from image_dominant_colors import get_most_dominant_colors
from tqdm import tqdm
from datasets import load_from_disk


def get_image_from_url(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def add_color_to_polyvore(file_path):
    
    ds = load_from_disk("polyvore_dataset/hf_images")
    image_lookup = dict(zip(ds["item_ID"], ds["image"]))
    
    with open(file_path) as f:
        data = json.load(f)

    for outfit in tqdm(data):
        
        set_id = outfit['set_id']
        
        for clothing_item in outfit["items"]:
            try:
                item_id = f"{set_id}_{clothing_item['index']}"
                image = image_lookup[item_id]
                colors = get_most_dominant_colors(image, 2)
                if colors is None or len(colors) < 2:
                    raise ValueError("Not enough colors found")
                c1, c2 = colors
                clothing_item["dominant_color"] = c1.tolist()
                clothing_item["secondary_color"] = c2.tolist()
            except Exception as e:
                print(f"Skipping item in outfit {clothing_item['name']}: {e}")

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
        
if __name__ == "__main__":
    add_color_to_polyvore("polyvore_dataset/valid_no_dup.json")