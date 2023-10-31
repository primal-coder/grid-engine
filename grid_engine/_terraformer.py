from __future__ import annotations as _annotations

from abc import ABC as _ABC
from typing import Optional as _Optional
import itertools as _itertools
import random as _random


_RIVER_BLUE = (16, 78, 139, 255)
_RIVERBANK_SAND = (188, 182, 134, 255)
_RIVERBANK_GRASS = (90, 154, 90, 255)


class Cell(_ABC):
    pass

class Grid(_ABC):
    pass

class Terraformer(_ABC):
    def __init__(self, grid: _Optional[Grid] = None):
        self._grid = grid
        
    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def cells(self):
        return self.grid.cells
    
    @property
    def dictTerrain(self) -> dict:
        return self.grid.dictTerrain
    
    @property
    def landmasses(self) -> dict:
        return self.grid.landmasses 
    
    @property
    def river_count(self) -> int:
        return self.grid.river_count
    
    @river_count.setter
    def river_count(self, value: int):
        self.grid.river_count = value
        
    @property
    def rivers(self) -> list[list[Cell,]]:
        self.grid.rivers

    def generate_realistic_river(self, start_cell: Cell, end_cell: Cell = None):
        # paths = self.get_river_bends(start_cell, end_cell)
        print('Getting river cells by walk ...')
        path = self.get_river_by_walk(start_cell, end_cell)
        path = list(_itertools.chain.from_iterable(path))
        print(f'River steps: {len(path)}')
        if path is not None:
            expanded_path = self.expand_river_path(path)
            # shaped_path = self.shape_river_path(expanded_path)
            for cell in expanded_path:
                cell.terrain_str = 'RIVER'
                cell.terrain_raw = 0.0
                cell.terrain_int = 9
                cell.terrain_color = _RIVER_BLUE
                self.dictTerrain[cell.designation] = {
                    'str': cell.terrain_str, 
                    'raw': cell.terrain_raw, 
                    'int': cell.terrain_int, 
                    'color': cell.terrain_color, 
                    'cost_in': 2, 
                    'cost_out': 2
                    }        
            self.grid.river_count += 1
            self.grid.rivers.append(expanded_path)
        else:
            print("No path found between the start and end cells.")

    def expand_river_path(self, path):
        expanded_path = []
        for cell in path:
            cell = self.cells[cell]
            expanded_path.append(cell)
            adjacent_cells = cell.adjacent
            for adjacent_cell in adjacent_cells:
                adjacent_cell = self.cells[adjacent_cell]
                if adjacent_cell not in expanded_path and adjacent_cell.passable:
                    expanded_path.append(adjacent_cell)
        return expanded_path

    def get_river_banks(self):
        for cell in self.cells.values():
            if cell.terrain_str == 'RIVER':
                adjacent_cells = cell.adjacent
                for adjacent_cell in adjacent_cells:
                    adjacent_cell = self.cells[adjacent_cell]
                    if adjacent_cell.terrain_str == 'RIVER':
                        continue
                    if adjacent_cell.terrain_str not in ['RIVER', 'OCEAN', 'SAND', 'MOUND', 'HILL']:
                        adjacent_cell.terrain_color = _RIVERBANK_SAND
                    elif adjacent_cell.terrain_str == 'MOUND':
                        adjacent_cell.terrain_color = _RIVERBANK_GRASS
                    adjacent_cell.terrain_str = 'RIVERBANK'
                    adjacent_cell.terrain_raw = 0.0
                    adjacent_cell.terrain_int = 8
                    self.dictTerrain[adjacent_cell.designation] = {
                        'str': adjacent_cell.terrain_str, 
                        'raw': adjacent_cell.terrain_raw, 
                        'int': adjacent_cell.terrain_int, 
                        'color': adjacent_cell.terrain_color, 
                        'cost_in': 1, 
                        'cost_out': 2
                    }

    def get_river_by_walk(self, start_cell: Cell, end_cell: Cell = None):
        river_cells = [start_cell]
        # branch_cells = []
        direction = 5
        if end_cell is None:
            print('Generating _random river ...')
            for step in range(_random.randint(199, 201)):
                current_cell = self.cells[river_cells[-1]]
                if adjacent_cells := [
                    adjacent_cell
                    for adjacent_cell in current_cell.adjacent
                    if self.cells[adjacent_cell].passable
                ]:
                    direction = (
                        direction
                        if (step % 20 != 0 or step == 0)
                        else direction - 2
                        if direction >= 2
                        else (direction + 2) % 8
                    )
                    next_cell = adjacent_cells[(direction + (0 if step % 3 else int(_random.uniform(-5, 5)))) % len(adjacent_cells)]
                    river_cells.append(next_cell)
        else:
            print('Generating river with end designated ...')
            start_distance = self.grid.get_distance(start_cell, end_cell)
            current_distance = self.grid.get_distance(start_cell, end_cell)
            while current_distance > 1:
                current_cell = self.cells[river_cells[-1]]
                adjacent_cells = [adjacent_cell for adjacent_cell in current_cell.adjacent if self.cells[adjacent_cell].passable and adjacent_cell not in river_cells]
                if not adjacent_cells:
                    river_cells.pop(-1)
                    break
                else:
                    direction = _random.randint(0, len(adjacent_cells)-1) if len(adjacent_cells) > 1 else 0
                    next_cell = adjacent_cells[direction]
                check_ = 0
                while self.grid.get_distance(next_cell, end_cell) > current_distance + 2 and check_  < 8:
                    print(f'Current distance: {current_distance} | Current cell: {current_cell.designation} | Next cell: {next_cell}', end='\r')
                    direction += 1
                    direction %= len(adjacent_cells)
                    check_ += 1
                    next_cell = adjacent_cells[direction]
                    continue
                river_cells.append(next_cell)
                current_distance = self.grid.get_distance(next_cell, end_cell)
            print(f'Cells in river: {len(river_cells)}')
        return [river_cells]
        
    def set_rivers(self, river_count):
        print('Finding start to river ...')
        for river in range(river_count):
            if self.grid.river_count > 0 and not river % 3:
                start: Cell = _random.choice(self.grid.rivers[-1])
                end: Cell = _random.choice(self.grid.landmasses[start.landmass_index]['coastal_cells'])
            elif river > 2:
                if lake_coastal_cells := self.grid._get_lake_coastal_cells():
                    end: Cell = _random.choice(lake_coastal_cells)
                else:
                    end: Cell = _random.choice(coast_cells)
            else:
                landmass = self.grid._get_largest_landmass()
                coast_cells = landmass['coastal_cells']
                start: Cell = _random.choice(coast_cells)
                if lake_coastal_cells := self.grid._get_lake_coastal_cells():
                    end: Cell = _random.choice(lake_coastal_cells)
                else:
                    end: Cell = _random.choice(coast_cells)
                print('Validating start/end of river ...')
                print(f'Start cell: {start}, End cell: {end}', end = '\r')
                while self.grid.get_distance(
                    start.designation, end.designation, 'cells'
                ) < 5000 and not [
                    adjacent_cell
                    for adjacent_cell in start.adjacent
                    if self.cells[adjacent_cell].passable
                ]:
                    start = _random.choice(coast_cells)
                    end = _random.choice(lake_coastal_cells) if lake_coastal_cells else _random.choice(coast_cells)
                    print(f'Start cell: {start}, End cell: {end}', end = '\r')
            print(f'Start cell: {start}, End cell: {end}')
            print('Building river ...')
            self.generate_realistic_river(start.designation, end.designation)
        self.get_river_banks()
        print('done')            
 