import itertools
from typing import Dict
import numpy as np
import random
import noise

DODGER_BLUE = (16, 78, 139, 255)
PALE_GREEN = (84, 139, 84, 255)
MEDIUM_GREY = (169, 169, 169, 255)
DULL_GREY = (105, 105, 105, 255)
STONE_GREY = (112, 128, 136, 255)
DARK_GREY = (79, 83, 72, 255)
SNOW_WHITE = (255, 250, 250, 255)

_COLORS = [
        DODGER_BLUE, PALE_GREEN, MEDIUM_GREY, DULL_GREY, STONE_GREY, DARK_GREY, SNOW_WHITE
]


TERRAIN_DICT = {
        'MOUNTAIN_PEAK': {
                'raw_max': 0.12,
                'int': 0,
                'color': _COLORS[6],
                'cost_in': float('inf'),
                'cost_out': 2
        },
        'MOUNTAIN_SIDE': {
                'raw_max': 0.18,
                'int': 1,
                'color': _COLORS[5],
                'cost_in': float('inf'),
                'cost_out': 1
        },
        'MOUNTAIN_BASE': {
                'raw_max': 0.23,
                'int': 2,
                'color': _COLORS[4],
                'cost_in': float('inf'),
                'cost_out': 0.5
        },
        'MOUND':        {
                'raw_max': 0.28,
                'int': 3,
                'color': _COLORS[3],
                'cost_in': 2,
                'cost_out': 0
        },
        'GRASS':         {
                'raw_max': 0.495,
                'int':     4,
                'color':   _COLORS[1],
                'cost_in':    1,
                'cost_out':   1
        },
        'SAND':          {
                'raw_max': 0.517,
                'int': 5,
                'color': _COLORS[2],
                'cost_in': 1.25,
                'cost_out': 1
        }
}


def diamond_square(noise_roughness: float, row_count: int, col_count: int) -> type[np.ndarray]:
    """
    Executes the diamond-square algorithm to generate a terrain grid.

    The diamond-square algorithm generates a grid of values using a combination of diamond and square steps. 
    It initializes the grid with zeros and sets the corner values to random numbers. 
    It then iteratively performs diamond and square steps to calculate the values for the remaining grid cells. 
    The roughness of the terrain is reduced with each iteration. 
    The resulting grid values are normalized and scaled to be in the range [0.001, 0.999].

    Args:
        noise_roughness (float): The roughness parameter for the algorithm.
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.

    Returns:
        grid (numpy.ndarray): The generated terrain grid.

    Example:
        ```python
        noise_roughness = 0.5
        row_count = 100
        col_count = 100
        terrain_grid = _diamond_square(noise_roughness, row_count, col_count)
        print(terrain_grid)
        ```
    """
    roughness = noise_roughness 
    r = row_count
    c = col_count
    # Initialize the grid with zeros using NumPy
    grid = np.zeros((r, c))

    # Set the corner values to random numbers
    grid[0, 0] = random.uniform(0.0, 1.0)
    grid[0, c - 1] = random.uniform(0.0, 1.0)
    grid[r - 1, 0] = random.uniform(0.0, 1.0)
    grid[r - 1, c - 1] = random.uniform(0.0, 1.0)
    step = c - 1
    while step > 1:
        half = step // 2
        # Diamond step
        for i in range(half, r - 1, step):
            for j in range(half, c - 1, step):
                average = (grid[i - half, j - half] + grid[i - half, j] +
                            grid[i, j - half] + grid[i, j]) / 4.0
                grid[i, j] = average + random.uniform(-1.0, 1.0) * roughness
        # Square step
        for i in range(0, r - 1, half):
            for j in range((i + half) % step, c - 1, step):
                average = (grid[(i - half + r - 1) % (r - 1), j] +
                            grid[(i + half) % (r - 1), j] +
                            grid[i, (j + half) % (c - 1)] +
                            grid[i, (j - half + c - 1) % (c - 1)]) / 4.0
                grid[i, j] = average + random.uniform(-1.0, 1.0) * roughness
                if i == 0:
                    grid[r - 1, j] = (grid[i, j] + grid[
                        r - 2, j]) / 2.0 + random.uniform(-1.0, 1.0) * roughness
        # Reduce the roughness for each iteration
        roughness /= 2.0
        # Reduce the step size for each iteration
        step //= 2
    # Normalize the grid values to be in the range [0, 1]
    max_value = np.max(grid)
    min_value = np.min(grid)
    range_value = max_value - min_value
    grid = (grid - min_value) / range_value
    # Scale and shift the normalized values to be in the range [0.001, 0.999]
    grid = grid * 0.998 + 0.001

    return grid

def perlin_noise(row_count: int, col_count: int, noise_scale: int, noise_octaves: int) -> type[np.ndarray]:
    """
    Generates Perlin noise terrain data for a grid.

    The function generates a grid of Perlin noise values using the specified dimensions (`row_count` and `col_count`), 
    noise scale (`noise_scale`), and number of octaves (`noise_octaves`). 
    It iterates over each cell in the grid and calculates the Perlin noise value using the `noise.pnoise2` function. 
    The generated terrain data is then normalized to be in the range [0, 1].

    Args:
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.
        noise_scale (int): The scale of the Perlin noise.
        noise_octaves (int): The number of octaves for the Perlin noise.

    Returns:
        numpy.ndarray: The generated terrain data grid.

    Example:
        ```python
        row_count = 100
        col_count = 100
        noise_scale = 10
        noise_octaves = 4
        terrain_data = perlin_noise(row_count, col_count, noise_scale, noise_octaves)
        print(terrain_data)
        ```
    """

    inverse_terrain_data = np.zeros((row_count, col_count))  # type: np.ndarray
    for y, x in itertools.product(range(col_count), range(row_count)):
        inverse_terrain_data[x][y] = noise.pnoise2(
            y / noise_scale, x / noise_scale,
            noise_octaves
            )
    return (inverse_terrain_data - np.min(inverse_terrain_data)) / (
            np.max(inverse_terrain_data) - np.min(inverse_terrain_data)
    )
    

def generate_terrain_dict(terrain_data_ds: type[np.ndarray], terrain_data_pn: type[np.ndarray], cell_size: int, grid_dict: Dict[str, any]):
    terrain_dict = {
        cell: {'str': None, 'raw': None, 'int': None, 'color': None, 'cost_in': None, 'cost_out': None}
        for cell in grid_dict
    }
    for cell, information in grid_dict.items():
        r, f = information['row_index'], information['col_index']
        x, y = information['coordinates']
        terrain_pn_raw = terrain_data_pn[y // cell_size][x // cell_size]
        terrain_ds_raw = terrain_data_ds[r, f]
        terrain_raw = (terrain_pn_raw + terrain_ds_raw) / 1.5
        for terrain, info in TERRAIN_DICT.items():
            if terrain_raw <= info['raw_max']:
                terrain_dict[cell]['str'] = terrain
                terrain_dict[cell]['raw'] = terrain_raw
                terrain_dict[cell]['int'] = info['int']
                terrain_dict[cell]['color'] = info['color']
                terrain_dict[cell]['cost_in'] = info['cost_in']
                terrain_dict[cell]['cost_out'] = info['cost_out']
                break
    return terrain_dict

def process_noise(noise_scale: int, noise_octaves: int, noise_roughness: float, row_count: int, col_count: int, cell_size: int, grid_dict: Dict[str, any]):
    terrain_data_ds = diamond_square(noise_roughness, row_count, col_count)
    terrain_data_pn = perlin_noise(row_count, col_count, noise_scale, noise_octaves)
    return generate_terrain_dict(
        terrain_data_ds, terrain_data_pn, cell_size, grid_dict
    )