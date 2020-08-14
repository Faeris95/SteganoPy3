# SteganoPy [![License](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://raw.githubusercontent.com/Faeris95/SteganoPy3/master/LICENSE)

Sébastien ROLLAND - Faeris95

SteganoPy3 hides data such as text in an image using LSB and cryptographycally secure pseudo-random number generator to determine the coordinates of pixels to use.

### How it works

SteganoPy3 replaces LSB of each colour component of each pixels with a bit of data to hide until all bits are hidden. 32 first bits are used to write the total length to recover so it can hide a maximum of X * Y * 3 - 32 bits with X and Y the pixels width and length of the image. 

### Cryptography

The key used as seed is derivated with 1M iterations of PBKDF2 with HMAC and SHA-256. 
HMAC with BLAKE2s computation of the secret and a counter is used as PRNG because it seems it is faster that SHA3 family on modern CPUs. 

### Installation of needed libraries
```
python3 -m pip install --user -r requirements.txt
```
### Running
<strong>Works with PNG images only !</strong>

To hide :
```
steganoPy.py hide <image.png> <data.file> <password> [-o <image_with_data.png>]
```

To recover data:
```
steganoPy.py show <image_with_data.png> <password> [-o <data.file>]
```
### To Do

Add possibility to encrypt data before hiding it
