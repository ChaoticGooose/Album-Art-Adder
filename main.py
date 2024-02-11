from sys import argv
import music_tag
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

audio_extensions = ['.aac', '.aiff', '.dsf', '.flac', '.m4a', '.mp3', '.ogg', '.opus', '.wav', '.wv']
image_extentions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']

def main():
    directory = argv[1] if len(argv) > 1 else os.getcwd()
    try:
        # Get all files in directories with valid extentions
        art = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.splitext(file)[1].lower() in image_extentions ][0] # Get the first image in the directory
        files = sorted([os.path.join(directory, file) for file in os.listdir(directory) if os.path.splitext(file)[1].lower() in audio_extensions]) # Get all audio files in the directory
    except (NotADirectoryError, FileNotFoundError) as e:
        print(f'{bcolors.FAIL}Error: {e}{bcolors.ENDC}')
        print(f'{bcolors.FAIL}Usage: python3 main.py {bcolors.UNDERLINE}<music-directory>{bcolors.ENDC} {bcolors.UNDERLINE}{bcolors.FAIL}<art-directory>{bcolors.ENDC}')
        return 1

    for file in files:
        try:
            print(f"{bcolors.OKGREEN}{'-'*os.get_terminal_size().columns}{bcolors.ENDC}")
            print(f"{bcolors.OKCYAN}Processing: {file}{bcolors.ENDC}")
            audio = music_tag.load_file(file)
            with open(art, 'rb') as img_in:
                audio['artwork'] = img_in.read() # Set the artwork 
            audio['artwork'].first.thumbnail([64, 64]) # Create a thumbnail
            audio.save()
            print(f"{bcolors.OKCYAN}Complete.{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")

main()