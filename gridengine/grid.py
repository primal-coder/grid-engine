from __future__ import annotations

from .terraformer import *
from .cell import *
from .blueprint import *
from .utility import QuietDict as _QuietDict

import pickle

import random

import heapq

import numpy as np

from pymunk import Vec2d

from abc import ABC

from uuid import uuid4

from subprocess import call

from collections import deque

from random import choice

from typing import Optional, Union

RIVER_BLUE = (18, 70, 132, 255)
RIVERBANK_BROWN = (32, 89, 31, 255)

saves_dir = '/devel/fresh/envs/grid-engine/src/grid/saves/'

DIRECTIONS = {'N': 'up', 'NE': 'up_right', 'E': 'right', 'SE': 'down_right', 'S': 'down', 'SW': 'down_left', 'W': 'left', 'NW': 'up_left'}

def clear():
    call('clear')

def get_vector_direction(pointa, pointb):
    pointa, pointb = Vec2d(pointa[0], pointa[1]), Vec2d(pointb[0], pointb[1])
    angle_degrees = (pointb - pointa).angle_degrees
    angle_degrees = int(angle_degrees)
    angle_degrees %= 360
    cardinal_directions = {
            "E":  range(337, 360) or range(23),
            "NE": range(23, 68),
            "N":  range(68, 113),
            "NW": range(113, 158),
            "W":  range(158, 203),
            "SW": range(203, 248),
            "S":  range(248, 293),
            "SE": range(293, 338)
    }
    return next(
            (
                    direction
                    for direction, angle_range in cardinal_directions.items()
                    if angle_degrees in angle_range
            ),
            "Invalid angle",
    )


def extract_cell_data(grid):
    """Accepts a grid object and returns only the necessary data to draw the cells"""
    cell_data = []
    for c, cell in grid.cells.items.items():
        cdata = [cell.x, cell.y, cell.terrain_color]
        cell_data.append(cdata)
    return cell_data

def delete_grid(grid: Grid):
    """Deletes the grid object from memory in order to avoid OOM events"""
    del grid

def save_grid(grid: Grid):
    import os
    os.chdir(f'{saves_dir}')
    if not os.path.exists(f'{grid.grid_id[-5:]}'):
        os.makedirs(f'{grid.grid_id[-5:]}')
            
    with open(f'{grid.grid_id[-5:]}/grid.{grid.grid_id[-5:]}.pkl', 'wb') as f:
        pickle.dump(grid, f)
        
def load_grid(num: int):
    import os
    os.chdir(f'{saves_dir}')
    save_dir = f'{os.listdir(".")[num]}'
    with open(f'{save_dir}/grid.{save_dir[-5:]}.pkl', 'rb') as f:
        return pickle.load(f)

class Cells(_QuietDict):
    pass

class AbstractGrid(_QuietDict, ABC):
    """The abstract base class for all grids."""
    _grid_id = None
    _with_terrain = None
    _blueprint = None
    _terraformer = None
    _grid_array = None
    _dictTerrain = None
    _grid_plan = None
    _init_cell_size = None
    _cell_size = None
    _cells = None
    _rows = None
    _cols = None
    _quadrants = None
    _first_col = None
    _last_col = None
    _first_row = None
    _last_row = None
    _selection = None
    
    def __init__(
        self, 
        blueprint = None, 
        cell_size = None, 
        dimensions = None, 
        noise_scale = None, 
        noise_octaves = None, 
        noise_roughness = None
    ) -> None:
        super(AbstractGrid, self).__init__()
    
    @property
    def grid_id(self) -> str:
        """The unique identifier of the grid."""
        return self._grid_id if self._grid_id is not None else print('Grid ID not set.')
    
    @grid_id.setter
    def grid_id(self, grid_id: Optional[str] = None) -> None:
        self._grid_id = grid_id if grid_id is not None else uuid4().hex
        
    @property
    def with_terrain(self) -> bool:
        """Whether or not the grid has terrain."""
        return self._with_terrain
    
    @with_terrain.setter
    def with_terrain(self, with_terrain: Optional[bool] = None) -> None:
        self._with_terrain = with_terrain if with_terrain is not None else True
        
    @property
    def blueprint(self) -> Optional[type[Blueprint.AbstractGridBlueprint]]:
        """The blueprint of the grid."""
        return self._blueprint
    
    @blueprint.setter
    def blueprint(self, blueprint: Optional[type[Blueprint.AbstractGridBlueprint]] = None) -> None:
        if blueprint is not None:
            self._blueprint = blueprint
        
    @property
    def terraformer(self) -> type[Terraformer]:
        """The terraformer of the grid."""
        return self._terraformer
        
    @property
    def grid_array(self) -> np.ndarray:
        """The grid array of the grid."""
        return self._grid_array
    
    @grid_array.setter
    def grid_array(self, grid_array: Optional[np.ndarray] = None) -> None:
        self._grid_array = grid_array
        
    @property
    def dictTerrain(self) -> Optional[dict[str, dict[str, Any]]]:
        """The dictionary of terrain data for the grid. Provided by the blueprint."""
        return self._dictTerrain
    
    @dictTerrain.setter
    def dictTerrain(self, dictTerrain: Optional[dict[str, dict[str, Any]]] = None) -> None:
        self._dictTerrain = dictTerrain
        
    @property
    def grid_plan(self) -> Optional[dict[str, dict[str, Any]]]:
        """The dictionary of grid data for the grid. Provided by the blueprint."""
        return self._grid_plan
    
    @grid_plan.setter
    def grid_plan(self, grid_plan: Optional[dict[str, dict[str, Any]]] = None) -> None:
        self._grid_plan = grid_plan
        
    @property
    def init_cell_size(self):
        """The initial cell size of the grid."""
        return self._init_cell_size
    
    @init_cell_size.setter
    def init_cell_size(self, init_cell_size: Optional[int] = None) -> None:
        self._init_cell_size = init_cell_size
        
    @property
    def cell_size(self) -> int:
        """The cell size of the grid."""
        return self._cell_size
    
    @cell_size.setter
    def cell_size(self, cell_size: Optional[int] = None) -> None:
        self._cell_size = cell_size
        
    @property
    def cells(self) -> type[Cells]:
        """A subclass of QuietDict representing all cells in the grid. Keys are cell designations, values are Cell objects."""
        return self._cells
    
    @cells.setter
    def cells(self, cells: Optional[type[Cells]] = None) -> None:
        self._cells = cells
        
    @property
    def rows(self) -> list[list[Cell,]]:
        """A dynamically generated list of all rows in the grid. The list contains Row objects, which are dynamically generated lists of Cell objects."""
        return self._rows
    
    @rows.setter
    def rows(self, rows: Optional[list[list[Cell,]]] = None) -> None:
        self._rows = rows
        
    @rows.deleter
    def rows(self) -> None:
        del self._rows
        
    @property
    def cols(self) -> list[list[Cell,]]:
        """A dynamically generated list of all columns in the grid. The list contains Column objects, which are dynamically generated lists of Cell objects."""
        return self._cols
    
    @cols.setter
    def cols(self, cols: Optional[list[list[Cell,]]] = None) -> None:
        self._cols = cols
        
    @cols.deleter
    def cols(self):
        del self._cols
        
    @property
    def quadrants(self) -> list[type[QuietDict]]:
        """A dynamically generated list of all quadrants in the grid. The list contains Quadrant objects, which are subclasses of QuietDict.
        The quadrant data can be accessed by quadrant number, e.g. `grid.quadrants.quad0`.
        
        grid.quadrants.quad0['cell_count']/[0] returns the number of cells in the quadrant.
        grid.quadrants.quad0['cells']/[1] returns a list of all cells in the quadrant.
        """
        return self._quadrants
    
    @quadrants.setter
    def quadrants(self, quadrants: Optional[list[type[QuietDict]]] = None) -> None:
        self._quadrants = quadrants

    @quadrants.deleter
    def quadrants(self):
        del self._quadrants

    @property
    def first_col(self):
        """The first column in the grid."""
        return self._first_col
    
    @first_col.setter
    def first_col(self, value):
        self._first_col = value
    
    @first_col.deleter
    def first_col(self):
        del self._first_col
        
    @property
    def last_col(self):
        """The last column in the grid."""
        return self._last_col
    
    @last_col.setter
    def last_col(self, value):
        self._last_col = value
        
    @last_col.deleter
    def last_col(self):
        del self._last_col
        
    @property
    def first_row(self):
        """The first row in the grid."""
        return self._first_row
    
    @first_row.setter
    def first_row(self, value):
        self._first_row = value
        
    @first_row.deleter
    def first_row(self):
        del self._first_row
        
    @property
    def last_row(self):
        """The last row in the grid."""
        return self._last_row
    
    @last_row.setter
    def last_row(self, value):
        self._last_row = value
        
    @last_row.deleter
    def last_row(self):
        del self._last_row
        
    @property
    def selection(self):
        return self._selection
    
    @selection.setter
    def selection(self, value):
        self._selection = value
                
class Grid(AbstractGrid, ABC):
    """The grid object. Contains all cells, rows, columns, and quadrants."""
    def __init__(
            self,
            blueprint: Optional[type[Blueprint.AbstractGridBlueprint]] = None,
            cell_size: Optional[int] = None,
            dimensions: Optional[tuple[int, int]] = None,
            with_terrain: Optional[bool] = None,
            noise_scale: Optional[float] = None,
            noise_octaves: Optional[int] = None,
            noise_roughness: Optional[float] = None            
    ):
        """
        Initializes the grid object. If no blueprint is provided, a terrain grid blueprint is generated.
        
        Args:
            blueprint (Optional[type[Blueprint.AbstractGridBlueprint]], optional): The blueprint of the grid. Defaults to None.
            cell_size (Optional[int], optional): The size of each cell in the grid. Defaults to None.
            dimensions (Optional[tuple[int, int]], optional): The dimensions of the grid. Defaults to None.
            with_terrain (Optional[bool], optional): Whether or not the grid has terrain. Defaults to None.
            noise_scale (Optional[float], optional): The scale of the Perlin noise. Defaults to None.
            noise_octaves (Optional[int], optional): The number of octaves for the Perlin noise. Defaults to None.
            noise_roughness (Optional[float], optional): The roughness of the Perlin noise. Defaults to None.
        """
        self.grid_id = uuid4().hex if blueprint is None else blueprint.blueprint_id
        self.with_terrain = with_terrain if with_terrain is not None else True
        self.blueprint = blueprint if blueprint is not None else Blueprint.TerrainGridBlueprint(cell_size, dimensions, self.grid_id, noise_scale, noise_octaves, noise_roughness) if self._with_terrain else BaseGridBlueprint(cell_size, dimensions, self.grid_id)
        self.grid_array = self.blueprint.array
        self.dictTerrain = self.blueprint.dictTerrain
        self.grid_plan = self.blueprint.dictGrid
        super(Grid, self).__init__()
        self._init_cell_size = cell_size if cell_size is not None else self.blueprint._cell_size
        self.cell_size = cell_size if cell_size is not None else self.blueprint._cell_size
        self.cells = Cells()
        for cell in self.grid_plan.keys():
            self.cells[cell] = Cell(cell, parentgrid=self)
            self.update({cell: self.cells[cell]})
        self.rows = None
        self.cols = None
        self.quadrants = None
        self._set_up()
        self._first_col = None
        self._last_col = None
        self._first_row = None
        self._last_row = None
        self._get_first_last()
        self.selection = None
        self.landmasses, self.islands = self._find_landmasses()
        self.landmass_count = len(self.landmasses)
        self.island_count = len(self.islands)
        self._set_landmass_cells()
        
        for row in self.rows:
            row.row_index = self.rows.index(row)
        for col in self.cols:
            col.col_index = self.cols.index(col)
        self._terraformer = Terraformer(self)
        # self.terraformer.set_rivers(1)

    def __getstate__(self):
        state = self.__dict__.copy()
        nonattrs = ['_cols', '_rows', '_quadrants', '_first_col', '_first_row', '_last_col', '_last_row']
        for nonattr in nonattrs:
            del state[nonattr]
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)


    def _get_first_last(self):
        """Sets the first and last rows and columns in the grid.
        The values are collected from the rows and cols attributes by index.
        """
        self._first_col = self.cols[0]
        self._last_col = self.cols[-1]
        self._first_row = self.rows[0]
        self._last_row = self.rows[-1]
    
    def _set_up(self):
        """Sets up the grid object."""
        self._set_up_rank()
        self._set_up_file()
        self._set_up_quadrants()
        self._set_up_cells()

    def _set_up_rank(self):
        """Sets up the rank attribute. A `rows` attribute is asigned a type value, with a base of type[list]. 
        The `rows` attribute is then instantiated. The `rows` attribute is then assigned an attribute for each row in the grid,
        with a base of type[list]. Each row attribute is then instantiated. Finally, each row attribute is appended to the `rows` object.
        
        Effectively, this creates a list of lists, with each list representing a row in the grid. But, each row is accessible by attribute.
        
        Example:
            ```grid.rows.rowa``` returns the first row in the grid.
            ```grid.rows[0]``` returns the first row in the grid.
        """
        setattr(self, 'rows', type('rows', (list,), {'blueprint': self.blueprint}))
        exec('self.rows = self.rows()')
        for height, row in enumerate(self.blueprint._rank):
            setattr(self.rows, f'row{row}',
                    type('Row', (list,), {'blueprint': self.blueprint, 'height': height * self.cell_size}))
            exec(f'self.rows.row{row} = self.rows.row{row}()')
            exec(f'self.rows.append(self.rows.row{row})')

    def _set_up_file(self):
        """Sets up the file attribute. A `cols` attribute is asigned a type value, with a base of type[list].
        The `cols` attribute is then instantiated. The `cols` attribute is then assigned an attribute for each column in the grid,
        with a base of type[list]. Each column attribute is then instantiated. Finally, each col attribute is appended to the `cols` object.
        
        Effectively, this creates a list of lists, with each list representing a column in the grid. But, each column is accessible by attribute.
        
        Example:
            ```grid.cols.col00001``` returns the first column in the grid
            ```grid.cols[0] returns the first column in the grid
            """
        setattr(self, 'cols', type('cols', (list,), {'blueprint': self.blueprint}))
        exec('self.cols = self.cols()')
        for width, col in enumerate(self.blueprint._file):
            setattr(self.cols, f'col{col}',
                    type('Column', (list,), {'blueprint': self.blueprint, 'width': width * self.cell_size}))
            exec(f'self.cols.col{col} = self.cols.col{col}()')
            exec(f'self.cols.append(self.cols.col{col})')

    def _set_up_cells(self):
        """Append each cell to its row and column created in `_set_up_rank` and `_set_up_file` respectively."""
        for d, c in self.cells.items.items():
            getattr(self.rows, f'row{d[:-5]}').append(c)
            getattr(self.cols, f'col{d[-5:]}').append(c)
 
    def _set_up_quadrants(self):
        """Sets up the quadrants attribute. A `quadrants` attribute is asigned a type value, with a base of type[list].
        The `quadrants` attribute is then instantiated. The `quadrants` attribute is then assigned an attribute for each quadrant in the grid,
        with a base of type[QuietDict]. Each quadrant attribute is then instantiated. Each quadrant attribute is appended to the `quadrants` object.
        Finally, each quadrant attribute is updated with the quadrant data from the blueprint.
        
        Example:
            ```grid.quadrants.quad0``` returns the first quadrant in the grid.
            ```grid.quadrants.quad0['cell_count']``` returns the number of cells in the first quadrant.
            ```grid.quadrants.quad0['cells']``` returns a list of all cells in the first quadrant.
        """
        setattr(self, 'quadrants', type('quadrants', (list,), {}))
        exec('self.quadrants = self.quadrants()')
        for quadrant, info in self.blueprint.quadrants.items():
            setattr(self.quadrants, f'quad{quadrant}',
                    type('Quadrant', (_QuietDict,), {'__int__': lambda self: int(quadrant)}))
            exec(f'self.quadrants.quad{quadrant} = self.quadrants.quad{quadrant}()')
            exec(f'self.quadrants.append(self.quadrants.quad{quadrant})')
            exec(f'self.quadrants.quad{quadrant}.update({info})')
            
    def get_cell(self, cell_designation: Optional[str] = None) -> Optional[Cell]:
        """Returns a cell object by its designation."""
        try:
            return self.cells[cell_designation]
        except KeyError:
            return None

    def get_cell_by_index(self, index: Optional[int] = None) -> Optional[Cell]:
        """Returns a cell object by its index in the cell list."""
        try:
            return self.cells[self.blueprint._cell_list[index]]
        except KeyError:
            return None

    def get_cell_by_relative_indices(self, reference: Optional[tuple[int, int]] = None, indices: Optional[tuple[int, int]] = None):
        """Returns a cell object by its relative indices from a reference cell.
        
        Args:
            reference (Optional[tuple[int, int]], optional): The reference cell. Defaults to None.
            indices (Optional[tuple[int, int]], optional): The relative indices from the reference cell. Defaults to None.
            
        Returns:
            Optional[Cell]: The cell object.
            
        Example:
            ```grid.get_cell_by_relative_indices((0, 0), (1, 0))``` returns the cell directly below the reference cell.
        """
        ref = Vec2d(*reference)
        ind = Vec2d(*indices)
        r, f = (ref + ind).int_tuple
        r, f = max(0, r), max(0, f)
        r, f = min(r, self.blueprint.row_count - 1), min(f, self.blueprint.col_count - 1)
        return self.grid_array[r, f, 0]['designation']

    def get_nearest_cell_with(self, cella: Union[str, Cell], attr_name: str, attr_val: Any):
        """Returns the nearest cell with the specified attribute value.
        
        Args:
            cella (Union[str, Cell]): The reference cell.
            attr_name (str): The attribute name.
            attr_val (Any): The attribute value.
            
        Returns:
            Cell: The nearest cell with the specified attribute value.
            
        Example:
            ```grid.get_nearest_cell_with('a00001', 'passable', True)``` returns the nearest passable cell to cell 'a00001'.
        """
        nearest = {'cell': None, 'distance': None}
        count = 0
        for cellb in self.cells.values():
            if not count:
                nearest['cell'] = [cellb]
                nearest['distance'] = self.get_distance(cella, cellb.designation)
                count += 1
                continue
            else:            
                if getattr(cellb, attr_name) == attr_val:
                    distance = self.get_distance(cella, cellb.designation)
                    if nearest['distance'] > distance:
                        nearest['cell'] = [cellb]
                        nearest['distance'] = distance
                    elif nearest['distance'] == distance:
                        nearest['cell'].append(cellb)

            count += 1
        if len(nearest['cell']) == 1:
            return nearest['cell'][0]
        else:
            return random.choice(nearest['cell'])
    
    def get_row_by_index(self, index: Optional[int] = None) -> Optional[list[Cell,]]:
        """Returns a row by its index in the row list."""
        return self.blueprint.rank[index]

    def get_row_by_height(self, height: Optional[int] = None) -> Optional[list[Cell,]]:
        """Returns a row by its height(y coordinate)."""
        if self.cell_size == 1:
            return height
        for i in range(len(self.rows)):
            if self.rows[i].height <= height < self.rows[i + 1].height:
                return self.get_row_by_index(i)

    def get_row_by_name(self, row_name: Optional[str] = None) -> Optional[list[Cell,]]:
        """Returns a row by its name."""
        return getattr(self.rows, f'row{row_name}')
    
    def get_col_by_index(self, index: Optional[int] = None) -> Optional[list[Cell,]]:
        """Returns a column by its index in the column list."""
        return self.blueprint.file[index]
    
    def get_col_by_width(self, width: Optional[int] = None) -> Optional[list[Cell,]]:
        """Returns a column by its width(x coordinate)."""
        if self.cell_size == 1:
            return width
        for i in range(len(self.cols)):
            if i == len(self.cols) - 1 or self.cols[i].width <= width < self.cols[i + 1].width:
                return self.get_col_by_index(i)
                    
    def get_col_by_name(self, col_name: Optional[str] = None) -> Optional[list[Cell,]]:
        """Returns a column by its name."""
        return getattr(self.cols, f'col{col_name}')
    
    def get_cell_by_position(self, x: Optional[int] , y: Optional[int]) -> Optional[Cell]:
        """Returns a cell by its position on the grid."""
        r = self.get_row_by_height(y)
        f = self.get_col_by_width(x)
        return self.get_cell(f'{r}{f}')
    
    def get_cell_by_rank_file(self, rank: Optional[int], file: Optional[int]) -> Optional[Cell]:
        """Returns a cell by its rank and file. Rank and file are the indices of the row and column respectively."""
        # r = self.get_row_by_index(rank)
        # f = self.get_col_by_index(file)
        # for cell in r:
        #     if cell in f:
        #         return cell
        return self.cells[self.grid_array[rank, file, 0]['designation']]

    def random_cell(self, attr: Optional[tuple[str, Any]] = None, attrs: Optional[tuple[tuple[str, any]]] = None, landmass_index: Optional[int] = None) -> Optional[Cell]:
        """Returns a random cell. If an attribute is provided, the cell must have that attribute. If multiple attributes are provided,
        the cell must have all attributes. If a landmass index is provided, the cell must be in that landmass.
        
        Args:
            attr (Optional[tuple[str, Any]], optional): The attribute. Defaults to None.
            attrs (Optional[tuple[tuple[str, any]]], optional): The attributes. Defaults to None.
            landmass_index (Optional[int], optional): The landmass index. Defaults to None.
            
        Example:
            ```grid.random_cell(attr=('passable', True))``` returns a random passable cell.
            ```grid.random_cell(attrs=(('passable', True), ('terrain_str', 'GRASS')))``` returns a random passable cell with terrain string 'GRASS'.
            ```grid.random_cell(landmass_index=0)``` returns a random cell in the first landmass.
        """
        if landmass_index is not None:
            cell = choice(self.landmasses[landmass_index]['landmass_cells'])
        elif attrs is not None:
            cell = self.cells[choice(self.blueprint.cell_list)]
            while any(getattr(cell, attr[0]) != attr[1] for attr in attrs):
                cell = self.cells[choice(self.blueprint.cell_list)]
        elif attr is not None:
            cell = self.cells[choice(self.blueprint.cell_list)]
            while getattr(cell, attr[0]) != attr[1]:
                cell = self.cells[choice(self.blueprint.cell_list)]
        else:
            cell = self.cells[choice(self.blueprint.cell_list)]
        return cell
    
    def random_row(self) -> Optional[list[Cell,]]:
        """Returns a random row."""
        return choice([getattr(self.rows, f'row{r}') for r in self.blueprint.rank])

    def random_col(self) -> Optional[list[Cell,]]:
        """Returns a random column."""
        return choice([getattr(self.cols, f'col{c}') for c in self.blueprint.file])

    def get_adjacent(self, cell_designation: Optional[str] = None) -> Optional[list[Cell,]]:
        """Returns a list of all adjacent cells to the specified cell."""
        return [self.cells[adj] for adj in self.cells[cell_designation].adjacent]

    # def get_neighbors(self, cell_designation: Optional[str] = None) -> Optional[list[Cell,]]:
    #     return [self.cells[adj].occupant for adj in self.cells[cell_designation].adjacent if
    #             self.cells[adj].occupant is not None]

    def get_distance(self, cella: Optional[str] = None, cellb: Optional[str] = None,
                     measurement: Optional[str] = None) -> Optional[int]:
        """Returns the distance between two cells. If no measurement is provided, the distance is in units. If measurement is 'cells',
        the distance is in cells."""
        m = measurement if measurement is not None else "units"
        if m == "units":
            return self._heuristic(cella, cellb)
        if m == "cells":
            return self._heuristic(cella, cellb) // self.cell_size

    def get_path(
            self,
            cella: Optional[Union[Cell, str]] = None,
            cellb: Optional[Union[Cell, str]] = None
    ) -> Optional[list[Cell,]]:
        """Returns a list of cells representing the shortest path between two cells and the cost of the path."""
        if isinstance(cella, Cell):
            cella = cella.designation
        if isinstance(cellb, Cell):
            cellb = cellb.designation
        path, cost = self._astar(cella, cellb)
        path.remove(cella)
        for count, step in enumerate(path):
            if not self[step].passable:
                path = path[:count]
                break
        return path, cost
    
    def get_direction(
            self,
            cella: Optional[Union[Cell, str]] = None,
            cellb: Optional[Union[Cell, str]] = None
    ) -> Optional[str]:
        """Returns the direction from cell A to cell B."""
        if isinstance(cella, Cell):
            cella = cella.designation
        if isinstance(cellb, Cell):
            cellb = cellb.designation
        cellA = self.cells[cella]
        if cellb in cellA.adjacent:
            cellB = self.cells[cellb]
            for direction, adjacent in DIRECTIONS.items():
                if cellB == getattr(cellA, adjacent):
                    return direction
        return get_vector_direction(self.cells[cella].coordinates, self.cells[cellb].coordinates)

    def get_area(self, center_cell: Optional[Union[Cell, str]] = None, radius: Optional[int] = None):
        """Returns a list of cells in the area around the center cell."""
        area_zone = []

        if isinstance(center_cell, str):
            center_cell = self.cells[center_cell]

        i1 = self.cols.index(center_cell.col)
        i2 = center_cell.col.index(center_cell)

        min_i1 = max(i1 - radius, 0)
        max_i1 = min(i1 + radius, len(self.cols) - 1)

        min_i2 = max(i2 - radius, 0)
        max_i2 = min(i2 + radius, len(center_cell.col) - 1)

        for i in range(min_i1, max_i1 + 1):
            col = self.cols[i]
            area_zone.extend(col[j] for j in range(min_i2, max_i2 + 1))
        area_zone = set(area_zone)
        return sorted(area_zone, key=lambda cell: cell.designation)
    
    def get_sub(self, bottom_left, top_right):
        return [
            cell
            for cell in self.cells.values()
            if bottom_left[0] <= cell.row_index <= top_right[0]
            and bottom_left[1] <= cell.col_index <= top_right[1]
        ]

    def _get_landmass_cells(self, center_cell):
        """
        Finds and returns all cells belonging to the same landmass as the center cell.
        Uses the passable attribute of each instance of cell to determine if it belongs
        to the landmass group.

        Args:
            center_cell: The center cell around which to search for the landmass.

        Returns:
            List of cells belonging to the same landmass as the center cell.
        """
        landmass_cells = set()
        visited = set()
        queue = deque([center_cell])

        while (
            queue
            and len(landmass_cells)
            < self.blueprint.row_count * self.blueprint.col_count
        ):
            current_cell = queue.popleft()

            # Check if the current cell is part of the landmass and not visited.
            if current_cell.passable and current_cell.designation not in visited:
                landmass_cells.add(current_cell)
                visited.add(current_cell.designation)

                # Add adjacent land cells to the queue for exploration.
                for neighbor in current_cell.adjacent:
                    if neighbor not in visited:
                        neighbor_cell = self.cells[neighbor]
                        if neighbor_cell.passable:
                            queue.append(neighbor_cell)
        return list(landmass_cells)

    def _find_landmasses(self):
        """
        Finds and returns all landmasses on the grid.

        Returns:
            List of landmasses, where each landmass is a list of cells.
        """
        landmasses = []
        visited = set()
        print('Finding landmasses ...')
        for cell in self.cells.values():
            if cell.passable and cell.designation not in visited:
                landmass = self._get_landmass_cells(cell)
                landmasses.append(landmass)
                visited.update(cell.designation for cell in landmass)
        landmasses = {
            i: {
                'landmass_cells': landmass,
                'coastal_cells': self._find_coastal_cells(landmass)
            }
            for i, landmass in enumerate(landmasses)
        }
        print('Separating islands from landmasses ...')
        islands = {
            i: {
                'island_cells': landmass['landmass_cells'],
                'coastal_cells': landmass['coastal_cells'],
            }
            for i, landmass in landmasses.items()
            if len(landmass['landmass_cells']) < 100
        }
        for i in islands:
            del landmasses[i]
        print('Done.')
        return landmasses, islands
                
                
    def _set_landmass_cells(self):
        for i, landmass in self.landmasses.items():
            for cell in landmass['landmass_cells']:
                cell.landmass_index = i
            for cell in landmass['coastal_cells']:
                cell.is_coastal = True
            
    
    def _find_coastal_cells(self, landmass_cells):
        """
        Finds and returns all cells belonging to a landmass that are adjacent to an unpassable cell.

        Args:
            landmass_cells: List of cells belonging to the landmass.

        Returns:
            List of cells that are adjacent to the ocean.
        """
        coastal_cells = set()
        for landmass_cell in landmass_cells:
            for neighbor in landmass_cell.adjacent:
                neighbor_cell = self.cells[neighbor]
                if not neighbor_cell.passable:
                    coastal_cells.add(landmass_cell)
        return list(coastal_cells)
    

    def _heuristic(self, cella, cellb):
        """Estimates the distance between two cells using Manhattan distance"""
        cell_a_coords = self.cells[cella].coordinates
        cell_b_coords = self.cells[cellb].coordinates
        (x1, y1) = cell_a_coords
        (x2, y2) = cell_b_coords
        return abs(x1 - x2) + abs(y1 - y2)

    # Define the _cost function
    def _cost(self, current, next):
        """Returns the cost to move from the current cell to the next cell"""
        cell = self.cells[next]
        cost = 0
        if current not in cell.adjacent:
            """Adjusts the cost for adjacency"""
            cost += float("inf")
        if not self.grid_plan[next]['passable'] or not cell.passable:
            cost += float("inf")
        else:
            cost += cell.cost_in
            cost += self.cells[current].cost_out            
        return cost

    # Implement A* algorithm
    def _astar(self, start, goal):
        goal_coords = self.cells[goal].coordinates
        """Finds the shortest path from start to goal in the given graph using A* algorithm"""
        frontier = [(0, start)]  # A priority queue of nodes to explore
        came_from = {}  # A dictionary that maps nodes to their parent nodes
        cost_so_far = {start: 0}  # A dictionary that maps nodes to the _cost of the best known path to that node
        graph = self.blueprint._graph

        while frontier:
            _, current = heapq.heappop(frontier)
            current_coords = self.cells[current].coordinates
            if current_coords == goal_coords:
                # We have found the goal, reconstruct the path and return it
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return (path, cost_so_far[goal])

            for next_step in graph[current]:
                # For each neighbor of the current node, 
                # calculate the _cost of the path from the start node to that neighbor
                new_cost = cost_so_far[current] + self._cost(current, next_step)
                if next_step not in cost_so_far or new_cost < cost_so_far[
                    next_step # If the new path is better than the old path
                ]:
                    cost_so_far[next_step] = new_cost  # Update the cost of the path to the neighbor
                    priority = new_cost + self._heuristic(goal, next_step)  # Calculate the priority of the neighbor
                    heapq.heappush(frontier, (priority, next_step))  # Add the neighbor to the frontier
                    came_from[next_step] = current  # Update the neighbor's parent to the current node

        return None  # We didn't find a path

    def refresh(self, dt):
        for cell in self.cells.values():
            cell.refresh(dt)

    def __json__(self):
        grid_dict = {
            "cell_size": self.cell_size,
        }
        cells_dict = {}
        for cell_designation, cell in self.cells.items():
            cell_dict = cell.__json__()
            cells_dict[cell_designation] = cell_dict

        grid_dict["cells"] = cells_dict

        return grid_dict
