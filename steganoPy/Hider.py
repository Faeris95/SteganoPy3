#!/usr/bin/python3
# coding : utf-8
from PIL import Image

if __name__ == '__main__':
    print("Please execute main.py")
    exit(-1)


class Hider():
    def __init__(self, image, txt):
        self.image = Image.open(image)
        self.pxls = self.image.load()

        self.txt = list(self.get_text(txt))
        self.pxl_list = []
        self.size = self.set_size()

    def hide(self):
        pass

    def set_size(self):
        return self.image.size

    def get_text(self, txt):
        with open(self.txt, "r") as f:
            return f.read().strip()
