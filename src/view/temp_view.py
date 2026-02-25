from PIL import Image


class TempView:
    
    def __init__(self, id: int):
        if not id:
            raise ValueError(f"Path is {None}")
    
        try:
            self.img = Image.open(f"./fashion_items/images/{id}.jpg")
        except:
            raise ValueError("No image found at the path")
    
    def view(self):
        self.img.show()
    

if __name__ == "__main__":
    view = TempView(1539)
    view.view()
    
    