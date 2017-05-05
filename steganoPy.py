#!/usr/bin/python3
# coding : utf-8
# Written by: Sébastien Rolland - Faeris95
# https://github.com/Faeris95/SteganoPy3
# Licensed under GNU GPL

import argparse
import time
from PIL import Image
import os

class NumberGenerator():
    """
    NumberGenerator use a pseudo random number generator using a key to find the coordinates of the pixels
    that have been used or will be used to hide/extract text in/from an image
    """
    def __init__(self,size,size_txt, key = None):
        """
        :param size: Size of the image (x,y)
        :param size_txt: Size of the text
        :param key: The key to use (If none, will be generated)
        """
        self.size = size
        self.size_txt = size_txt
        if(key):
            self.key = key
        else:
            self.key = int(time.time())
            with open("key.txt","w") as f:
                f.write(str(self.key)+";"+str(self.size_txt))
        self.pixels_list = []
        self.generate_list()

    def generate_list(self):
        new_key = self.key
        i=0
        x=0
        y=0
        while(i<=self.size_txt):
            for j in range(2):
                new_key = (new_key * 9301 + 49297) % 233280
                if(j==0):
                    x=new_key%(self.size[0]-1)
                else:
                    y=new_key%(self.size[1]-1)
            if not ((x,y)) in self.pixels_list:
                self.pixels_list.append((x,y))
                i+=1
    def get_pixels_list(self):
        return self.pixels_list


class Engine():
    """
    The engine class initialyze a number generator to find the coordinates of the pixels
    The engine allow us to hide or recover the text from or in an PNG image
    """

    def __init__(self, image, text, key):
        """
        :param image: Image to use
        :param text: The text to hide (can be None)
        :param key: The key to use (can be None)
        """
        self.image = Image.open(image)  # Loads the image we will use (to hide or recover)
        self.pxls = self.image.load()  # Loads the pixels of the image
        self.key = key  # The key to use (may be None, if None the number generator will create one and save it in key.txt)
        self.text = text  # The text to use,(may be None,
        self.len_txt = 0
        if (text):  # If text, we count the number of color component (8 bits per character, and 3 bits per pixel)
            self.text = list(self.get_text(text))
            length = ((len(self.text) * 8) // 3)
            self.len_txt = ((len(self.text) * 8) % 3) + length
        if (key):  # If key, we extract the key from the key file or just use the key if this is not a file
            self.extract_key(key)
        self.size = self.set_size()  # size of the image (x*y)
        self.generator = NumberGenerator(self.size, self.len_txt, self.key)  # initialize a number generator
        self.pxl_list = self.generator.get_pixels_list()  # the list of coordinates of pixels to use to hide or recover

    def hide(self, output="out.jpg"):
        """
        :param output: Output file (not necessary)
        :return: 
        This method is used to hide the text in the image that are loaded
        """
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
        self.image.save(output, quality=100)

    def recover(self, output):
        """
        :param output: Name of the output file (not necessary)
        :return: 


        Extract the text from the image using the key and write it in a file if an output file is given or print it if not.
        """
        text = []
        final_text = []
        for x, y in self.pxl_list:
            for k in range(3):
                text.append(self.pxls[x, y][k])

        text = [str(i & 1) for i in text]
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
        if (output):
            with open(output, "w") as f:
                f.write(''.join(final_text))
        else:
            print(''.join(final_text))

    def extract_key(self, key):
        """
        :param key: The key to use to extract
        :return:


        If the key argument is a file, we extract the file and the size of the text we are going to extract
        If the argument is a key, we load the key
        """

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
        """
           If the text argument is a file, we load the text from it
        """
        if (os.path.isfile(txt)):
            with open(txt, "r") as f:
                return f.read().strip()
        else:
            return txt


def main():
    parser = argparse.ArgumentParser(prog='SteganoPy',
                                     description='''Hide/Show text in/from an image - possibility to encrypt/decrypt it before/after
                                     
    Example usage :
    Hide : 
    steganoPy.py image.png -t text.txt -o outputImage.png
    steganoPy.py image.png -t text.txt -k 1548796548 -o outputImage.png
                                     
    Recover :
    steganoPy.py steganoImage.png -e -k keyFile.txt -o text.txt''',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 1.0')
    parser.add_argument('image', help="The image to use")
    parser.add_argument('-t', '--text', help="The file or text to use")
    parser.add_argument('-k', '--key', help="The key or the keyfile to use to encrypt/decrypt")
    parser.add_argument('-e', '--extract', help='Extract mode', action='store_true')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    engine = Engine(args.image, args.text, args.key)
    if not (args.extract):
        engine.hide(args.output)
    else:
        engine.recover(args.output)

if __name__ == '__main__':
    main()
