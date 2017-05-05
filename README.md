# SteganoPy
Written by Sébastien ROLLAND - Faeris95

SteganoPy can hide text in an image using LSB and pseudo-random number generator with a key (to determine the coordinates of pixels), and recover it.

### Installation of dependent libraries

sudo python3 -m pip install argparse
sudo python3 -m pip install pillow

### Running
<strong>Currently working only with PNG images !</strong>

chmod +x steganoPy.py

To hide :
./steganoPy.py image.png -t text.txt -o output.png
or you can specify a key to use (>= 10 numbers)
./steganoPy.py image-png -t text.txt -k 1546879542 -o output.png

To recover text:
./steganoPy.py image.png -e -k keyFile.txt -o text.txt


### Contact
Sébastien ROLLAND
sebastien.rolland@protonmail.com

I need your help to improve it ;)