from ..__log__ import log_method as _log_method

from ._grid_processing import *
from ._terrain_processing import *
from ._terrain_processing import _COLORS 
import numpy as np
from collections import defaultdict
from uuid import uuid4
import pickle
import os as _os


saves_dir = 'grid_engine/_saves/'

_OCEAN_BLUE = _COLORS['OCEAN_BLUE']


def save_blueprint(blueprint):
    import os
    if not os.path.exists(f'{saves_dir}{blueprint.blueprint_id[-5:]}'):
        os.makedirs(f'{saves_dir}{blueprint.blueprint_id[-5:]}')
    with open(f'{saves_dir}{blueprint.blueprint_id[-5:]}/blueprint.{blueprint.blueprint_id[-5:]}.pkl', 'wb') as f:
        pickle.dump(blueprint, f)


def load_blueprint(num: int):
    import os
    with open(f'{saves_dir}{os.listdir(saves_dir)[-num]}/blueprint.{os.listdir(saves_dir)[-num][-5:]}.pkl', 'rb') as f:
        return pickle.load(f)


_levels = ['base', 'terrain', 'object', 'unit', 'zone', 'effect', 'fow']

# colors

_UNPASSABLE_TERRAIN = [
        'OCEAN', 'BLOCKED', 'MOUND', 'MOUNTAIN_BASE', 'MOUNTAIN_SIDE', 'MOUNTAIN_CRAG', 'MOUNTAIN_PEAK', 'HILL'
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
        ],
        'object':    [
                'items', 'obstructions', 'structures', 'features',
                'containers', 'doors', 'traps', 'switches'
        ],
        'unit':      [
                'players', 'npcs', 'monsters',
                'neutrals', 'pets', 'mounts'
        ],
        'zone':    [
                'areas', 'locales', 'regions',
                'cities', 'towns', 'villages'
        ],
        'effect':    [
                'weather', 'lighting',
                'environment', 'magic'
        ],
        'fow': [
                'visibility', 'explored',
                'seen', 'hidden'
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
    _dictObject = None
    _dictUnit = None
    _dictZone = None
    _dictEffect = None
    _dictFow = None
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
    def rank(self, rank: Optional[list[str]]) -> None:
        """Sets the rank of the grid."""
        self._rank = rank

    @property
    def file(self) -> list[str]:
        """Returns the file of the grid. The file is a list of strings that represent the columns of the grid."""
        return self._file

    @file.setter
    def file(self, file: Optional[list[str]]) -> None:
        """Sets the file of the grid."""
        self._file = file

    @property
    def cell_list(self) -> list[str]:
        """Returns the list of cells. The list of cells is a list of strings that represent the cells of the grid."""
        return self._cell_list

    @cell_list.setter
    def cell_list(self, cell_list: Optional[list[str]]) -> None:
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
        
    @property
    def dictGrid(self) -> dict[str, any]:
        """Returns the dictionary of cells."""
        return self._dictGrid

    @dictGrid.setter
    def dictGrid(self, dict_grid) -> None:
        """Sets the dictionary of cells. The value set here will be reflected in the array."""
        self._dictGrid = dict_grid
        
    @property
    def dictTerrain(self):
        """Returns the dictionary of terrain information. Which corresponds to the terrain layer of the array."""
        return self._dictTerrain

    @dictTerrain.setter
    def dictTerrain(self, dictTerrain) -> None:
        """Sets the dictionary of terrain information. Which corresponds to the terrain layer of the array. The value
        set here will be reflected in the array."""
        self._dictTerrain = dictTerrain
        for designation, terrain_info in dictTerrain.items():
            self.array[self.dictGrid[designation]['col_index']][self.dictGrid[designation]['row_index']][0] = terrain_info
        
    @property
    def dictObject(self):
        """Returns the dictionary of objects. Which corresponds to the object layer of the array."""
        return self._dictObject

    @dictObject.setter
    def dictObject(self, dictObject) -> None:
        """Sets the dictionary of objects. Which corresponds to the object layer of the array. The value set here will
        be reflected in the array."""
        self._dictObject = dictObject
        for designation, object_info in dictObject.items():
            self.array[self.dictGrid[designation]['col_index']][self.dictGrid[designation]['row_index']][1] = object_info
        

    @property
    def dictUnit(self):
        """Returns the dictionary of units. Which corresponds to the unit layer of the array."""
        return self._dictUnit

    @dictUnit.setter
    def dictUnit(self, dictUnit) -> None:
        """Sets the dictionary of units. Which corresponds to the unit layer of the array. The value set here will be
        reflected in the array."""
        self._dictUnit = dictUnit
        for designation, unit_info in dictUnit.items():
            self.array[self.dictGrid[designation]['col_index']][self.dictGrid[designation]['row_index']][2] = unit_info


    @property
    def dictZone(self):
        """Returns the dictionary of zones. Which corresponds to the zone layer of the array."""
        return self._dictZone

    @dictZone.setter
    def dictZone(self, dictZone) -> None:
        """Sets the dictionary of zones. Which corresponds to the zone layer of the array. The value set here will be"""
        self._dictZone = dictZone
        for designation, zone_info in dictZone.items():
            self.array[self.dictGrid[designation]['col_index']][self.dictGrid[designation]['row_index']][3] = zone_info



    @property
    def dictEffect(self):
        """Returns the dictionary of effects. Which corresponds to the effect layer of the array."""
        return self._dictEffect

    @dictEffect.setter
    def dictEffect(self, dictEffect) -> None:
        """Sets the dictionary of effects. Which corresponds to the effect layer of the array. The value set here will
        be reflected in the array."""
        self._dictEffect = dictEffect   
        for designation, effect_info in dictEffect.items():
            self.array[self.dictGrid[designation]['col_index']][self.dictGrid[designation]['row_index']][4] = effect_info


            
    @property
    def dictFow(self):
        """Returns the dictionary of fog of war. Which corresponds to the fog of war layer of the array."""
        return self._dictFow

    @dictFow.setter
    def dictFow(self, dictFow) -> None:
        """Sets the dictionary of fog of war. Which corresponds to the fog of war layer of the array. The value set"""
        self._dictFow = dictFow
        for designation, fow_info in dictFow.items():
            self.array[self.dictGrid[designation]['col_index']][self.dictGrid[designation]['row_index']][5] = fow_info
        

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
        array: np.ndarray = None, 
        quadrants: dict = None, 
        graph: dict = None
    ) -> None:
        super(BaseGridBlueprint, self).__init__()
        self.blueprint_id = uuid4().hex if grid_id is None else grid_id
        if array and quadrants and graph:
            self._array = array
            self._quadrants = quadrants
            self._graph = graph
            self._init_from_array()
        self.cell_size = cell_size if cell_size is not None else 10
        self.grid_dimensions = grid_dimensions if grid_dimensions is not None else (1000, 1000)
        self._array = np.array(
                [0 for _ in list(range((self._col_count * self._row_count) * (len(_levels)-1)))],
                dtype=type(any),
        ).reshape((self._col_count, self._row_count, len(_levels) - 1))
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
        self._init_layers()
                
    def _init_quadrants(self):
        quadrants = defaultdict(dict)
        quad_cells = defaultdict(list)
        for cell, information in self.dictGrid.items():
            quad_cells[information['quadrant_index']].append(cell)
        for quadrant_index, cell_list in quad_cells.items():
            # Create a dictionary of the cells in each quadrant
            quadrants[quadrant_index] = {
                    'cell_count': len(cell_list),
                    'cells':       cell_list
            }
        return quadrants

    def _init_layers(self):
        for i, level in enumerate(_levels):
            if i > 0:
                for cell, information in self.dictGrid.items():
                    # self.array[information['col_index']][information['row_index']][0] = information
                    self.array[information['col_index']][information['row_index']][i-1] = {f'{attr}': None for attr in _layer_attributes[level]}
                setattr(self, f'_dict{level.capitalize()}', self.array[:, :, i-1])
       
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

    @_log_method
    def _init_terrain(self, noise_scale, noise_octaves, noise_roughness):
        self._noise_scale = noise_scale if noise_scale is not None else 25
        self._noise_octaves = noise_octaves if noise_octaves is not None else 38
        self._noise_roughness = noise_roughness if noise_roughness is not None else 0.35
        self.dictTerrain = process_noise(self._noise_scale, self._noise_octaves, self._noise_roughness, self._row_count, self._col_count, self._cell_size, self.dictGrid)
        self._set_base_terrain()
        self._adjust_passability()

    @_log_method
    def _set_base_terrain(self):
        base_terrain = {
            'str': 'OCEAN',
            'raw': None,
            'int': 9,
            'color': _OCEAN_BLUE,
            'cost_in': float('inf'),
            'cost_out': float('inf'),
            'char': '~'
        }
        dictTerrain = self.dictTerrain.copy()
        for cell in self.cell_list:
            if self.dictTerrain[cell]['raw'] is None:
                dictTerrain[cell] = base_terrain
                self.dictGrid[cell]['passable'] = False
        self.dictTerrain = dictTerrain
    @_log_method
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
