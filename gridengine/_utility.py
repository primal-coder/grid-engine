# This file contains utility functions for the grid engine.

# Path: grid-engine/utility.py
import os as _os
import sys as _sys

_module_name = 'gridengine'
_install_dir = _os.path.dirname(_sys.modules[_module_name].__file__)
# Define the directory for saving generated grids.
saves_dir = f'{_install_dir}/saves/'

# Define the function for generating grid images
def generate_images(dimensions, cdata, cell_size, grid_id, animate=False):
    print('Generating grid image ...')
    print('Importing pillow ...')
    from PIL import Image as _Image, ImageDraw as _ImageDraw
    import random
    print('Preparing raw image ...')
    image = _Image.new('RGB', dimensions, (255, 255, 255))
    draw = _ImageDraw.Draw(image)
    print('Counting cells ...')
    total = len(cdata)
    print(f'Total cells: {total}')
    cells = cdata
    print('Shuffling cells ...')
    random.shuffle(cells)
    if animate:
        frames = []
        for count in range(0, total, 100):
            for cell in zip(range(100), cells[count:count+100]):
                print(f'Drawing cells {count+1}-{min(count+100, total)} ... {round(((count+100)/total)*100)}%', end='\r')
                x = cell[0]
                y = cell[1]
                color = cell[2]
                draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
                
            frames.append(image.copy())

        print('Saving grid animation ...')
        frames[0].save(f'{saves_dir}{grid_id}/grid.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1, loop=0)
    else:
        for i, cell in enumerate(cells):
            print(f'Drawing cells {round((i/total)*100)}%', end='\r')
            x = cell[0]
            y = cell[1]
            color = cell[2]
            draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
        print('Cells drawn.')
    print('Saving grid image ...')
    image.save(f'{saves_dir}{grid_id}/grid.png')
    print(f'Grid ID: {grid_id}')
    
    
# Define the QuietDict class

from typing import Union as _Union

class QuietDict:
    def __init__(self):
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key: _Union[str, int]):
        if isinstance(key, str):
            return self.items[key]
        elif isinstance(key, int):
            return list(self.items.values())[key]
        else:
            raise TypeError("Key must be of type str or int")

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, key):
        return key in self.items

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self.items)} items)"

    def __sub__(self, other):
        if isinstance(other, QuietDict):
            for key, value in self.items.copy().items():
                if key in other:
                    del self[key]

    def update(self, other=None, **kwargs):
        if other:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def values(self):
        return list(self.items.values())