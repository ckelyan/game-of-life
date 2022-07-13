# Conway's Game of Life
This is my own attempt at recreating the famous 0-player Game of Life. It's using matplotlib to create images from a binary matrix, which are then used to create a gif.

## Example output (100 frames):
![output](https://github.com/flexflower/Game-of-Life/blob/main/out/out12.gif "With preset 'glidergun'")

# Usage
## With pcreate
You can create presets using my other project [pcreate](https://github.com/flexflower/pcreate).

You can use pcreate-bridge.* (sh for *nix, bat for Windows and py universal) to do the process automatically;
Each one asks for 2 arguments:
- pcpath: the path to the pcreate folder. Can be absolute or relative. 
- patname (optional): the name of the pattern to be saved in this folder's preset JSON file. Defaults to "default"
```sh
// windows
start pcreate-bridge.bat <pcpath> <patname>
// *nix (macos, linux, etc)
./pcreate-bridge.sh <pcpath> <patname>
// universal
<python executable> pcreate-bridge.py <pcpath> <patname>
```

## With your own matrices
You can use your own matrices if you're using JSON to store them, else you're going to need to write your own program to load them into main.py, then pass it as an array-like to the generate function. Keep in mind, it is not meant to be used as a module.

## With a random matrix
If you don't pass anything to the Life initializer, it will create a random matrix, that is a matrix whose cells are evenly randomly set.