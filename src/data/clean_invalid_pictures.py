import json

def clean_data_polyvore(json_path:str, new_path : str) -> None:
    
    with open(json_path) as f:
        data = json.load(f, )
    
    for outfit in data:
        outfit['items'] = [item for item in outfit['items'] if 'dominant_color' in item and 'secondary_color' in item]
    
    with open(new_path, 'w') as f:
        json.dump(data, f)
        
def clean_data_kaggle(json_path: str, new_path):
    with open(json_path) as f:
        data = json.load(f)
        
    data = [item for item in data if 'dominant_color' in item and 'secondary_color' in item]

    with open(new_path, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    clean_data_kaggle('fashion_items/styles.json', 'polyvore_dataset/styles_cleaned.json')
