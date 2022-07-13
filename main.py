import os
import sys
import json
import shutil
import random
import numpy as np
import imageio.v2 as imageio
from matplotlib import pyplot as plt
from typing import Union

# constants
DEFAULT_PRESET_FILE = 'presets.json'
PAT_NAME = sys.argv[1] if len(sys.argv) > 1 else None
IMG_PATH = '.imgs'

if not os.path.exists(IMG_PATH):
    os.mkdir(IMG_PATH)

class Life:
    def __init__(self, preset: Union[np.ndarray, list, tuple, str]=None, show_plot: bool=False, grid_size: int=100) -> None:
        """Life initializer

        Args:
            preset (Union[np.ndarray, list, tuple, str], optional): Either the name of the preset in the presets file, or the matrix directly. If None, an random matrix will be created. Defaults to None.
            show_plot (bool, optional): Tells whether or not each frame should be shown in a window. Defaults to False.
            grid_size (int, optional): If preset is empty, the size of the random grid. Won't be used otherwise. Defaults to 100.
        """
        
        # boolean to tell whether or not it shows each frame as a pyplot with plt.show()
        self.show_plot = show_plot
        
        # if preset is none, create a random grid
        if not preset:
            self.grid = [[1 if i in random.sample(range(grid_size), int(grid_size/(grid_size/3))) else 0 for i in range(grid_size)] for _ in range(grid_size)]
        
        else:
            # if the preset is an ndarray, store it as-is
            if type(preset) == np.ndarray:
                self.grid = preset
            
            # if the preset is a list or a tuple, convert it to a ndarray
            elif type(preset) in [list, tuple]:
                self.grid = np.array(preset)
            
            # if the preset is a string, load it from the presets file
            elif type(preset) == str:
                # load the presets
                with open(DEFAULT_PRESET_FILE, "r") as f:
                    presets = json.load(f)

                self.grid = np.array(presets[preset])
        
        # might make it possible to have a non-square grid
        self.grid_size = len(self.grid)    

    def DEPRECATED_neighbors(self, row: int, col: int) -> int:
        # This implementation is unnecessarily slow and long, but it works and I like it so I'm leaving it in the code.
        
        """Get the amount of set neighbors of a cell

        Args:
            row (int): Row number of the cell
            col (int): Col number of the cell

        Returns:
            int: Amount of neighbors
        """
        
        result = []
        # -1, 0, 1 (left, same, right)
        for rAddend in range(-1, 2):
            # to find the row it's going to check (first row-1, then row, then row+1)
            new_row = row + rAddend
            # if new_row is in bounds
            if len(self.grid)-1 >= new_row >= 0:
                # repeat for cols
                for cAddend in range(-1, 2):
                    new_col = col + cAddend
                    if new_col >= 0 and new_col <= len(self.grid)-1:
                        # skip if it's the center cell
                        if new_col == col and new_row == row:
                            continue
                        # else add the cell to the result
                        result.append(self.grid[new_row, new_col])

        # all we really need is the amount of set neighbors and since the matrix is binary we can just use the sum
        return sum(result)

    def neighbors(self, row: int, col: int) -> int:
        """Function to get the amount of set neighbors of a cell. This implementation works since if a value is not 0 it's always 1, which means we can get the amount by getting their sum.

        Args:
            row (int): Row number of the cell
            col (int): Col number of the cell

        Returns:
            int: Amount of set neighbors
        """
        
        # get the sum of the neighbors, which correspons to the amount of set neighbors since they're always 0 or 1, then subtract the one in the center.
        return np.sum(self.grid[row-1:row+2, col-1:col+2]) - self.grid[row, col]

    def next(self) -> bool:
        """Generate the next frame of the game

        Returns:
            bool: Has changed
        """

        new_grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        for i1 in range(self.grid_size):
            for i2 in range(self.grid_size):
                # get the amount of neighbors for each cell
                amnt_neighbors = self.neighbors(i1, i2)
                
                # if the cell is alive
                if self.grid[i1, i2]:
                    # if it has less than 2 or more than 3 neighbors, it dies
                    if amnt_neighbors < 2 or amnt_neighbors > 3:
                        new_grid[i1, i2] = 0

                    # otherwise it lives
                    else:
                        new_grid[i1, i2] = 1

                else:
                    # if the cell is dead and has exactly 3 neighbors, it comes to life
                    if amnt_neighbors == 3:
                        new_grid[i1, i2] = 1

        # show the plot if it's supposed to
        if self.show_plot:
            self.plotgrid()

        # if the grid has changed, return False
        if np.array_equal(self.grid, new_grid):
            return False
        
        # otherwise update the grid and return True
        self.grid = new_grid
        return True

    def isalive(self) -> bool:
        """Check if there are any alive cells"""

        return np.any(self.grid)

    def print_grid(self) -> None:
        """Print the grid to the console"""
        
        for i in self.grid:
            for j in i:
                if j:
                    print("██", end="")
                else:
                    print("  ", end="")
            print()
     
    def plotgrid(self) -> None:
        """Plot the grid with plt.show()"""

        # flip each bits because white for alive and black for dead looks better
        grid = np.invert(np.array(self.grid.copy()))
        plt.imshow(grid, interpolation='none', cmap='Greys')
        plt.show()

    def saveplot(self, i: int) -> None:
        # same as plotgrid
        grid = np.invert(np.array(self.grid.copy()))
        # the ticks are irrelevant
        plt.xticks([])
        plt.yticks([])
        # set the xlabel as the frame number
        plt.xlabel(f'frame {i}')
        plt.imshow(grid, interpolation='none', cmap='Greys')
        # save the plot as an image in the IMG_PATH folder
        plt.savefig(f'{IMG_PATH}/fig{i:03}.png')
        # clear the figure
        plt.clf()


def imgif(speed: float=0.4) -> None:
    """Create a gif from the images in the IMG_PATH folder in ./out

    Args:
        speed (float): Time in s of the each frame in the gif
    """
    
    # sort the files in the IMG_PATH folder by the trailing numbers in their names.
    # Apparently it works as-is, no need to indicate the sorting key. Probably because the numbers are of fixed length.
    file_names = sorted((f'{IMG_PATH}/{fn}' for fn in os.listdir(f'{IMG_PATH}/') if fn.endswith('.png')))
    # create image objects for each file
    images = [imageio.imread(fn) for fn in file_names]

    # get all the gif names in the out folder
    unsorted_gifs = (fn[:-4] for fn in os.listdir('./out/') if fn.endswith('.gif'))
    # sort them, now we have to add a key because the numbers are of different lengths
    sorted_gifs = sorted(unsorted_gifs, key=lambda x: int(x[3:]))
    # get the last one if there even is any and turn it into an int
    last_n = int(sorted_gifs[-1][3:]) if sorted_gifs else 0
    filename = f"out{last_n+1}.gif"
    # write the gif to the out folder. duration is the time between each frame
    imageio.mimwrite("./out/"+filename, images, loop=1, duration=speed)
    print(f"Saved as {filename}")
    
# main function
def generate(max_frames=100, preset:  Union[np.ndarray, list, tuple, str]=PAT_NAME):
    life = Life(preset=preset)
    
    for i in range(max_frames):
        print("Generating frame", i, end="\r")

        life.saveplot(i)
        
        # life.next returns False if the grid has not changed, that is, if nothing is going to be changing anymore
        if not life.next():
            break
        
        if not life.isalive():
            print(f'\nDied at frame {i}')
            break
        
    else:
        print(f"Maximum frames reached ({max_frames})")

if __name__ == "__main__":
    generate(500)
    imgif(speed=0.1)
    
    # delete the temporary image folder
    shutil.rmtree(IMG_PATH)