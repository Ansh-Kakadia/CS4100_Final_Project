import json
import pandas as pd
import os

base = os.path.dirname(__file__)

datasets = {
    'train': 'train_no_dup.json',
    'test': 'test_no_dup.json',
    'valid': 'valid_no_dup.json',
}

for split, fname in datasets.items():
    with open(os.path.join(base, fname)) as f:
        data = json.load(f)

    rows = []
    for outfit in data:
        for item in outfit.get('items', []):
            rows.append({
                'set_id': outfit.get('set_id'),
                'outfit_name': outfit.get('name'),
                'views': outfit.get('views'),
                'date': outfit.get('date'),
                'item_index': item.get('index'),
                'item_name': item.get('name'),
                'categoryid': item.get('categoryid'),
                'image_url': item.get('image'),
            })

    df = pd.DataFrame(rows)
    out_path = os.path.join(base, f'{split}_flat.xlsx')
    df.to_excel(out_path, index=False)
    print(f'{split}: {len(data)} outfits → {len(df)} rows → saved to {split}_flat.xlsx')
