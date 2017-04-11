#!/usr/bin/python3
# coding : utf-8
import argparse
from PIL import Image
from steganoPy.numberGenerator import NumberGenerator



def main():
    """parser = argparse.ArgumentParser(prog='HideMe', description='Hide/Show text in/from an image - possibility to encrypt/decrypt it before/after')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 1.0')
    parser.add_argument('image', help="The image to use")
    parser.add_argument('--file', '-f', help="The textfile to use")
    parser.add_argument('-k', '--key', help="The key to use to encrypt/decrypt")
    parser.add_argument('-e', '--extract', help='Extract mode', action='store_false')
    args = parser.parse_args()"""
    a = NumberGenerator((600, 400), 500)
    a.generate_list()




if __name__ == '__main__':
    main()

