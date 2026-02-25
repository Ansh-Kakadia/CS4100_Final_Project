import kagglehub

# Download latest version
path = kagglehub.dataset_download("paramaggarwal/fashion-product-images-small", 
                                  output_dir="./fashion_items")
print("Path to dataset files:", path)