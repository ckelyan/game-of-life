import os
import sys
import pathlib

# get path from args
PATH = sys.argv[1] if len(sys.argv) > 1 else ""
PAT_NAME = sys.argv[2] if len(sys.argv) > 2 else "default"
if not PATH:
    print("Please provide a path to the pcreate folder")
    sys.exit(1)

# store the current working directory
curdir = str(pathlib.Path().absolute()).replace("\\", "/")

# navigate to the pcreate folder
os.chdir(PATH)
# run the preset script
os.system(f'{sys.executable} main.py {PAT_NAME} ai {curdir}/presets.json')

# run game of life
os.chdir(curdir)
os.system(f'{sys.executable} main.py {PAT_NAME}')