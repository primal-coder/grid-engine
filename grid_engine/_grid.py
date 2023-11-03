from __future__ import annotations
import random

import pyglet as pyglet

from .__log__ import logger as _logger, log_method as _log_method

from ._terraform import Terraformer
from ._cell import Cell
from ._blueprint import Blueprint
from ._grid_object import GridZone
from ._utility import QuietDict as _QuietDict


import pickle as _pickle
import random as _random
import itertools as _itertools
import heapq as _heapq
import numpy as _np
import os as _os
import math

from pymunk import Vec2d as _Vec2d

from abc import ABC as _ABC

from uuid import uuid4 as _uuid4

from subprocess import call as _call

from collections import deque as _deque

from random import choice as _choice

from typing import Optional as _Optional, Union as _Union, Any

RIVER_BLUE = (18, 70, 132, 255)
RIVERBANK_BROWN = (32, 89, 31, 255)

_logger.gridengine('Setting saves directory ...')
saves_dir = f'{_os.path.abspath(_os.path.curdir)}/grid_engine/_saves/'
_logger.gridengine(f'Saves directory set to {saves_dir}')
DIRECTIONS = {
        'N': 'up',
        'NE': 'up_right',
        'E': 'right',
        'SE': 'down_right',
        'S': 'down',
        'SW': 'down_left',
        'W': 'left',
        'NW': 'up_left'
}


def clear():
    _call('clear')


def get_vector_direction(pointa, pointb):
    pointa, pointb = _Vec2d(pointa[0], pointa[1]), _Vec2d(pointb[0], pointb[1])
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


def save_grid(grid: Grid):
    if not _os.path.exists(f'{saves_dir}{grid.grid_id[-5:]}'):
        _os.makedirs(f'{saves_dir}{grid.grid_id[-5:]}')
            
    with open(f'{saves_dir}{grid.grid_id[-5:]}/grid.{grid.grid_id[-5:]}.pkl', 'wb') as f:
        _pickle.dump(grid, f)


def load_grid(num: _Optional[int] = None, grid_id: _Optional[str] = None):
    if num is not None: # load by index
        save_dir = f'{_os.listdir(saves_dir)[num]}'
    elif grid_id is not None: # load by grid ID
        save_dir = f'{saves_dir}{grid_id[-5:]}'
    else:
        raise ValueError('No save number or grid ID provided.')
    
    with open(f'{save_dir}/grid.{save_dir[-5:]}.pkl', 'rb') as f:
        return _pickle.load(f)


class Cells(_QuietDict):
    pass


class AbstractGrid(_QuietDict, _ABC):
    """The abstract base class for all grids."""
    _grid_id = None
    _with_terrain = None
    _blueprint = None
    _terraformer = None
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
        blueprint=None,
        cell_size=None,
        dimensions=None,
        noise_scale=None,
        noise_octaves=None,
        noise_roughness=None
    ) -> None:
        super(AbstractGrid, self).__init__()
    
    @property
    def grid_id(self) -> str:
        """The unique identifier of the grid."""
        return self._grid_id if self._grid_id is not None else print('Grid ID not set.')
    
    @grid_id.setter
    def grid_id(self, grid_id: _Optional[str] = None) -> None:
        self._grid_id = grid_id if grid_id is not None else _uuid4().hex
        
    @property
    def with_terrain(self) -> bool:
        """Whether the grid has terrain."""
        return self._with_terrain
    
    @with_terrain.setter
    def with_terrain(self, with_terrain: _Optional[bool] = None) -> None:
        self._with_terrain = with_terrain if with_terrain is not None else True
        
    @property
    def blueprint(self) -> _Optional[type[Blueprint._AbstractGridBlueprint]]:
        """The blueprint of the grid."""
        return self._blueprint
    
    @blueprint.setter
    def blueprint(self, blueprint: _Optional[type[Blueprint._AbstractGridBlueprint]] = None) -> None:
        if blueprint is not None:
            self._blueprint = blueprint
        
    @property
    def terraformer(self) -> type[Terraformer]:
        """The terraformer of the grid."""
        return self._terraformer
        
    @property
    def grid_array(self):
        """The grid array of the grid."""
        return self.blueprint.array
    
    @grid_array.setter
    def grid_array(self, grid_array):
        self.blueprint.array = grid_array
    
    @property
    def grid_plan(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of grid data for the grid. Provided by the blueprint."""
        return self._grid_plan
    
    @grid_plan.setter
    def grid_plan(self, grid_plan: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        self._grid_plan = grid_plan
            
    @property
    def dictTerrain(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of terrain data for the grid. Provided by the blueprint."""
        return self.blueprint.dictTerrain
    
    @dictTerrain.setter
    def dictTerrain(self, dictTerrain: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        for cell in self.cells.values():
            cell.entry_terrain = self.grid_array[cell.col_index, cell.row_index, 0]
    
    @property
    def dictObject(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of object data for the grid. Provided by the blueprint."""
        return self.blueprint.dictObject
    
    @dictObject.setter
    def dictObject(self, dictObject: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        for cell in self.cells.values():
            cell.entry_object = self.grid_array[cell.col_index, cell.row_index, 1]
            
    @property
    def dictUnit(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of unit data for the grid. Provided by the blueprint."""
        return self.blueprint.dictUnit
    
    @dictUnit.setter
    def dictUnit(self, dictUnit: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        for cell in self.cells.values():
            cell.entry_unit = self.grid_array[cell.col_index, cell.row_index, 2]
    
    @property
    def dictZone(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of zone data for the grid. Provided by the blueprint."""
        return self.blueprint.dictZone
    
    @dictZone.setter
    def dictZone(self, dictZone: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        for cell in self.cells.values():
            cell.entry_zone = self.grid_array[cell.col_index, cell.row_index, 3]
    
    @property
    def dictEffect(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of effect data for the grid. Provided by the blueprint."""
        return self.blueprint.dictEffect

    @dictEffect.setter
    def dictEffect(self, dictEffect: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        for cell in self.cells.values():
            cell.entry_effect = self.grid_array[cell.col_index, cell.row_index, 4]
                
    @property
    def dictFow(self) -> _Optional[dict[str, dict[str, Any]]]:
        """The dictionary of fog of war data for the grid. Provided by the blueprint."""
        return self.blueprint.dictFow

    @dictFow.setter
    def dictFow(self, dictFow: _Optional[dict[str, dict[str, Any]]] = None) -> None:
        for cell in self.cells.values():
            cell.entry_fow = self.grid_array[cell.col_index, cell.row_index, 5]

    @property
    def init_cell_size(self):
        """The initial cell size of the grid."""
        return self._init_cell_size
    
    @init_cell_size.setter
    def init_cell_size(self, init_cell_size: _Optional[int] = None) -> None:
        self._init_cell_size = init_cell_size
        
    @property
    def cell_size(self) -> int:
        """The cell size of the grid."""
        return self._cell_size
    
    @cell_size.setter
    def cell_size(self, cell_size: _Optional[int] = None) -> None:
        self._cell_size = cell_size
        
    @property
    def cells(self) -> type[Cells]:
        """A subclass of QuietDict representing all cells in the grid. Keys are cell designations, values are Cell
        objects."""
        return self._cells
    
    @cells.setter
    def cells(self, cells: _Optional[type[Cells]] = None) -> None:
        self._cells = cells
        
    @property
    def rows(self) -> list[list[Cell,]]:
        """A dynamically generated list of all rows in the grid. The list contains Row objects, which are dynamically
        generated lists of Cell objects."""
        return self._rows
    
    @rows.setter
    def rows(self, rows: _Optional[list[list[Cell,]]] = None) -> None:
        self._rows = rows
        
    @rows.deleter
    def rows(self) -> None:
        del self._rows
        
    @property
    def cols(self) -> list[list[Cell,]]:
        """A dynamically generated list of all columns in the grid. The list contains Column objects, which are
        dynamically generated lists of Cell objects."""
        return self._cols
    
    @cols.setter
    def cols(self, cols: _Optional[list[list[Cell,]]] = None) -> None:
        self._cols = cols
        
    @cols.deleter
    def cols(self):
        del self._cols
        
    @property
    def quadrants(self) -> list[type[_QuietDict]]:
        """A dynamically generated list of all quadrants in the grid. The list contains Quadrant objects, which are
        subclasses of QuietDict. The quadrant data can be accessed by quadrant number, e.g. `grid.quadrants.quad0`.
        
        grid.quadrants.quad0['cell_count']/[0] returns the number of cells in the quadrant.
        grid.quadrants.quad0['cells']/[1] returns a list of all cells in the quadrant.
        """
        return self._quadrants
    
    @quadrants.setter
    def quadrants(self, quadrants: _Optional[list[type[_QuietDict]]] = None) -> None:
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


class Grid(AbstractGrid, _ABC):
    """The grid object. Contains all cells, rows, columns, and quadrants."""
    def __init__(
            self,
            blueprint: _Optional[type[Blueprint.AbstractGridBlueprint]] = None,
            cell_size: _Optional[int] = None,
            dimensions: _Optional[tuple[int, int]] = None,
            with_terrain: _Optional[bool] = None,
            noise_scale: _Optional[float] = None,
            noise_octaves: _Optional[int] = None,
            noise_roughness: _Optional[float] = None            
    ):
        """
        Initializes the grid object. If no blueprint is provided, a terrain grid blueprint is generated.
        
        Args: blueprint (_Optional[type[Blueprint.AbstractGridBlueprint]], optional): The blueprint of the grid.
        Defaults to None. cell_size (_Optional[int], optional): The size of each cell in the grid. Defaults to None.
        dimensions (_Optional[tuple[int, int]], optional): The dimensions of the grid. Defaults to None. with_terrain
        (_Optional[bool], optional): Whether the grid has terrain. Defaults to None. noise_scale (_Optional[
        float], optional): The scale of the Perlin noise. Defaults to None. noise_octaves (_Optional[int],
        optional): The number of octaves for the Perlin noise. Defaults to None. noise_roughness (_Optional[float],
        optional): The roughness of the Perlin noise. Defaults to None.
        """
        if dimensions is not None and (dimensions[0] * dimensions[1] > 1000000) and not self._size_warning():
            return
            
        self.grid_id = _uuid4().hex if blueprint is None else blueprint.blueprint_id
        self.with_terrain = with_terrain if with_terrain is not None else True
        self.blueprint = blueprint if blueprint is not None else Blueprint.TerrainGridBlueprint(cell_size, dimensions, self.grid_id, noise_scale, noise_octaves, noise_roughness) if self._with_terrain else Blueprint.BaseGridBlueprint(cell_size, dimensions, self.grid_id)
        self.grid_plan = self.blueprint.dictGrid
        super(Grid, self).__init__()
        self._init_cell_size = cell_size if cell_size is not None else self.blueprint._cell_size
        self.cell_size = cell_size if cell_size is not None else self.blueprint._cell_size
        self.cells = Cells()
        for cell in self.grid_plan.keys():
            self.cells[cell] = Cell(cell, parentgrid=self)
            self.update({cell: self.cells[cell]})
        self.dictTerrain = self.blueprint.dictTerrain
        self.dictObject = self.blueprint.dictObject
        self.dictUnit = self.blueprint.dictUnit
        self.dictZone = self.blueprint.dictZone
        self.dictEffect = self.blueprint.dictEffect
        self.dictFow = self.blueprint.dictFow
        for cell in self.cells.items.values():
            cell.init_array()
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
        self.bodies_of_water, self.oceans, self.seas, self.lakes = self._find_bodies_of_water()
        self.delete_bodies_of_water()
        self.bodies_of_water_count = len(self.bodies_of_water)
        self.ocean_count = len(self.oceans)
        self.sea_count = len(self.seas)
        self.lake_count = len(self.lakes)
        self._set_water_cells()
        for row in self.rows:
            row.row_index = self.rows.index(row)
        for col in self.cols:
            col.col_index = self.cols.index(col)
        self.river_count = 0
        self.rivers: list[list[Cell,]] = []
        self._terraformer = Terraformer(self)
        self.terraformer.set_rivers(2)

        # self.town = GridZone(self, 'Town', 'town', self.random_cell(attr=('passable', True)), (45, 45, 45), 2)

    def _size_warning(self, cell_dimensions):
        import colorama
        quit = input(f'{colorama.Fore.RED}WARNING{colorama.Fore.RESET}: The provided parameters will generate a grid composed of {colorama.Fore.LIGHTWHITE_EX}{round((args.rows*args.columns)/1000000, 1)} million{colorama.Fore.RESET} cells. \nThis will consume a significant amount of memory/resources/time. \nIf you have limited amount of memory this could cause your system to hang or crash. \nIf you understand the risks, continue by pressing {colorama.Fore.LIGHTGREEN_EX}ENTER{colorama.Fore.RESET}. Otherwise, press {colorama.Fore.LIGHTRED_EX}CTRL+C{colorama.Fore.RESET} to exit.')
        return quit == ''
    
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
        The values here are directly related to the edges of the grid.
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
        """Sets up the rank attribute. A `rows` attribute is assigned a type value, with a base of type[list]. The
        `rows` attribute is then instantiated. The `rows` attribute is then assigned an attribute for each row in the
        grid, with a base of type[list]. Each row attribute is then instantiated. Finally, each row attribute is
        appended to the `rows` object.
        
        Effectively, this creates a list of lists, with each list representing a row in the grid. But, each row is
        accessible by attribute.
        
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
        """Sets up the file attribute. A `cols` attribute is assigned a type value, with a base of type[list]. The
        `cols` attribute is then instantiated. The `cols` attribute is then assigned an attribute for each column in
        the grid, with a base of type[list]. Each column attribute is then instantiated. Finally, each col attribute
        is appended to the `cols` object.
        
        Effectively, this creates a list of lists, with each list representing a column in the grid. But, each column
        is accessible by attribute.
        
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
        """Sets up the quadrants attribute. A `quadrants` attribute is assigned a type value, with a base of type[
        list]. The `quadrants` attribute is then instantiated. The `quadrants` attribute is then assigned an
        attribute for each quadrant in the grid, with a base of type[QuietDict]. Each quadrant attribute is then
        instantiated. Each quadrant attribute is appended to the `quadrants` object. Finally, each quadrant attribute
        is updated with the quadrant data from the blueprint.
        
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
            
    @_log_method
    def get_cell(self, cell_designation: _Optional[str] = None) -> _Optional[Cell]:
        """Returns a cell object by its designation."""
        try:
            return self.cells[cell_designation]
        except KeyError:
            return None

    @_log_method
    def get_cell_by_index(self, index: _Optional[int] = None) -> _Optional[Cell]:
        """Returns a cell object by its index in the cell list."""
        try:
            return self.cells[self.blueprint._cell_list[index]]
        except KeyError:
            return None

    @_log_method
    def get_cell_by_relative_indices(
            self,
            reference: _Optional[tuple[int, int]] = None,
            indices: _Optional[tuple[int, int]] = None
    ):
        """Returns a cell object by its relative indices from a reference cell.
        
        Args:
            reference (_Optional[tuple[int, int]], optional): The reference cell. Defaults to None.
            indices (_Optional[tuple[int, int]], optional): The relative indices from the reference cell. Defaults to None.
            
        Returns:
            _Optional[Cell]: The cell object.
            
        Example:
            ```grid.get_cell_by_relative_indices((0, 0), (1, 0))``` returns the cell directly below the reference cell.
        """
        ref = _Vec2d(*reference)
        ind = _Vec2d(*indices)
        r, f = (ref + ind).int_tuple
        r, f = max(0, r), max(0, f)
        r, f = min(r, self.blueprint.row_count - 1), min(f, self.blueprint.col_count - 1)
        return self.grid_array[r, f, 0]['designation']

    @_log_method
    def get_nearest_cell_with(self, cella: _Union[str, Cell], attr_name: str, attr_val: Any):
        """Returns the nearest cell with the specified attribute value.
        
        Args:
            cella (_Union[str, Cell]): The reference cell.
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
            return _random._choice(nearest['cell'])
    
    @_log_method
    def get_row_by_index(self, index: _Optional[int] = None) -> _Optional[list[Cell,]]:
        """Returns a row by its index in the row list."""
        return self.blueprint.rank[index]

    @_log_method
    def get_row_by_height(self, height: _Optional[int] = None) -> _Optional[list[Cell,]]:
        """Returns a row by its height(y coordinate)."""
        if self.cell_size == 1:
            return height
        for i in range(len(self.rows)):
            if self.rows[i].height <= height < self.rows[i + 1].height:
                return self.get_row_by_index(i)

    @_log_method
    def get_row_by_name(self, row_name: _Optional[str] = None) -> _Optional[list[Cell,]]:
        """Returns a row by its name."""
        return getattr(self.rows, f'row{row_name}')
    
    @_log_method
    def get_col_by_index(self, index: _Optional[int] = None) -> _Optional[list[Cell,]]:
        """Returns a column by its index in the column list."""
        return self.blueprint.file[index]
    
    @_log_method
    def get_col_by_width(self, width: _Optional[int] = None) -> _Optional[list[Cell,]]:
        """Returns a column by its width(x coordinate)."""
        if self.cell_size == 1:
            return width
        for i in range(len(self.cols)):
            if i == len(self.cols) - 1 or self.cols[i].width <= width < self.cols[i + 1].width:
                return self.get_col_by_index(i)
                    
    @_log_method
    def get_col_by_name(self, col_name: _Optional[str] = None) -> _Optional[list[Cell,]]:
        """Returns a column by its name."""
        return getattr(self.cols, f'col{col_name}')
    
    @_log_method
    def get_cell_by_position(self, x: _Optional[int] , y: _Optional[int]) -> _Optional[Cell]:
        """Returns a cell by its position on the grid."""
        r = self.get_row_by_height(y)
        f = self.get_col_by_width(x)
        return self.get_cell(f'{r}{f}')
    
    @_log_method
    def get_cell_by_rank_file(self, rank: _Optional[int], file: _Optional[int]) -> _Optional[Cell]:
        """Returns a cell by its rank and file. Rank and file are the indices of the row and column respectively."""
        # r = self.get_row_by_index(rank)
        # f = self.get_col_by_index(file)
        # for cell in r:
        #     if cell in f:
        #         return cell
        return self.cells[self.grid_array[rank, file, 0]['designation']]

    @_log_method
    def random_cell(
            self,
            attr: _Optional[tuple[str, Any]] = None,
            attrs: _Optional[tuple[tuple[str, any]]] = None,
            landmass_index: _Optional[int] = None
    ) -> _Optional[Cell]:
        """Returns a _random cell. If an attribute is provided, the cell must have that attribute. If multiple
        attributes are provided, the cell must have all attributes. If a landmass index is provided, the cell must be
        in that landmass.
        
        Args:
            attr (_Optional[tuple[str, Any]], optional): The attribute. Defaults to None.
            attrs (_Optional[tuple[tuple[str, any]]], optional): The attributes. Defaults to None.
            landmass_index (_Optional[int], optional): The landmass index. Defaults to None.
            
        Example:
            ```grid.random_cell(attr=('passable', True))``` returns a _random passable cell.
            ```grid.random_cell(attrs=(('passable', True), ('terrain_str', 'GRASS')))``` returns a _random passable cell with terrain string 'GRASS'.
            ```grid.random_cell(landmass_index=0)``` returns a _random cell in the first landmass.
        """
        if landmass_index is not None:
            cell = _choice(self.landmasses[landmass_index]['landmass_cells'])
        elif attrs is not None:
            cell = self.cells[_choice(self.blueprint.cell_list)]
            while any(getattr(cell, attr[0]) != attr[1] for attr in attrs):
                cell = self.cells[_choice(self.blueprint.cell_list)]
        elif attr is not None:
            cell = self.cells[_choice(self.blueprint.cell_list)]
            while getattr(cell, attr[0]) != attr[1]:
                cell = self.cells[_choice(self.blueprint.cell_list)]
        else:
            cell = self.cells[_choice(self.blueprint.cell_list)]
        return cell
    
    @_log_method
    def random_row(self) -> _Optional[list[Cell,]]:
        """Returns a _random row."""
        return _choice([getattr(self.rows, f'row{r}') for r in self.blueprint.rank])

    @_log_method
    def random_col(self) -> _Optional[list[Cell,]]:
        """Returns a _random column."""
        return _choice([getattr(self.cols, f'col{c}') for c in self.blueprint.file])

    @_log_method
    def get_adjacent(self, cell_designation: _Optional[str] = None) -> _Optional[list[Cell,]]:
        """Returns a list of all adjacent cells to the specified cell."""
        return [self.cells[adj] for adj in self.cells[cell_designation].adjacent]

    # @_log_method
    # def get_neighbors(self, cell_designation: _Optional[str] = None) -> _Optional[list[Cell,]]:
    #     return [self.cells[adj].occupant for adj in self.cells[cell_designation].adjacent if
    #             self.cells[adj].occupant is not None]

    def get_distance(self,
                     cella: _Optional[str] = None,
                     cellb: _Optional[str] = None,
                     measurement: _Optional[str] = None
        ) -> _Optional[int]:
        """Returns the distance between two cells. If no measurement is provided, the distance is in units. If
        measurement is 'cells', the distance is in cells."""
        m = measurement if measurement is not None else "units"
        if m == "units":
            return self._heuristic(cella, cellb)
        if m == "cells":
            return self._heuristic(cella, cellb) // self.cell_size

    @_log_method
    def get_path(
            self,
            cella: _Optional[_Union[Cell, str]] = None,
            cellb: _Optional[_Union[Cell, str]] = None
    ) -> _Optional[list[Cell,]]:
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
    
    @_log_method
    def get_walk(self, start_cell: _Optional[str] = None, end_cell: _Optional[str] = None):
        walk_cells = [start_cell]
        if start_cell != end_cell:
            current_distance = self.get_distance(start_cell, end_cell, 'cells')
            while current_distance > 1:
                current_cell = self.cells[walk_cells[-1]]
                adjacent_cells = [adjacent_cell for adjacent_cell in current_cell.adjacent if self.cells[adjacent_cell].passable and adjacent_cell not in walk_cells]
                if not adjacent_cells:
                    walk_cells.pop(-1)
                    break
                else:
                    direction = random.randint(0, len(adjacent_cells)-1) if len(adjacent_cells) > 1 else 0
                    next_cell = adjacent_cells[direction]
                check_ = 0
                while self.get_distance(next_cell, end_cell) > current_distance + 2 and check_  < 8:
                    print(f'Current distance: {current_distance} | Current cell: {current_cell.designation} | Next cell: {next_cell}', end='\r')
                    direction += 1
                    direction %= len(adjacent_cells)
                    check_ += 1
                    next_cell = adjacent_cells[direction]
                    continue
                walk_cells.append(next_cell)
                current_distance = self.get_distance(next_cell, end_cell)
            return walk_cells


    
    @_log_method
    def get_direction(
            self,
            cella: _Optional[_Union[Cell, str]] = None,
            cellb: _Optional[_Union[Cell, str]] = None
    ) -> _Optional[str]:
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

    @_log_method
    def get_area(self, center_cell: _Optional[_Union[Cell, str]] = None, radius: _Optional[int] = None):
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
    
    @_log_method
    def get_perimeter(self, area_cells: _Optional[list[Cell,]] = None):
        perimeter_cells = []
        for cell in self.cells.values():
            perimeter_cells.extend(
                cell
                for adjacent in cell.adjacent
                if self.cells[adjacent] in area_cells and cell not in area_cells
            )
        perimeter_cells = set(perimeter_cells)
        return sorted(perimeter_cells, key=lambda cell: cell.designation)

    @_log_method
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
        queue = _deque([center_cell])

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
            
    def _get_largest_landmass(self):
        largest_land = 0
        largest_size = 0
        for i, landmass in self.landmasses.items():
            landmass_size = len(landmass['landmass_cells'])
            if landmass_size > largest_size:
                largest_land = i
                largest_size = landmass_size
        landmass = self.landmasses[largest_land]
        print(f'Found largest landmass: {largest_land} with {largest_size} cells')
        return landmass
    
    def _get_lake_coastal_cells(self):
        print('Finding lake coastal cells ...')
        if lake_coastal_cells := list(
            _itertools.chain.from_iterable(
                [
                    self.lakes[lake]['coastal_cells']
                    for lake in self.lakes
                ]
            )
        ):
            print(f'Found {len(lake_coastal_cells)} cells.')
            return lake_coastal_cells
        print('No coastal lake cells found.')
        return None

        
    def _find_coastal_cells(self, landmass_cells):
        """
        Finds and returns all cells belonging to a landmass that are adjacent to an u_npassable cell.

        Args:
            landmass_cells: List of cells belonging to the landmass.

        Returns:
            List of cells that are adjacent to the ocean.
        """
        coastal_cells = set()
        for landmass_cell in landmass_cells:
            for neighbor in landmass_cell.adjacent:
                neighbor_cell = self.cells[neighbor]
                if neighbor_cell.terrain_str == 'OCEAN':
                    coastal_cells.add(landmass_cell)
        return list(coastal_cells)
    
    def _find_bodies_of_water(self):
        visited = set()
        bodies_of_water = []
        for cell in self.cells.values():
            if not cell.passable and cell.designation not in visited:
                body_of_water = self._get_body_of_water(cell)
                bodies_of_water.append(body_of_water)
                visited.update(cell.designation for cell in body_of_water)
        bodies_of_water = {
            i: {
                'body_of_water_cells': body_of_water,
                'coastal_cells': self._find_coastal_cells(body_of_water)
            }
            for i, body_of_water in enumerate(bodies_of_water)
        }
        oceans = {
            i: {
                'ocean_cells': body_of_water['body_of_water_cells'],
                'coastal_cells': body_of_water['coastal_cells'],
            }
            for i, body_of_water in bodies_of_water.items()
            if len(body_of_water['body_of_water_cells']) > 1000
        }
        seas = {
            i: {
                'sea_cells': body_of_water['body_of_water_cells'],
                'coastal_cells': body_of_water['coastal_cells'],
            }
            for i, body_of_water in bodies_of_water.items()
            if 500 < len(body_of_water['body_of_water_cells']) < 1000
        }
        lakes = {
            i: {
                'lake_cells': body_of_water['body_of_water_cells'],
                'coastal_cells': body_of_water['coastal_cells'],
            }
            for i, body_of_water in bodies_of_water.items()
            if 100 < len(body_of_water['body_of_water_cells']) < 500
        }
        return bodies_of_water, oceans, seas, lakes
    
    def delete_bodies_of_water(self):
        for i, body in self.bodies_of_water.copy().items():
            if len(body['body_of_water_cells']) < 100:
                del self.bodies_of_water[i]
                    
    
    def _get_body_of_water(self, center_cell):
        """
        Finds and returns all cells belonging to the same body of water as the center cell.
        Uses the passable attribute of each instance of cell to determine if it belongs
        to the body of water group.

        Args:
            center_cell: The center cell around which to search for the body of water.

        Returns:
            List of cells belonging to the same body of water as the center cell.
        """
        body_of_water_cells = set()
        visited = set()
        queue = _deque([center_cell])

        while (
            queue
            and len(body_of_water_cells)
            < self.blueprint.row_count * self.blueprint.col_count
        ):
            current_cell = queue.popleft()

            # Check if the current cell is part of the body of water and not visited.
            if not current_cell.passable and current_cell.designation not in visited:
                body_of_water_cells.add(current_cell)
                visited.add(current_cell.designation)

                # Add adjacent water cells to the queue for exploration.
                for neighbor in current_cell.adjacent:
                    if neighbor not in visited:
                        neighbor_cell = self.cells[neighbor]
                        if not neighbor_cell.passable:
                            queue.append(neighbor_cell)
        return list(body_of_water_cells)
    
    def _set_water_cells(self):
        for i, body_of_water in self.bodies_of_water.items():
            for cell in body_of_water['body_of_water_cells']:
                cell.body_of_water_index = i

    def _heuristic(self, cella, cellb):
        """Estimates the distance between two cells using Manhattan distance"""
        cell_a_coords = self.cells[cella].coordinates
        cell_b_coords = self.cells[cellb].coordinates
        (x1, y1) = cell_a_coords
        (x2, y2) = cell_b_coords
        return round(math.hypot(abs(x1 - x2), abs(y1 - y2)))

    # Define the _cost function
    def _cost(self, current, next):
        """Returns the cost to move from the current cell to the next cell"""
        cell = self.cells[next]
        cost = self.cells[current].cost_out
        if current not in cell.adjacent:
            """Adjusts the cost for adjacency"""
            cost += float("inf")
        if not self.grid_plan[next]['passable'] or not cell.passable:
            cost += float("inf")
        else:
            cost += cell.cost_in
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
            _, current = _heapq.heappop(frontier)
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
                    _heapq.heappush(frontier, (priority, next_step))  # Add the neighbor to the frontier
                    came_from[next_step] = current  # Update the neighbor's parent to the current node

        return None  # We didn't find a path
    
    def _cast_grid(self, scene):
        """Cast the grid to the scene. Each cell is represented as a pyglet.shapes.Rectangle object."""
        for cell in self.cells.values():
            x, y, w, h, c = cell._request_shape()
            cell.shape = pyglet.shapes.Rectangle(x, y, w, h, c, batch=scene.main_batch)

    def _highlight_cell(self, cell, color=(255, 255, 255)):
        """Highlight a cell."""
        cell.shape.color = color
        
    def _restore_cell(self, cell):
        """Restore a cell to its original color."""
        cell.shape.color = cell.terrain_color
        
    def _highlight_path(self, path):
        """Highlight a path."""
        for cell in path:
            cell = self.cells[cell]
            self._highlight_cell(cell)
        
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
