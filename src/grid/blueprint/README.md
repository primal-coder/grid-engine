# Blueprint Package

## Description

The **Blueprint** package provides classes for generating and manipulating blueprints, which are the foundation of Grid objects created using the parent module, [grid engine](https://github.com/primal-coder/grid-engine.git).

## Usage
To use this package, import the necessary classes and functions. Here's an example:

```
from grid_engine.blueprint.grid_blueprint import BaseGridBlueprint, TerrainGridBlueprint

# Create a base grid blueprint
base_blueprint = BaseGridBlueprint(cell_size=10, grid_dimensions=(1000, 1000))

# Create a terrain grid blueprint
terrain_blueprint = TerrainGridBlueprint(cell_size=10, grid_dimensions=(1000, 1000), noise_scale=25, noise_octaves=38, noise_roughness=0.35)

# Save a blueprint
base_blueprint.save_blueprint()

# Load a blueprint
loaded_blueprint = BaseGridBlueprint.load_blueprint(1)
```

# Classes
## BaseGridBlueprint

The BaseGridBlueprint class represents a base blueprint. It provides methods for initializing, setting the dimensions and size of the grid, and accessing and modifying the grid's cells and layers. The coordinates of the cells, by default, extend from the bottom left corner of the grid. The grid is divided into quadrants, which are used to facilitate the processing of the grid. The grid is also represented as a graph, which is used to facilitate pathfinding.

### Properties
- cell_size: Returns the size of a cell.
- grid_dimensions: Returns the dimensions of the grid.
- col_count: Returns the number of columns in the grid.
- grid_width: Returns the width of the grid.
- row_count: Returns the number of rows in the grid.
- grid_height: Returns the height of the grid.
- rank: Returns the rank(rows) of the grid.
- file: Returns the file(columns) of the grid.
- cell_list: Returns the list of cells.
- array: Returns the array of cells.
- dictGrid: Returns the dictionary of cells.
- dictTerrain: Returns the dictionary of terrain information.
- cell_coordinates: Returns the coordinates of the cells.
- quadrants: Returns the quadrants of the grid.
- graph: Returns the graph of the grid.

## TerrainGridBlueprint

The TerrainGridBlueprint class represents a terrain grid blueprint. It inherits from the BaseGridBlueprint class and adds methods for initializing the terrain layer of the blueprint and adjusting the passability of cells based on terrain.

### Properties
Inherits all properties from the BaseGridBlueprint class.

# Extras 

The grid_blueprint makes use of the following modules and files:

## grid_processing

The grid_processing module is used by grid_blueprint to facilitate the processing of grids. It provides functions for generating many of the characteristics of the blueprint object.

### Functions

- generate_row_strings: Generates a list of row strings. (i.e. ['a', 'b', 'c', ... , 'z', 'aa', 'ab', ... , 'az', 'ba', 'bb', ...])
- generate_column_strings: Generates a list of column strings. Column strings are padded to 5 characters. (i.e. ['00001', '00002', '00003', ... , '00009', '00010', '00011', ... , '00099', '00100', '00101', ...])
- generate_cell_strings: Generates a list of cells. (i.e. ['a00001', 'a00002', 'a00003', ... , 'a00009', 'a00010', 'a00011', ... , 'a00099', 'a00100', 'a00101', ...])
- get_cell_coordinates: Returns the coordinates of a cell.
- get_grid_dict: Returns a dictionary of cells.
- generate_quadrant_coordinates: Calculates the coordinates of the quadrants for the grid.
- get_quadrant_indices: Assigns quadrant indices.
- generate_adjacency: Generates the adjacency data for the grid.
- get_graph: Returns the graph of the grid.
- process_grid: Performs all grid processing functions and returns a dictionary containing the processed grid data.

## terrain_processing

The terrain_processing module is used by grid_blueprint to facilitate the processing of terrain data. It provides functions for generating the terrain layer of the blueprint object.

### Functions

- load_terrain: Loads terrain data from a file.
- diamond_square: Generates a height map using the diamond-square algorithm.
- perlin_noise: Generates a height map using the perlin noise algorithm.
- generate_terrain_dict: Generates a dictionary of terrain data.

## terrains.json

The terrains.json file contains the terrain data used by the terrain_processing module. It is a dictionary of terrain types. The data is structured as follows:

```
{
    "terrain_type": {
        "raw_max" : 0.0,
        "int": 0,
        "color": "COLOR_IDENTIFIER",
        "cost_in": 0,
        "cost_out": 0,
        "char": ""
    }
}
```

You can add or remove terrain types from this file to change the terrain types available to the terrain_processing module. Colors can be specified using a color identifier (i.e. "GRASS_GREEN") or a RGBA tuple (i.e (255, 255, 255, 255)).