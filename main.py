from colorama import *
from PIL import Image
import sys
import os
from vectors import *


COLORS = {
    "BLACK": (0, 0, 0),
    "RED": (1, 0, 0),
    "GREEN": (0, 1, 0),
    "YELLOW": (1, 1, 0),
    "BLUE": (0, 0, 1),
    "MAGENTA": (1, 0, 1),
    "CYAN": (0, 1, 1),
    "WHITE": (0, 0, 0)
}


def get_resize_factor(terminal_size, image_size):
    if terminal_size > image_size:
        return 1
    



def main():
    argv = sys.argv

    if len(argv) == 1:
        return 1, "You must specify the path to the image to be converted!"
    if len(argv) != 2:
        return 1, "You can convert only one image!"
    
    path = f"{os.getcwd()}/{argv[1]}"

    if not os.path.isfile(path):
        return 1, f"Can't open {path}!"

    img = Image.open(path)
    img_size = vec2i(*img.size)

    terminal_size = vec2i(os.get_terminal_size().lines, os.get_terminal_size().columns)

    pixels = img.load()
    for y in range(size_y):
        for x in range(size_x):
            print(pixels[x, y])

    return 0, None


if __name__ == "__main__":
    exit_code, message = main()
    if exit_code == 0:
        print("Program was working fine!")
    if exit_code == 1:
        print("Program enden with error.\nError message: " + message)
    if exit_code == 2:
        print("Program ended with unknown error!")
