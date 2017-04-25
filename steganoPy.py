#!/usr/bin/python3
# coding : utf-8
import argparse
from steganoPy.engine import Engine


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

    engine = Engine(args.image, args.text, args.key)
    if not (args.extract):
        engine.hide(args.output)
    else:
        engine.unhide(args.output)

if __name__ == '__main__':
    main()
