import json

def clean_data(json_path:str, new_path : str) -> None:
    
    with open(json_path) as f:
        data = json.load(f, )
    
    for outfit in data:
        outfit['items'] = [item for item in outfit['items'] if 'dominant_color' in item and 'secondary_color' in item]
    
    with open(new_path, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    clean_data('polyvore_dataset/valid_no_dup.json', 'polyvore_dataset/valid_no_dup_cleaned.json')
