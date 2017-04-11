#!/usr/bin/python3
# coding : utf-8
# Sébastien Rolland <sebastien.rolland@protonmail.com> - Faeris95
# https://github.com/Faeris95/SteganoPy3

import argparse
from PIL import Image, UnidentifiedImageError
import os
import sys
import hashlib
import hmac
import secrets
import base64
from math import ceil

VERSION = 2.0
ENCODED_SIZE_BITS_LENGTH = 32


class NumberGeneratorException(Exception):
    def __init__(self, message):
        self.message = message


class NumberGenerator():
    """
    NumberGenerator return an iterator on pairs of values generated from
    HMAC-BLAKE2s PRF
    """

    def __init__(self, x: int, y: int, key: bytes):
        """
        :param x: Max range of the generated values for first value
        :param y: Maximum range of generated values for second value
        :param key: Key to use for PRF
        """

        if not (x and y and key):
            raise NumberGeneratorException("Bad coordinates or key")

        self.ctr = bytes(1)
        self.coord = self._generate_coord(x, y)
        self.prng = hmac.new(key=key, msg=self.ctr, digestmod=hashlib.blake2s)

    def _generate_coord(self, x: int, y: int) -> list:
        """
        Method that generates a list of all possibles coordinates for x and y
        """

        coord = list()

        for sublist in [[(i, j) for i in range(x)] for j in range(y)]:
            for elem in sublist:
                coord.append(elem)

        return coord

    def __iter__(self):
        return self

    def __next__(self) -> list:

        self.prng.update(self.ctr)

        # Increment self.ctr
        next_ctr = int.from_bytes(self.ctr, sys.byteorder) + 1
        self.ctr = next_ctr.to_bytes(
            ceil(next_ctr.bit_length() / 8), sys.byteorder)

        if not self.coord:
            raise StopIteration()

        # PRNG result is used to determined index in the
        # list of coordinates that will be used
        index = int.from_bytes(
            self.prng.digest(), sys.byteorder) % len(self.coord)

        return self.coord.pop(index)


class SteganoIMGException(Exception):
    def __init__(self, message):
        super().__init__(message)


class SteganoIMGOverflowError(SteganoIMGException):
    def __init__(self):
        super().__init__("Image capacity is lower than data length to hide")


class SteganoIMG():
    """
    Hide/Recover a file in/from a PNG image.
    Used pixels are pseudo-random and chosen thanks HMAC-BLAKE2s, a cryptographycally secure and fast PRF.  # noqa: E501
    Seed is derivated from the password using 1M iterations of PBKDF2-HMAC-SHA256.
    """

    def __init__(self, image: str, key: str):
        """
        :param image: Image to use
        :param file: The file to hide
        :param key: The key to use
        """

        if not image.lower().endswith(".png"):
            print("Image is not an .png extension file. Process might failed.")

        try:
            self.image = Image.open(image)
        except UnidentifiedImageError as err:
            raise SteganoIMGException(f"{image} is not an image. {err}")

        image_x = self.image.size[0]
        image_y = self.image.size[1]
        secure_key = self._gen_key(key)
        self.numberGenerator = iter(
            NumberGenerator(image_x, image_y, secure_key))

        # RGB pixels
        self.image_capacity = image_x * image_y * 3
        self.img = self.image.load()

    def _gen_key(self, password=None) -> bytes:
        """
        Generate a random 256 bits number if `password` is None.
        Derive `password` with 1M iterations of PBKDF2-HMAC-256 otherwise.

        :param password: Password to generate the final key from.
        :return:
        """

        if password:
            key = hashlib.pbkdf2_hmac("sha256", bytes(
                password, "utf-8"), bytes(), 1000000)
            b64key = base64.b64encode(key)
        else:
            key = secrets.randbits(256).to_bytes(32, sys.byteorder)
            b64key = base64.b64encode(key)

        return b64key

    def _get_data_from_file(self, data_file: str) -> None:
        """
        :param data_file: File to extract the data from
        :return: Data from `data_file`

        Return data from `data_file`
        """
        if (os.path.isfile(data_file)):
            try:
                with open(data_file, "rb") as f:
                    return f.read()
            except OSError as err:
                raise SteganoIMGException(err)

    def hide(self, data_file: str, output_file: str) -> None:
        """
        :param data_file: File to hide
        :param output_file: File to write to

        This method is used to hide the text in the image that are loaded
        """

        file_len = os.path.getsize(data_file)
        bits_to_hide_len = file_len * 8

        if (bits_to_hide_len > self.image_capacity):
            raise SteganoIMGOverflowError()

        data = self._get_data_from_file(data_file)

        x, y = 0, 0
        rgb = 0
        tmp_bits = [bin(t)[2:] for t in data]
        bits_to_hide = ["0" * (8 - len(t)) + t if len(t)
                        < 8 else t for t in tmp_bits]

        # Total length is written on the ENCODED_SIZE_BITS_LENGTH first bits
        binary_encoded_size = "0" * \
            (ENCODED_SIZE_BITS_LENGTH -
             len(bin(bits_to_hide_len)[2:])) + bin(bits_to_hide_len)[2:]

        bits_to_hide.insert(0, binary_encoded_size)

        for byte in bits_to_hide:
            for bit in byte:
                if (rgb == 0):
                    try:
                        x, y = next(self.numberGenerator)
                    except StopIteration:
                        raise SteganoIMGException("No more coordinates to use")

                pixels_values = list(self.img[x, y])

                colour_value = pixels_values[rgb]

                # LSB is modified following `bit`
                colour_value = colour_value & 0xFE | int(bit)

                pixels_values[rgb] = colour_value
                self.img[x, y] = tuple(pixels_values)

                rgb = (rgb + 1) % 3

        if not output_file:
            output_file = "outfile.png"
        try:
            self.image.save(output_file, quality=100)
        except ValueError as err:
            raise SteganoIMGException(str(err))

    def recover(self, output_file: str) -> None:
        """
        :param output_file: File to write to

        Recover hidden data from the image and write them to `output_file`
        """

        ctr = 0
        size_to_recover = 0
        x = y = rgb = 0
        buffer = 0

        bytes_array = bytes()

        while (ctr < ENCODED_SIZE_BITS_LENGTH):
            if rgb == 0:
                try:
                    x, y = next(self.numberGenerator)
                except StopIteration:
                    raise SteganoIMGException("No more coordinates to use")

            # Left bit shifft and add the bit from LSB of colour pixel
            size_to_recover = (size_to_recover << 1) + \
                (self.img[x, y][rgb] & 1)
            rgb = (rgb + 1) % 3
            ctr += 1

        if size_to_recover > self.image_capacity:
            raise SteganoIMGException("Bits length to recover is higher than image capacity. "  # noqa: E501
                                      "Bad password, data is corrupted or nothing to recover.")  # noqa: E501
        ctr = 0
        while(ctr < size_to_recover):
            if rgb == 0:
                try:
                    x, y = next(self.numberGenerator)
                except StopIteration:
                    raise SteganoIMGException("No more coordinates to use")

            buffer = (buffer << 1) + (self.img[x, y][rgb] & 1)
            ctr += 1
            rgb = (rgb + 1) % 3
            if ctr % 8 == 0:
                bytes_array += bytes([buffer])
                buffer = 0

        if not output_file:
            output_file = "a.out"
        try:
            with open(output_file, "wb") as f:
                f.write(bytes_array)
        except OSError as err:
            raise SteganoIMGException(err)


def main():
    parser = argparse.ArgumentParser(prog='SteganoPy3',
                                     description="Hide/Show data in/from PNG "
                                                 "file using pseudo random pixels coordinates")  # noqa: E501

    parser.add_argument("action", choices=("hide", "show"))
    parser.add_argument('image', help="The image to use")
    parser.add_argument('password', help="Password, secret, key to use")
    parser.add_argument('-f', '--file', help="The file to hide within image")
    parser.add_argument('-o', '--output')
    parser.add_argument('--version', '-V', action='version',
                        version=f"%(prog)s v{VERSION}")

    args = parser.parse_args()
    if args.action == "hide":
        if not (args.file and os.path.isfile(args.file)):
            print(f"Unable to find {args.file}", file=sys.stderr)
            exit(-1)

    if not os.path.isfile(args.image):
        print(f"Unable to find {args.image}", file=sys.stderr)
        exit(-1)

    try:
        stegano = SteganoIMG(args.image, args.password)
    except SteganoIMGException as e:
        print(f"{e}", sys.stderr)
        exit(-1)

    if args.action == "hide":
        try:
            stegano.hide(args.file, args.output)
        except SteganoIMGException as e:
            print(f"{e}", sys.stderr)
            exit(-1)
    elif args.action == "show":
        try:
            stegano.recover(args.output)
        except SteganoIMGException as e:
            print(f"{e}", sys.stderr)
            exit(-1)


if __name__ == '__main__':
    main()
