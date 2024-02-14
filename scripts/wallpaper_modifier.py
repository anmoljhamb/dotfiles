"""
When the script starts, check for the environment variable "CURR_WALLPAPER",
and if that variable, doesn't exist, create one, by choosing one of the random
files from the array that is returned by files.

Set the wallpaper to that.
"""

import os
import random
import subprocess as sp

directory = "/home/anmol/dotfiles/Wallpapers/"


def getCurrWallpaper():
    with open(f"{directory}curr_wallpaper") as file:
        data = file.read()
        data = int(data.strip("\n"))
        return data


def setCurrWallpaper(index: int):
    with open(f"{directory}curr_wallpaper", "w") as file:
        file.write(str(index))


if __name__ == "__main__":
    files = os.listdir(directory)
    curr = getCurrWallpaper()
    print(f"curr_wallpaper={curr}")
    rand = random.randint(0, len(files) - 1)
    while rand == curr:
        rand = random.randint(0, len(files) - 1)
    curr = rand
    setCurrWallpaper(curr)
    print(f"new_wallpaper={curr}")
    file = f"{directory}{files[curr]}"
    print(file)
