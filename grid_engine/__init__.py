from . import _grid as grid
from . import _blueprint as blueprint
from . import _cell as cell
from . import _grid_object as grid_object

def create_grid(cell_size=None, dimensions=None):
    if cell_size is None:
        cell_size = 1
    if dimensions is None:
        dimensions = (1000, 1000)
    g = grid.Grid(cell_size=cell_size, dimensions=dimensions)
    return g