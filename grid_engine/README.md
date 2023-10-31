# Grid

The **Grid** submodule provides numerous classes and functions for generating and manipulating grids. Each grid is composed of [Cell](#Cell) objects and is defined by a [Blueprint](#Blueprint). A grid can be generated from a blueprint, loaded from a file, or created manually. It can also be pickled for later use. It cab be rendered as a 2D image, an animated GIF or an ASCII string. Grids provide a number of relevant methods for pathfinding, cell manipulation, and more.

## Usage

To use this submodule, import the necessary classes and functions. Here's an example:

```python
import gridengine
from gridengine import Grid

# Create a grid
grid = Grid(cell_size=10, grid_dimensions=(1000, 1000))