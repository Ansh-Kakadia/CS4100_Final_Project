import requests
from PIL import Image
from io import BytesIO
import json
from image_dominant_colors import get_most_dominant_colors
from tqdm import tqdm


def get_image_from_url(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def add_color_to_polyvore(file_path):
    with open(file_path) as f:
        data = json.load(f)

    for outfit in tqdm(data):
        for clothing_item in outfit["items"]:
            try:
                image = get_image_from_url(clothing_item["image"])
                c1, c2 = get_most_dominant_colors(image, 2)
                clothing_item["dominant_color"] = c1.tolist()
                clothing_item["secondary_color"] = c2.tolist()
            except Exception as e:
                print(f"Skipping item in outfit {clothing_item['name']}: {e}")

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
if __name__ == "__main__":
    add_color_to_polyvore("polyvore_dataset/valid_no_dup.json")