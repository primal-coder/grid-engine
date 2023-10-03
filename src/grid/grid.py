from __future__ import annotations

from .cell import *

from .blueprint import *

from .quiet_dict import QuietDict as _QuietDict

import pickle

import random

import heapq as _heapq

import itertools

from pymunk import Vec2d

from abc import ABC

from uuid import uuid4

from subprocess import call

from collections import deque

from random import choice as _choice

from typing import Optional as _Optional, Union as _Union

DODGER_BLUE = (16, 78, 139, 255)

saves_dir = '/devel/fresh/envs/project/src/grid/saves/'

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
    _grid_id = None
    _gen_terrain = None
    _blueprint = None
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
    
    def __init__(self, blueprint = None, cell_size = None, dimensions = None, noise_scale = None, noise_octaves = None, noise_roughness = None):
        super(AbstractGrid, self).__init__()
    
    @property
    def grid_id(self):
        return self._grid_id
    
    @grid_id.setter
    def grid_id(self, value):
        self._grid_id = value
        
    @property
    def gen_terrain(self):
        return self._gen_terrain
    
    @gen_terrain.setter
    def gen_terrain(self, value):
        self._gen_terrain = value
        
    @property
    def blueprint(self):
        return self._blueprint
    
    @blueprint.setter
    def blueprint(self, value):
        self._blueprint = value
        
    @property
    def grid_array(self):
        return self._grid_array
    
    @grid_array.setter
    def grid_array(self, value):
        self._grid_array = value
        
    @property
    def dictTerrain(self):
        return self._dictTerrain
    
    @dictTerrain.setter
    def dictTerrain(self, value):
        self._dictTerrain = value
        
    @property
    def grid_plan(self):
        return self._grid_plan
    
    @grid_plan.setter
    def grid_plan(self, value):
        self._grid_plan = value
        
    @property
    def init_cell_size(self):
        return self._init_cell_size
    
    @init_cell_size.setter
    def init_cell_size(self, value):
        self._init_cell_size = value
        
    @property
    def cell_size(self):
        return self._cell_size
    
    @cell_size.setter
    def cell_size(self, value):
        self._cell_size = value
        
    @property
    def cells(self):
        return self._cells
    
    @cells.setter
    def cells(self, value):
        self._cells = value
        
    @property
    def rows(self):
        return self._rows
    
    @rows.setter
    def rows(self, value):
        self._rows = value
        
    @rows.deleter
    def rows(self):
        del self._rows
        
    @property
    def cols(self):
        return self._cols
    
    @cols.setter
    def cols(self, value):
        self._cols = value
        
    @cols.deleter
    def cols(self):
        del self._cols
        
    @property
    def quadrants(self):
        return self._quadrants
    
    @quadrants.setter
    def quadrants(self, value):
        self._quadrants = value

    @quadrants.deleter
    def quadrants(self):
        del self._quadrants

    @property
    def first_col(self):
        return self._first_col
    
    @first_col.setter
    def first_col(self, value):
        self._first_col = value
    
    @first_col.deleter
    def first_col(self):
        del self._first_col
        
    @property
    def last_col(self):
        return self._last_col
    
    @last_col.setter
    def last_col(self, value):
        self._last_col = value
        
    @last_col.deleter
    def last_col(self):
        del self._last_col
        
    @property
    def first_row(self):
        return self._first_row
    
    @first_row.setter
    def first_row(self, value):
        self._first_row = value
        
    @first_row.deleter
    def first_row(self):
        del self._first_row
        
    @property
    def last_row(self):
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
    def __init__(
            self,
            blueprint: _Optional[type[Blueprint.AbstractGridBlueprint]] = None,
            cell_size: _Optional[int] = None,
            dimensions: _Optional[tuple[int, int]] = None,
            gen_terrain: _Optional[bool] = None,
            noise_scale: _Optional[float] = None,
            noise_octaves: _Optional[int] = None,
            noise_roughness: _Optional[float] = None            
    ):
        self.grid_id = uuid4().hex if blueprint is None else blueprint.blueprint_id
        self.gen_terrain = gen_terrain if gen_terrain is not None else True
        self.blueprint = blueprint if blueprint is not None else Blueprint.TerrainGridBlueprint(cell_size, dimensions, self.grid_id, noise_scale, noise_octaves, noise_roughness) if self._gen_terrain else BaseGridBlueprint(cell_size, dimensions, self.grid_id)
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
        self.get_first_last()
        self.selection = None
        self.set_rivers(2)
        
        for row in self.rows:
            row.row_index = self.rows.index(row)
        for col in self.cols:
            col.col_index = self.cols.index(col)


    def __getstate__(self):
        state = self.__dict__.copy()
        nonattrs = ['_cols', '_rows', '_quadrants', '_first_col', '_first_row', '_last_col', '_last_row']
        for nonattr in nonattrs:
            del state[nonattr]
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)


    def get_first_last(self):
        self._first_col = self.cols[0]
        self._last_col = self.cols[-1]
        self._first_row = self.rows[0]
        self._last_row = self.rows[-1]
    
    def _set_up(self):
        self._set_up_rank()
        self._set_up_file()
        self._set_up_quadrants()
        self._set_up_cells()
#        self._initgrid_objects()

    # def _setup_cell_row_col(self):
    #  
    #     for cell in self.cells.values():
    #         cell._setup_row_col()

    def _set_up_rank(self):
        setattr(self, 'rows', type('rows', (list,), {'blueprint': self.blueprint}))
        exec('self.rows = self.rows()')
        for height, row in enumerate(self.blueprint._rank):
            setattr(self.rows, f'row{row}',
                    type('Row', (list,), {'blueprint': self.blueprint, 'height': height * self.cell_size}))
            exec(f'self.rows.row{row} = self.rows.row{row}()')
            exec(f'self.rows.append(self.rows.row{row})')

    def _set_up_file(self):
        setattr(self, 'cols', type('cols', (list,), {'blueprint': self.blueprint}))
        exec('self.cols = self.cols()')
        for width, col in enumerate(self.blueprint._file):
            setattr(self.cols, f'col{col}',
                    type('Column', (list,), {'blueprint': self.blueprint, 'width': width * self.cell_size}))
            exec(f'self.cols.col{col} = self.cols.col{col}()')
            exec(f'self.cols.append(self.cols.col{col})')

    def _set_up_cells(self):
        for d, c in self.cells.items.items():
            getattr(self.rows, f'row{d[:-5]}').append(c)
            getattr(self.cols, f'col{d[-5:]}').append(c)
 
    def _set_up_quadrants(self):
        setattr(self, 'quadrants', type('quadrants', (list,), {}))
        exec('self.quadrants = self.quadrants()')
        for quadrant, info in self.blueprint._quadrants.items():
            setattr(self.quadrants, f'quad{quadrant}',
                    type('Quadrant', (_QuietDict,), {'__int__': lambda self: int(quadrant)}))
            exec(f'self.quadrants.quad{quadrant} = self.quadrants.quad{quadrant}()')
            exec(f'self.quadrants.append(self.quadrants.quad{quadrant})')
            exec(f'self.quadrants.quad{quadrant}.update({info})')

    def get_cell(self, cell_designation: _Optional[str] = None) -> _Optional[Cell]:
        try:
            return self.cells[cell_designation]
        except KeyError:
            return None

    def get_cell_by_index(self, index: _Optional[int] = None) -> _Optional[Cell]:
        try:
            return self.cells[self.blueprint._cell_list[index]]
        except KeyError:
            return None

    def get_cell_by_relative_indices(self, reference: _Optional[tuple[int, int]] = None, indices: _Optional[tuple[int, int]] = None):
        ref = V2(*reference)
        ind = V2(*indices)
        r, f = (ref + ind).int_tuple
        for cell in self.cells.values():
            if cell.rank_index == r and cell.file_index == f:
                return cell if cell.passable else None

    def get_nearest_cell_with(self, cella, attr_name, attr_val):
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
    
    def get_rank_by_index(self, index: _Optional[int] = None) -> _Optional[list[Cell,]]:
        return self.blueprint.rank[index]

    def get_rank_by_height(self, height: _Optional[int] = None) -> _Optional[list[Cell,]]:
        if self.cell_size == 1:
            return height
        for i in range(len(self.rows)):
            if self.rows[i].height <= height < self.rows[i + 1].height:
                return self.get_rank_by_index(i)

    def get_row_by_name(self, row_name: _Optional[str] = None) -> _Optional[list[Cell,]]:
        return getattr(self.rows, f'row{row_name}')
    
    def get_file_by_index(self, index: _Optional[int] = None) -> _Optional[list[Cell,]]:
        return self.blueprint.file[index]
    
    def get_file_by_width(self, width: _Optional[int] = None) -> _Optional[list[Cell,]]:
        if self.cell_size == 1:
            return width
        for i in range(len(self.cols)):
            if i == len(self.cols) - 1 or self.cols[i].width <= width < self.cols[i + 1].width:
                return self.get_file_by_index(i)
                    
    def get_col_by_name(self, col_name: _Optional[str] = None) -> _Optional[list[Cell,]]:
        return getattr(self.cols, f'col{col_name}')
    
    def get_cell_by_position(self, x: _Optional[int] , y: _Optional[int]) -> _Optional[Cell]:
        r = self.get_rank_by_height(y)
        f = self.get_file_by_width(x)
        return self.get_cell(f'{r}{f}')
    
    def get_cell_by_rank_file(self, rank: _Optional[int], file: _Optional[int]) -> _Optional[Cell]:
        r = self.get_rank_by_index(rank)
        f = self.get_file_by_index(file)
        for cell in r:
            if cell in f:
                return cell

    def random_cell(self, attr: Optional[tuple[str, Any]] = None) -> _Optional[Cell]:
        cell = self.cells[_choice(self.blueprint.cell_list)]
        if attr is not None:
            while getattr(cell, attr[0]) != attr[1]:
                cell = self.cells[_choice(self.blueprint.cell_list)]
        return cell
    
    def random_row(self) -> _Optional[list[Cell,]]:
        return _choice([getattr(self.rows, f'row{r}') for r in self.blueprint.rank])

    def random_col(self) -> _Optional[list[Cell,]]:
        return _choice([getattr(self.cols, f'col{c}') for c in self.blueprint.file])

    def get_adjacent(self, cell_designation: _Optional[str] = None) -> _Optional[list[Cell,]]:
        return [self.cells[adj] for adj in self.cells[cell_designation].adjacent]

    def get_neighbors(self, cell_designation: _Optional[str] = None) -> _Optional[list[Cell,]]:
        return [self.cells[adj].occupant for adj in self.cells[cell_designation].adjacent if
                self.cells[adj].occupant is not None]

    def get_distance(self, cella: _Optional[str] = None, cellb: _Optional[str] = None,
                     measurement: _Optional[str] = None) -> _Optional[int]:
        m = measurement if measurement is not None else "units"
        if m == "units":
            return self._heuristic(cella, cellb)
        if m == "cells":
            return self._heuristic(cella, cellb) // self.cell_size

    def get_path(
            self,
            cella: _Optional[_Union[Cell, str]] = None,
            cellb: _Optional[_Union[Cell, str]] = None
    ) -> _Optional[list[Cell,]]:
        if isinstance(cella, Cell):
            cella = cella.designation
        if isinstance(cellb, Cell):
            cellb = cellb.designation
        path = self._astar(cella, cellb)
        path.remove(cella)
        for count, step in enumerate(path):
            if not self[step].passable:
                path = path[:count]
                break
        return path
    
    def get_direction(
            self,
            cella: _Optional[_Union[Cell, str]] = None,
            cellb: _Optional[_Union[Cell, str]] = None
    ) -> _Optional[str]:
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
        path = self._astar(cella, cellb)
        path.remove(cella)
        if path == []:
            return None
        elif len(path) > 5:
            return get_vector_direction(self.cells[cella].coordinates, self.cells[path[5]].coordinates)

    def get_area(self, center_cell: _Optional[_Union[Cell, str]] = None, radius: _Optional[int] = None):
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

    def find_landmass_cells(self, center_cell):
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
    
    def find_coastal_cells(self, landmass_cells):
        """
        Finds and returns all cells that are adjacent to a landmass.

        Args:
            landmass_cells: List of cells belonging to the landmass.

        Returns:
            List of cells that are adjacent to a landmass.
        """
        coastal_cells = set()
        for landmass_cell in landmass_cells:
            for neighbor in landmass_cell.adjacent:
                neighbor_cell = self.cells[neighbor]
                if not neighbor_cell.passable:
                    coastal_cells.add(landmass_cell)
        return list(coastal_cells)
    
    def expand_river_path(self, path):
        expanded_path = []
        for i, cell in enumerate(path):
            cell = self.cells[cell]
            expanded_path.append(cell)
            adjacent_cells = cell.adjacent
            for adjacent_cell in adjacent_cells:
                adjacent_cell = self.cells[adjacent_cell]
                if adjacent_cell not in expanded_path:
                    expanded_path.append(adjacent_cell)
            if i % random.randint(1, 10) == 0:
                for _ in range(random.randint(1, 5)):
                    cell = expanded_path[-1]
                    adjacent_cells = cell.adjacent
                    for adjacent_cell in adjacent_cells:
                        adjacent_cell = self.cells[adjacent_cell]
                        if adjacent_cell not in expanded_path:
                            expanded_path.append(adjacent_cell)
        return expanded_path

    def shape_river_path(self, expanded_path):
        shaped_path = []
        for i, cell in enumerate(expanded_path):
            if i % 2 == 0:
                shaped_path.append(cell)
            else:
                previous_cell = expanded_path[i - 1]
                next_cell = expanded_path[i + 1] if i + 1 < len(expanded_path) else None
                if next_cell is not None:
                    direction = self.get_direction(previous_cell, next_cell)
                    if direction in DIRECTIONS.keys():
                        shaped_path.append(cell)
        return shaped_path

    def generate_realistic_river(self, start_cell: Cell, end_cell: Cell):
        paths = self.get_river_bends(start_cell, end_cell)
        path = list(itertools.chain.from_iterable(paths))
        if path is not None:
            expanded_path = self.expand_river_path(path)
#            shaped_path = self.shape_river_path(expanded_path)
            for cell in expanded_path:
                cell.terrain_str = 'river'
                cell.terrain_raw = 0.0
                cell.terrain_int = 9
                cell.terrain_color = DODGER_BLUE
                self.dictTerrain[cell.designation] = {
                    'str': cell.terrain_str, 
                    'raw': cell.terrain_raw, 
                    'int': cell.terrain_int, 
                    'color': cell.terrain_color, 
                    'cost_in': 2, 
                    'cost_out': 2
                    }        
        else:
            print("No path found between the start and end cells.")

    def get_river_ends(self, coastal_cells, length = 50):
        """
        Randomly chooses and returns a cell to use as the mouth of a river.

        Args:
            coastal_cells: List of cells that are adjacent to a landmass.

        Returns:
            Cell that is the mouth of a river.
        """
        start = random.choice(coastal_cells)
        end = self.random_cell(attr=("passable", True))
        while length + (length // 10) < self.get_distance(start.designation, end.designation) < length - (length//10):
            end = self.random_cell(attr=("passable", True))
        return start.designation, end.designation
        
    def get_river_bends(self, start, end):
        """
        Finds several paths between the ends of river and returns them in a list.
        
        Args:
            start: Cell that is the mouth of a river.
            end: Cell that is the end of a river.
            
        Returns:
            List of paths between the ends of a river.
        """
        if self.get_direction(start, end) in ['NE', 'E', 'SE']:
            paths = []
            path_count = self.get_distance(start, end, 'cells')// 10
            for _ in range(path_count):
                bend = self.random_cell(attr=('passable', True))
                while self.get_direction(end, bend) not in ['NW', 'W', 'SW']:
                    bend = self.random_cell(attr=('passable', True))
                if not paths:
                    paths.append(self.get_path(start, bend))
                else:
                    paths.append(self.get_path(paths[-1][-1], bend))
            paths.append(self.get_path(paths[-1][-1], end))
            return paths
        elif self.get_direction(start, end) in ['SW', 'W', 'NW']:
            paths = []
            path_count = self.get_distance(start, end, 'cells')// 10
            for _ in range(path_count):
                bend = self.random_cell(attr=('passable', True))
                while self.get_direction(end, bend) not in ['NE', 'E', 'SE']:
                    bend = self.random_cell(attr=('passable', True))
                if not paths:
                    paths.append(self.get_path(start, bend))
                else:
                    paths.append(self.get_path(paths[-1][-1], bend))
            paths.append(self.get_path(paths[-1][-1], end))
            return paths
        elif self.get_direction(start, end) in ['N', 'S']:
            paths = []
            path_count = self.get_distance(start, end, 'cells')// 10
            for _ in range(path_count):
                bend = self.random_cell(attr=('passable', True))
                while self.get_direction(end, bend) not in ['NE', 'E', 'SE', 'SW', 'W', 'NW']:
                    bend = self.random_cell(attr=('passable', True))
                if not paths:
                    paths.append(self.get_path(start, bend))
                else:
                    paths.append(self.get_path(paths[-1][-1], bend))
            paths.append(self.get_path(paths[-1][-1], end))
            return paths
    
    def set_rivers(self, river_count):
        for _ in range(river_count):
            print('finding landmass cells')
            landmass_cells = self.find_landmass_cells(self.random_cell(attr=('passable', True)))
            print('finding coastal cells')
            coastal_cells = self.find_coastal_cells(landmass_cells)
            print('getting river ends')
            start, end = self.get_river_ends(coastal_cells)
            print('bending river')
            self.generate_realistic_river(start, end)
            print('done')            
    # Define the _heuristic function

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
            _, current = _heapq.heappop(frontier)
            current_coords = self.cells[current].coordinates
            if current_coords == goal_coords:
                # We have found the goal, reconstruct the path and return it
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for next_step in graph[current]:
                """For each neighbor of the current node, calculate the _cost of the path from the start node to that 
                neighbor"""
                new_cost = cost_so_far[current] + self._cost(current, next_step)
                if next_step not in cost_so_far or new_cost < cost_so_far[
                    next_step]:  # If the new path is better than the old path
                    cost_so_far[next_step] = new_cost  # Update the cost of the path to the neighbor
                    priority = new_cost + self._heuristic(goal, next_step)  # Calculate the priority of the neighbor
                    _heapq.heappush(frontier, (priority, next_step))  # Add the neighbor to the frontier
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


class _Neighborhood:
    """A class to represent a neighborhood of cells.

    Args:
        grid (Grid): The grid object to which the neighborhood belongs.
        focus (Cell): The cell object that is the focus of the neighborhood.

    Attributes:
        grid (Grid): The grid object to which the neighborhood belongs.
        focus (Cell): The cell object that is the focus of the neighborhood.
        cell_addresses (list): A list of cell objects that are the addresses of the neighborhood.
        neighbors (list): A list of objects that are the occupants of the cells in the neighborhood
    """

    def __init__(self,
                 grid: _Optional[Grid] = None,
                 focus: _Optional[_Union[Cell, str]] = None,
                 ):
        self.grid = grid
        self.focus = focus
        self.cell_addresses = [self.grid.cells[address] for address in self.focus.adjacent]
        self.neighbors = [address.occupant for address in self.cell_addresses if address.occupied]

    def __call__(self):
        return self.cell_addresses

    def update(self):
        self.neighbors = [address.occupant for address in self.cell_addresses if address.occupied]
