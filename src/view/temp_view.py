from PIL import Image


class TempView:
    
    def __init__(self, path: str):
        if not path:
            raise ValueError(f"Path is {None}")
    
        try:
            self.img = Image.open(path)
        except:
            raise ValueError("No image found at the path")
    
    def view(self):
        self.img.show()
    

if __name__ == "__main__":
    view = TempView("./fashion_items/images/1163.jpg")
    view.view()