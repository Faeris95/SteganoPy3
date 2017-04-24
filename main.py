#!/usr/bin/python3
# coding : utf-8
import argparse
from steganoPy.hide import Hide


def main():
    parser = argparse.ArgumentParser(prog='HideMe',
                                     description='Hide/Show text in/from an image - possibility to encrypt/decrypt it before/after')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 1.0')
    parser.add_argument('image', help="The image to use")
    parser.add_argument('-t', '--text', help="The file or text to use")
    parser.add_argument('-k', '--key', help="The key or the keyfile to use to encrypt/decrypt")
    parser.add_argument('-e', '--extract', help='Extract mode', action='store_true')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    hide = Hide(args.image, args.text, args.key)
    if not (args.extract):
        hide.hide(args.output)
        print("On cache")
    else:
        hide.unhide(args.output)
        print("On extrait")









if __name__ == '__main__':
    main()
