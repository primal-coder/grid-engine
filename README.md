# grid-engine

## Description

The **grid-engine** package provides classes for generating and manipulating grids. The grid-engine package is divided into two subpackages: **grid blueprint** and **grid**. The **grid blueprint** subpackage provides classes for generating and manipulating blueprints, which are the foundation of Grid objects created using this module. The **grid** subpackage provides classes for generating and manipulating Grid objects, which are the foundation of the grid engine.

## Usage

To use this package, import the necessary classes and functions. Here's an example:

```python
import grid_engine
from grid_engine import grid

# Create a grid
grid = grid.Grid(cell_size=10, grid_dimensions=(1000, 1000))

# Save a grid
grid.save_grid()

# Load a grid
loaded_grid = grid.Grid.load_grid(1)
```

grid-engine also provides a command line interface. To use it, run the following command:

```bash
python -m grid_engine --help

# Output:
# usage: grid [-h] [-i] [-b BLUEPRINT] [--ascii] [-l LOAD] [-t] [-ns NOISE_SCALE] [-no NOISE_OCTAVES] [-nr NOISE_ROUGHNESS] [-r ROWS] [-c COLUMNS] [-s SIZE] [-S] [-T TYPE] [-v]

# Generate a visualized grid from a blueprint. For producing a blueprint, see the blueprint module.

# options:
#   -h, --help            show this help message and exit
#   -i, --interactive     Run an interactive session
#   -b BLUEPRINT, --blueprint BLUEPRINT
#                         Load a blueprint from a file
#   --ascii               Print the grid as ascii
#   -l LOAD, --load LOAD  Load a grid from a file
#   -t, --terrain         Whether to generate terrain with the grid.
#   -ns NOISE_SCALE, --noise-scale NOISE_SCALE
#                         Noise scale
#   -no NOISE_OCTAVES, --noise-octaves NOISE_OCTAVES
#                         Noise octaves
#   -nr NOISE_ROUGHNESS, --noise-roughness NOISE_ROUGHNESS
#                         Noise roughness
#   -r ROWS, --rows ROWS  Number of rows in the grid
#   -c COLUMNS, --columns COLUMNS
#                         Number of columns in the grid
#   -s SIZE, --size SIZE  Size of each cell in the grid
#   -S, --save            Save the grid object to a file
#   -T TYPE, --type TYPE  Type of file to save the grid as
#   -v, --verbose         Verbose output
```

# Examples

The following examples demonstrate the use of the grid-engine package.

### CLI

The following command:

```bash
python -m grid -v -S -t -ns 580 -no 93 -nr 0.47 -r 450 -c 800 -s 2 
```

Will produce the following output:
    
    ```bash
    Generating blueprint with cell size 2, 450 rows and 800 columns. Total_cells: 360000 ...
    Success! Blueprint generated. Dimensions: (1600, 900)
    Building grid from blueprint ...
    Finding landmasses ...
    Separating islands from landmasses ...
    Done.
    Finding start to river ...
    Found largest landmass: 3 with 239606 cells
    Start cell: pb00527(443, 526)
    Building river ...
    River steps: 200
    done
    Success! Grid generated.
    Pickling grid ...
    Success!
    Pickling blueprint ...
    Success!
    Generating grid image ...
    Importing pillow ...
    Preparing raw image ...
    Counting cells ...
    Total cells: 360000
    Shuffling cells ...
    Cells drawn.s 100%
    Saving grid image ...
    Grid ID: ee9e4
    ```

The following image is the result of the above command:

![grid](src/grid/saves/ee9e4/grid.png)
*The river generation algorithm is not perfect. I am currently working on improving it.*

The above command will also produce the following files:

- `grid.ee9e4.pickle`: A pickled Grid object.
- `blueprint.ee9e4.pickle`: A pickled TerrainGridBlueprint object.

```python
import grid_engine
from grid_engine import grid

# Load the ee9e4 grid(assuming you've not generated any other grids)
ee9e4 = grid.load_grid(0)

print(ee9e4.grid_id)
# output: 'fb16965aa77f44138dd6149b823ee9e4'

# Get a random cell
cellA = ee9e4.random_cell(attr=('passable', True))

# Get another
cellB = ee9e4.random_cell(attr=('passable', True))

# Get a path from cellA to cellB
path, cost = ee9e4.get_path(cellA, cellB)
print(path)
```