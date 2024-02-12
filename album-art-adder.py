#!/usr/bin/python3

import os
from glob import glob
from sys import argv, exit

import music_tag


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


audio_extensions = [
    ".aac",
    ".aiff",
    ".dsf",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".opus",
    ".wav",
    ".wv",
]
image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"]


def main():
    selected_directory = argv[1] if len(argv) > 1 else os.getcwd()
    sub_dirs = next(os.walk(selected_directory))[1]
    sub_dirs.append(selected_directory)

    for directory in sub_dirs:
        try:
            # Get all files in directories with valid extentions
            pattern = os.path.join(directory, "*%s")
            try:
                art = sum((glob(pattern % ext) for ext in image_extensions), [])[0]
            except IndexError:
                print(f"{bcolors.WARNING}Warning: No image found in {directory}{bcolors.ENDC}")
                continue
            files = sum((glob(pattern % ext) for ext in audio_extensions), [])
            if not files:
                print(
                    f"{bcolors.WARNING}Warning: No audio files found in {directory}{bcolors.ENDC}"
                )
                continue

        except (NotADirectoryError, FileNotFoundError) as e:
            print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
            print(
                f"{bcolors.FAIL}Usage: python3 main.py {bcolors.UNDERLINE}<music-directory>{bcolors.ENDC}"
            )
            return 1

        for file in files:
            try:
                print(
                    f"{bcolors.OKGREEN}{'-'*os.get_terminal_size().columns}{bcolors.ENDC}"
                )
                print(f"{bcolors.OKCYAN}Processing: {file}{bcolors.ENDC}")
                audio = music_tag.load_file(file)
                with open(art, "rb") as img_in:
                    audio["artwork"] = img_in.read()  # Set the artwork
                audio["artwork"].first.thumbnail([64, 64])  # Create a thumbnail
                audio.save()
                print(f"{bcolors.OKCYAN}Complete.{bcolors.ENDC}")
            except Exception as e:
                print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")


if __name__ == "__main__":
    exit(main())
