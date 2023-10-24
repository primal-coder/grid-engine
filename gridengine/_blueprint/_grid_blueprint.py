from ._grid_processing import *
from ._terrain_processing import *
from ._terrain_processing import _COLORS 
import numpy as _np
from collections import defaultdict as _defaultdict
from uuid import uuid4 as _uuid4
import pickle as _pickle
from typing import Optional as _Optional
import sys as _sys
import os as _os


_module_name = 'gridengine'
_install_dir = _os.path.dirname(_sys.modules[_module_name].__file__)
_saves_dir = f'{_install_dir}/saves/'

_OCEAN_BLUE = _COLORS['OCEAN_BLUE']

def save_blueprint(blueprint):
    import os as _os
    _os.chdir(f'{_saves_dir}')
    if not _os.path.exists(f'{blueprint.blueprint_id[-5:]}'):
        _os.makedirs(f'{blueprint.blueprint_id[-5:]}')
    with open(f'{blueprint.blueprint_id[-5:]}/blueprint.{blueprint.blueprint_id[-5:]}.pkl', 'wb') as f:
        _pickle.dump(blueprint, f)


def load_blueprint(num: int):
    import os as _os
    with open(f'{_saves_dir}{_os.listdir(_saves_dir)[-num]}/blueprint.{_os.listdir(_saves_dir)[-num][-5:]}.pkl', 'rb') as f:
        return _pickle.load(f)


_levels = ['base', 'terrain']

# colors

_UNPASSABLE_TERRAIN = [
        'OCEAN', 'BLOCKED', 'MOUNTAIN_BASE', 'MOUNTAIN_SIDE', 'MOUNTAIN_CRAG', 'MOUNTAIN_PEAK'
]

_layer_attributes = {
        'base':       [
                'designation', 'coordinates', 'cell_index', 'rank_index',
                'file_index', 'quadrant_index', 'adjacent', 'groups'
        ],
        'terrain':    [
                'raw', 'int',
                'str', 'color',
                'cost_in', 'cost_out',
                'char'
        ]
}


class _AbstractGridBlueprint:
    """
    Abstract Grid Blueprint class. This is the blueprint for the GridBlueprint class, if you will.
    """
    _blueprint_id = None
    _cell_size = None
    _grid_dimensions = None
    _col_count = None
    _grid_width = None
    _row_count = None
    _grid_height = None
    _rank = None
    _file = None
    _layers = None
    _cell_list = None
    _array = None
    _dictGrid = None
    _dictTerrain = None
    _cell_coordinates = None
    _quadrants = None
    _graph = None
    _items = None

    @property
    def cell_size(self) -> int:
        """Returns the size of a cell."""
        return self._cell_size

    @cell_size.setter
    def cell_size(self, cell_size: int) -> None:
        """Sets the size of a cell."""
        self._cell_size = cell_size

    @property
    def grid_dimensions(self) -> tuple[int, int]:
        """Returns the dimensions of the grid."""
        return self._grid_dimensions

    @grid_dimensions.setter
    def grid_dimensions(self, grid_dimensions: tuple[int, int]) -> None:
        """Sets the dimensions(in pixels) of the grid."""
        self._grid_dimensions = grid_dimensions
        grid_shape = (grid_dimensions[0] // self.cell_size,   # convert to cells
                            grid_dimensions[1] // self.cell_size)
        self._grid_width = grid_dimensions[0]
        self._col_count = grid_shape[0]
        self._grid_height = grid_dimensions[1]
        self._row_count = grid_shape[1]

    @property
    def col_count(self) -> int:
        """Returns the number of columns in the grid."""
        return self._col_count

    @property
    def grid_width(self) -> int:
        """Returns the width(in pixels) of the grid."""
        return self._grid_width

    @property
    def row_count(self) -> int:
        """Returns the number of rows in the grid."""
        return self._row_count

    @property
    def grid_height(self) -> int:
        """Returns the height(in pixels) of the grid."""
        return self._grid_height


    @property
    def rank(self) -> list[str]:
        """Returns the rank of the grid. The rank is a list of strings that represent the rows of the grid."""
        return self._rank

    @rank.setter
    def rank(self, rank: _Optional[list[str]]) -> None:
        """Sets the rank of the grid."""
        self._rank = rank

    @property
    def file(self) -> list[str]:
        """Returns the file of the grid. The file is a list of strings that represent the columns of the grid."""
        return self._file

    @file.setter
    def file(self, file: _Optional[list[str]]) -> None:
        """Sets the file of the grid."""
        self._file = file

    @property
    def cell_list(self) -> list[str]:
        """Returns the list of cells. The list of cells is a list of strings that represent the cells of the grid."""
        return self._cell_list

    @cell_list.setter
    def cell_list(self, cell_list: _Optional[list[str]]) -> None:
        """Sets the list of cells."""
        self._cell_list = cell_list
        
    @property
    def array(self):
        """Returns the array of cells. The array of cells is a NumPy array of cells with 3 dimensions. The first
        dimension is the column, the second dimension is the row, and the third dimension is the layer. The layers
        are defined in the `_layer_attributes` dictionary. The first layer is the base layer, the second layer is the
        terrain layer.
        """
        return self._array
    
    @array.setter
    def array(self, array) -> None:
        """Sets the array of cells. Each cell's array attribute is set to the corresponding cell in the array."""
        self._array = array
        for cell in self.cell_list:
            self[cell].array = self.array[self[cell].row_index, self[cell].col_index, :]

    @property
    def dictGrid(self) -> dict[str, any]:
        """Returns the dictionary of cells."""
        return self._dictGrid

    @dictGrid.setter
    def dictGrid(self, dict_grid) -> None:
        """Sets the dictionary of cells. The value set here will be reflected in the array."""
        self._dictGrid = dict_grid
        for cell in self.cell_list:
            self.array[self.dictGrid[cell]['col_index']][self.dictGrid[cell]['row_index']][0] = self.dictGrid[cell]

    @property
    def dictTerrain(self):
        """Returns the dictionary of terrain information. Which corresponds to the terrain layer of the array."""
        return self._dictTerrain

    @dictTerrain.setter
    def dictTerrain(self, dictTerrain) -> None:
        """Sets the dictionary of terrain information. Which corresponds to the terrain layer of the array. The value
        set here will be reflected in the array."""
        self._dictTerrain = dictTerrain
        for cell in self.cell_list:
            self.array[self.dictGrid[cell]['col_index']][self.dictGrid[cell]['row_index']][1] = self.dictTerrain[cell]

    @property
    def cell_coordinates(self):
        """Returns the coordinates of the cells."""
        return self._cell_coordinates

    @cell_coordinates.setter
    def cell_coordinates(self, cell_coordinates) -> None:
        """Sets the coordinates of the cells."""
        self._cell_coordinates = cell_coordinates

    @property
    def quadrants(self):
        """Returns the quadrants of the grid."""
        return self._quadrants

    @quadrants.setter
    def quadrants(self, quadrants) -> None:
        """Sets the quadrants of the grid."""
        self._quadrants = quadrants

    @property
    def graph(self):
        """Returns the graph of the grid."""
        return self._graph

    @graph.setter
    def graph(self, graph) -> None:
        """Sets the graph of the grid."""
        self._graph = graph

    def __getstate__(self):
        return self.__dict__.copy()
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        

class BaseGridBlueprint(_AbstractGridBlueprint):

    def __init__(
        self, 
        cell_size: int = None, 
        grid_dimensions: tuple[int, int] = None, 
        grid_id: str = None, 
        array: _np.ndarray = None, 
        quadrants: dict = None, 
        graph: dict = None
    ) -> None:
        super(BaseGridBlueprint, self).__init__()
        self.blueprint_id = _uuid4().hex if grid_id is None else grid_id
        if array and quadrants and graph:
            self._array = array
            self._quadrants = quadrants
            self._graph = graph
            self._init_from_array()
        self.cell_size = cell_size if cell_size is not None else 10
        self.grid_dimensions = grid_dimensions if grid_dimensions is not None else (1000, 1000)
        self._array = _np.array(
                [0 for _ in list(range((self._col_count * self._row_count) * 2))],
                dtype=type(any),
        ).reshape((self._col_count, self._row_count, 2))
        self._init()

    def _init(self):
        grid_info = process_grid(self._row_count, self._col_count, self.cell_size)
        self.rank = grid_info['row_strings']
        self.file = grid_info['col_strings']
        self.cell_list = grid_info['cell_strings']
        self.cell_coordinates = grid_info['cell_coordinates']
        self.dictGrid = grid_info['grid_dict']
        self.quadrants = self._init_quadrants()
        self.graph = grid_info['graph']
        self._assign_array_elements()
                
    def _init_quadrants(self):
        quadrants = _defaultdict(dict)
        quad_cells = _defaultdict(list)
        for cell, information in self.dictGrid.items():
            quad_cells[information['quadrant_index']].append(cell)
        for quadrant_index, cell_list in quad_cells.items():
            # Create a dictionary of the cells in each quadrant
            quadrants[quadrant_index] = {
                    'cell_count': len(cell_list),
                    'cells':       cell_list
            }
        return quadrants

    def _assign_array_elements(self):
        terrain_layer = {}
        for cell, information in self.dictGrid.items():
            self.array[information['col_index']][information['row_index']][0] = information
            cell_layer_dict = {cell: {attrs: None for attrs in _layer_attributes['terrain']}}
            terrain_layer |= cell_layer_dict
            self.array[information['col_index']][information['row_index']][1] = cell_layer_dict
        self.dictTerrain = terrain_layer
        
    def __json__(self):
        return {
            'cell_size': self.cell_size,
            'grid_dimensions': self.grid_dimensions,
            'array': self.array,
            'quadrants': self.quadrants,
            'graph': self.graph,
        }

class TerrainGridBlueprint(BaseGridBlueprint):
    def __init__(
            self, cell_size: int, grid_dimensions: tuple[int, int], grid_id: str = None, noise_scale: int = None,
            noise_octaves: int = None, noise_roughness: float = None
            ):
        super(TerrainGridBlueprint, self).__init__(cell_size, grid_dimensions, grid_id)        
        for cell in self.dictGrid:
            self.dictGrid[cell]['passable'] = None
        self._init_terrain(noise_scale, noise_octaves, noise_roughness)

    def _init_terrain(self, noise_scale, noise_octaves, noise_roughness):
        self._noise_scale = noise_scale if noise_scale is not None else 25
        self._noise_octaves = noise_octaves if noise_octaves is not None else 38
        self._noise_roughness = noise_roughness if noise_roughness is not None else 0.35
        self.dictTerrain = process_noise(self._noise_scale, self._noise_octaves, self._noise_roughness, self._row_count, self._col_count, self._cell_size, self.dictGrid)
        self._set_base_terrain()
        self._adjust_passability()


    def _set_base_terrain(self):
        for cell in self.cell_list:
            if self.dictTerrain[cell]['raw'] is None:
                self.dictTerrain[cell]['raw'] = 0.0
                self.dictTerrain[cell]['int'] = 9
                self.dictTerrain[cell]['str'] = 'OCEAN'
                self.dictTerrain[cell]['color'] = _OCEAN_BLUE
                self.dictTerrain[cell]['cost_in'] = float('inf')
                self.dictTerrain[cell]['cost_out'] = float('inf')
                self.dictTerrain[cell]['char'] = '~'
                self.dictGrid[cell]['passable'] = False


    def _adjust_passability(self):
        passable = []
        unpassable = []
        for c, info in self.dictTerrain.items():
            if info['str'] in _UNPASSABLE_TERRAIN:
                self.dictGrid[c]['passable'] = False
                unpassable.append(c)
            else:
                self.dictGrid[c]['passable'] = True
                passable.append(c)
        return passable, unpassable

    def __json__(self):
        return {
            'cell_size': self.cell_size,
            'grid_dimensions': self.grid_dimensions,
            'row_strings': self.rank,
            'col_strings': self.file,
            'cell_strings': self.cell_list,
            'cell_coordinates': self.cell_coordinates,
            'dict_grid': self.dictGrid,
            'dict_terrain': self.dictTerrain,
            'noise_scale': self._noise_scale,
            'noise_octaves': self._noise_octaves,
            'noise_roughness': self._noise_roughness,
            'quadrants': self.quadrants,
            'graph': self.graph,
        }
