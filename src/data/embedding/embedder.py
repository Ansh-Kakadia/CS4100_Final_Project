import pandas as pd




def get_embedding(id: str):
    
    df = pd.read_csv("./fashion_items/styles.csv", on_bad_lines="skip")
    
    row = df.query(f"id == {id}").iloc[0]
    
    gender = row["gender"]
    master_category = row["masterCategory"]
    sub_category = row["subCategory"]
    article_type = row["articleType"]
    base_colour = row["baseColour"]
    season = row["season"]
    year = row["year"]
    usage = row["usage"]
    product_name = row["productDisplayName"]
    
    # work on making these into numbers
    
    

