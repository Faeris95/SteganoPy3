#!/usr/bin/python3
# coding : utf-8
import argparse
from PIL import Image

phrase = list("phrase")
ok = True
pxl_list = []


def main():
    global ok
    parser = argparse.ArgumentParser(prog='HideMe',
                                     description='Hide/Show text in/from an image - possibility to encrypt/decrypt it before/after')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 1.0')
    parser.add_argument('image', help="The image to use")
    parser.add_argument('--file', '-f', help="The textfile to use")
    parser.add_argument('-k', '--key', help="The key to use to encrypt/decrypt")
    parser.add_argument('-e', '--extract', help='Extract mode', action='store_false')
    args = parser.parse_args()
    if not (args.extract):
        img = Image.open(args.image)
        x, y = img.size
        im = img.load()
        for i in range(x):
            if not (ok):
                break
            for j in range(y):
                if not (ok):
                    break
                for k in range(3):
                    if (k <= 0):
                        ok = False
                        break

    else:
        img = Image.open(args.image)
        x, y = img.size
        im = img.load()
        for i in range(x):
            if not (ok):
                break
            for j in range(y):
                if not (ok):
                    break
                for k in range(3):
                    try:
                        letter = phrase.pop()
                    except IndexError:
                        ok = False
                        break
                    r = im[i, j][0]
                    g = im[i, j][1]
                    b = im[i, j][2]
                    nb = ord(letter)
                    if (k == 0):
                        r += nb
                        r %= 256
                    elif (k == 1):
                        g += nb
                        g %= 256
                    else:
                        b += nb
                        b %= 256
                    im[i, j] = (r, g, b)
                    print(r, g, b)
        img.save("test.jpg")


if __name__ == '__main__':
    main()

