#!/usr/bin/python3
# coding : utf-8
from PIL import Image
import os
from steganoPy.numberGenerator import NumberGenerator

class Hide():
    def __init__(self, image, text, key):
        self.image = Image.open(image)
        self.pxls = self.image.load()
        self.key = key
        self.text=text
        self.len_txt = 0
        if(text):
            self.text = list(self.get_text(text))
            self.len_txt = len(self.text)
        if(key):
            self.extract_key(key)
        self.size = self.set_size()
        self.generator = NumberGenerator(self.size, self.len_txt, self.key)
        self.pxl_list = self.generator.get_pixels_list()

    def hide(self, output="out"):
        pass
    def unhide(self,output="out"):
        pass

    def extract_key(self, key):
        if(os.path.isfile(key)):
            with open(key,"r") as f:
                line = f.readline().strip()
                final_key = line.split(";")[0]
                length = line.split(";")[1]
                self.key = int(final_key)
                self.len_txt = int(length)
        else:
            self.key = int(key)

    def set_size(self):
        return self.image.size

    def get_text(self, txt):
        if (os.path.isfile(txt)):
            with open(txt, "r") as f:
                return f.read().strip()
        else:
            return txt
