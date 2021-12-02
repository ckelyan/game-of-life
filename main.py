import os
import json
import random
import imageio
import numpy as np
from PIL import Image
from time import sleep
from matplotlib import pyplot as plt

with open("presets.json", "r") as f:
    presets = json.load(f)

with open("fullpresets.json", "r") as f:
    fpresets = json.load(f)

def neighbors(matrix, rowNumber, colNumber):
    result = []
    for rowAdd in range(-1, 2):
        newRow = rowNumber + rowAdd
        if newRow >= 0 and newRow <= len(matrix)-1:
            for colAdd in range(-1, 2):
                newCol = colNumber + colAdd
                if newCol >= 0 and newCol <= len(matrix)-1:
                    if newCol == colNumber and newRow == rowNumber:
                        continue
                    result.append(matrix[newCol][newRow])
    return len([1 for i in result if i != 0])

class Life:
    def __init__(self, s=100, p=False, preset=None, fpreset=None):
        self.p = p
        self.s = s
        
        if not (preset or fpreset):
            self.grid = [[1 if i in random.sample(range(s), int(s/(s/3))) else 0 for i in range(s)] for _ in range(s)]
        elif preset in presets.keys(): #TODO: probably not working
            grid = np.zeros((s, s), dtype=int)
            pta = np.array(presets[preset]).reshape(3, 3)
            r, c = 50, 50
            grid[r:r+pta.shape[0], s-c:c+pta.shape[1]] = pta # append the preset to a blank grid
            self.grid = grid 
        elif fpreset in fpresets.keys():
            self.grid = fpresets[fpreset]
            self.s = len(self.grid[0])

    @staticmethod
    def delall():
        dir = 'imgs'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    def next(self):
        new = [[0 for _ in range(self.s)] for _ in range(self.s)]
        for i1 in range(self.s):
            for i2 in range(self.s):
                n = neighbors(self.grid, i2, i1)
                if self.grid[i1][i2]:
                    
                    if n < 2 or n > 3:
                        new[i1][i2] = 0
                    else:
                        new[i1][i2] = 1
                else:
                    if n == 3:
                        new[i1][i2] = 1

        return new

    def update(self, newg):
        self.grid = newg
        if self.p: self.plotgrid()

    def print_grid(self):
        for i in self.grid:
            for j in i:
                if j:
                    print("██", end="")
                else:
                    print("  ", end="")
            print()
     
    def plotgrid(self):
        g = np.array(self.grid.copy())
        g = np.invert(g)
        o = plt.imshow(g, interpolation='none', cmap='Greys')
        plt.show()
            
    def isalive(self):
        for i in self.grid:
           if 1 in i:
               return True
               
        return False

    def saveplot(self, i):
        g = np.array(self.grid.copy())
        g = np.invert(g)
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(f'frame {i}')
        o = plt.imshow(g, interpolation='none', cmap='Greys')
        plt.savefig(f'imgs/fig{i:03}.png')

def imgif(speed=0.4):
    file_names = sorted(('imgs/'+fn for fn in os.listdir('imgs/') if fn.endswith('.png')))

    # images = [Image.open(fn) for fn in file_names]
    images = [imageio.imread(fn) for fn in file_names]

    unsortedGifs = list(fn[:-4] for fn in os.listdir('./out/') if fn.endswith('.gif'))
    ls = sorted(unsortedGifs, key=lambda x: int(x[3:]))
    last = int(ls[-1][3:]) if ls else 0
    filename = f"out{last+1}.gif"
    imageio.mimwrite("./out/"+filename, images, loop=1, duration=speed)
    print(f"Saved as {filename}")
    

def main(maxFrames=100):
    lastLast = None
    last = None        
    l = Life(p=False, fpreset="glidergun")
    for i in range(maxFrames):
        l.saveplot(i)
        n = l.next()
        if n == last or n == lastLast:
            print(f"Stuck at frame {i}")
            break
        last = n
        
        l.update(n)
        if not l.isalive(): print(f'Died at frame {i}'); break
        print("Generating frame", i)
    else:
        print(f"Maximum frames reached ({maxFrames})")

try: 
    main(100)
except Exception as e:
    print("Saving...")
    print(e)
finally: 
    imgif(speed=0.1)
    Life.delall()
    