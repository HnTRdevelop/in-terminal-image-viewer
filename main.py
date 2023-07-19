from colorama import *
from PIL import Image
import sys
import os


COLORS = {
    (0, 0, 0): Fore.BLACK,
    (1, 0, 0): Fore.RED,
    (0, 1, 0): Fore.GREEN,
    (1, 1, 0): Fore.YELLOW,
    (0, 0, 1): Fore.BLUE,
    (1, 0, 1): Fore.MAGENTA,
    (0, 1, 1): Fore.CYAN,
    (1, 1, 1): Fore.WHITE
}


def get_resize_factor(terminal_size, image_size, bypass_ver=False):
    if terminal_size[0] >= image_size[0] and terminal_size[0] >= image_size[0]:
        return 1
    if bypass_ver:
        return image_size[0] / terminal_size[0]
    if image_size[0] / terminal_size[0] > image_size[1] / terminal_size[1]:
        return image_size[0] / terminal_size[0]
    return image_size[1] / terminal_size[1]


def get_closest_color(color):
    tmp = color.copy()
    tmp[0] = 1 if tmp[0] >= 128 else 0
    tmp[1] = 1 if tmp[1] >= 128 else 0
    tmp[2] = 1 if tmp[2] >= 128 else 0
    return (COLORS[tuple(tmp)], tuple(tmp))


def up(num):
    if int(num) < num:
        return int(num) + 1
    return int(num)


def add_lists(list1, list2):
    tmp = [0 for _ in range(len(list1))]
    for i in range(len(list1)):
        tmp[i] = list1[i] + list2[i]
    return tmp


def sub_lists(list1, list2):
    tmp = [0 for _ in range(len(list1))]
    for i in range(len(list1)):
        tmp[i] = list1[i] - list2[i]
    return tmp


def mult_list(lst, mult):
    tmp = [0 for _ in range(len(lst))]
    for i in range(len(lst)):
        tmp[i] = lst[i] * mult
    return tmp
    

def main():
    argv = sys.argv

    path = f"{os.getcwd()}/{argv[-1]}"

    bypass_ver = False
    images_paths = []
    char = "█"
    for arg_id in range(1, len(argv)):
        arg = argv[arg_id]
        if arg[arg.rfind("."):] not in Image.registered_extensions() and arg[0] != "-":
            continue
        if arg in {"--bypass-vertical", "-b"}:
            bypass_ver = True
            continue
        if arg in {"-c", "--character"}:
            char = argv[arg_id + 1][0]
            continue
        
        images_paths.append(arg)
    
    for path in images_paths: 
        if not os.path.isfile(path):
            return 1, f"Can't open {path}!"

        img = Image.open(path)
        pixels = img.load()
        
        terminal_size = (os.get_terminal_size().columns, os.get_terminal_size().lines)
        factor = up(get_resize_factor(terminal_size, img.size, bypass_ver))
        img_size_cubes = (img.size[0] // factor, img.size[1] // factor)

        error_table = [[0, 0, 0] for _ in range(img_size_cubes[0] * img_size_cubes[1])]

        pixels = img.load()
        for y in range(img_size_cubes[1]):
            for x in range(img_size_cubes[0]):
                color = [0, 0, 0]
                for i in range(factor):
                    for j in range(factor):
                        pixel = pixels[x * factor + j, y * factor + i]
                        if type(pixel) is int:
                            pixel = (pixel, pixel, pixel)
                        color = add_lists(color, pixel)
                clamped_color = add_lists(mult_list(color, 1 / (factor ** 2)), error_table[x + y * img_size_cubes[0]])
                clr, clr_tuple = get_closest_color(clamped_color)
                
                error = sub_lists(clamped_color, mult_list(clr_tuple, 255))
                if x != img_size_cubes[0] - 1:
                    error_table[x + 1 + y * img_size_cubes[0]] = add_lists(error_table[x + 1 + y * img_size_cubes[0]], mult_list(error, 2/4))
                if y != img_size_cubes[1] - 1:
                    error_table[x + (y + 1) * img_size_cubes[0]] = add_lists(error_table[x + (y + 1) * img_size_cubes[0]], mult_list(error, 1/4))
                if x != 0 and y != img_size_cubes[1] - 1:
                    error_table[x - 1 + (y + 1) * img_size_cubes[0]] = add_lists(error_table[x - 1 + (y + 1) * img_size_cubes[0]], mult_list(error, 1/4))
                print(clr + char, end="")
            print(Fore.RESET + "")
        print(Fore.RESET)
    return 0


if __name__ == "__main__":
    main()


"""
             X   5   3
     2   4   5   4   2
         2   3   2
           (1/32)
"""
