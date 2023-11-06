# Grid

The **Grid** submodule provides numerous classes and functions for generating and manipulating grids. Each grid is composed of [Cell](_cell/cell.py) objects and is defined by a [Blueprint](_blueprint/_grid_blueprint.py). A grid can be generated from a blueprint, loaded from a file, or created manually. It can also be pickled for later use. It cab be rendered as a 2D image, an animated GIF or an ASCII string. Grids provide a number of relevant methods for pathfinding, cell manipulation, and more.

## Usage

To use this submodule, import the necessary classes and functions. Here's an example:

```python
import gridengine
from gridengine import Grid

# Create a grid
grid = Grid(cell_size=2, grid_dimensi1ons=(5000, 2500))

# Save a grid
Grid.save_grid(grid)

# get two random cells
cellA, cellB = [grid.random_cell(attr='passable', True) for _ in range(2)]

# Get the shortest path between the two cells
path, cost = grid.get_path(cellA, cellB)
```
