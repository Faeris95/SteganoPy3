#!/usr/bin/python3
# coding : utf-8
from PIL import Image
import os
from steganoPy.numberGenerator import NumberGenerator


class Engine():
    def __init__(self, image, text, key):
        self.image = Image.open(image)
        self.pxls = self.image.load()
        self.key = key
        self.text = text
        self.len_txt = 0
        if (text):
            self.text = list(self.get_text(text))
            length = ((len(self.text) * 8) // 3)
            self.len_txt = ((len(self.text) * 8) % 3) + length
        if (key):
            self.extract_key(key)
        self.size = self.set_size()
        self.generator = NumberGenerator(self.size, self.len_txt, self.key)
        self.pxl_list = self.generator.get_pixels_list()

    def hide(self, output="out.jpg"):
        x, y = 0, 0
        k = 0
        text = [bin(ord(t))[2:] for t in self.text]
        text = ["0" * (8 - len(t)) + t if len(t) < 8 else t for t in text]
        for t in text:
            for bit in t:
                if (k == 0):
                    x, y = self.pxl_list.pop(0)
                compo = bin(self.pxls[x, y][k])
                compo = list(compo)
                compo.pop()
                compo.append(bit)
                compo = ''.join(compo)
                compo = int(compo, 2)
                if (k == 0):
                    self.pxls[x, y] = (compo, self.pxls[x, y][1], self.pxls[x, y][2])
                    k += 1
                elif (k == 1):
                    self.pxls[x, y] = (self.pxls[x, y][0], compo, self.pxls[x, y][2])
                    k += 1
                else:
                    self.pxls[x, y] = (self.pxls[x, y][0], self.pxls[x, y][1], compo)
                    k = 0
        self.image.save(output,quality=100)

    def unhide(self, output):
        text = []
        final_text = []
        for x, y in self.pxl_list:
            for k in range(3):
                text.append(self.pxls[x, y][k])

        text = [str(i&1) for i in text]
        cnt = 0
        buff = ""
        for c in text:
            if (cnt >= 8):
                final_text.append(buff)
                buff = c
                cnt = 1
            else:
                buff += c
                cnt += 1

        final_text = [chr(int(i, 2)) for i in final_text]
        if(output):
            with open(output, "w") as f:
                f.write(''.join(final_text))
        else:
            print(''.join(final_text))

    def extract_key(self, key):
        if (os.path.isfile(key)):
            with open(key, "r") as f:
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
