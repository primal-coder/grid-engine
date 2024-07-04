from __future__ import annotations

from ..__log__ import log_method as _log_method

from abc import ABC
from typing import List, Tuple, Optional, Any, Union, AnyStr
import itertools
import random

RIVER_BLUE = (16, 78, 139, 255)
RIVERBANK_SAND = (188, 182, 134, 255)
RIVERBANK_GRASS = (105, 105, 105, 255)
RIVERBANK_MOUND = (112, 128, 136, 255)
FOREST_GREEN = (0, 155, 22, 255)

class Cell(ABC):
    pass

class Grid(ABC):
    pass

class Terraformer(ABC):
    def __init__(self, grid: Optional[Grid] = None):
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

    @_log_method
    def generate_realistic_river(self, start_cell: Cell, end_cell: Cell = None):
        # paths = self.get_river_bends(start_cell, end_cell)
        print('Generating river ...')
        path = self.get_river_by_walk(start_cell, end_cell)
        path = list(itertools.chain.from_iterable(path))
        path = [self.cells[cell] for cell in path]
        if path is not None:
            path = self.expand_river_path(path)
            step = 0
            total_steps = len(path)
            split = False
            # shaped_path = self.shape_river_path(expanded_path)
            for cell in path:
                step += 1
                cell.terrain_str = 'RIVER'
                cell.terrain_raw = 0.0
                cell.terrain_int = 9
                cell.terrain_color = RIVER_BLUE
                self.dictTerrain[cell.designation] = {
                    'str': cell.terrain_str, 
                    'raw': cell.terrain_raw, 
                    'int': cell.terrain_int, 
                    'color': cell.terrain_color, 
                    'cost_in': 2, 
                    'cost_out': 2
                    }                            
            self.grid.river_count += 1
            self.grid.rivers.append(path)
        else:
            print("No path found between the start and end cells.")

    @_log_method
    def expand_river_path(self, path):
        expanded_path = []
        for cell in path:
            expanded_path.append(cell)
            adjacent_cells = cell.adjacent
            for adjacent_cell in adjacent_cells:
                if adjacent_cell is not None:
                    adjacent_cell = self.cells[adjacent_cell]
                    if adjacent_cell not in expanded_path and adjacent_cell.passable and len(expanded_path) % 5: 
                        expanded_path.append(adjacent_cell)
        return expanded_path
    
    @_log_method
    def expand_riverbanks(self, riverbank_cells):
        for cell in riverbank_cells:
            adjacent_cells = cell.adjacent
            for adjacent_cell in adjacent_cells:
                if adjacent_cell is not None:
                    adjacent_cell = self.cells[adjacent_cell]
                    if adjacent_cell.terrain_str not in ['RIVER', 'RIVERBANK', 'OCEAN', 'SAND']:
                        if adjacent_cell.terrain_str in ['GRASS0', 'GRASS1', 'BEACH_GRASS', 'FOOTHILL']:
                            adjacent_cell.terrain_color = RIVERBANK_SAND
                        elif adjacent_cell.terrain_str == 'FOOTHILL':
                            adjacent_cell.terrain_color = RIVERBANK_GRASS
                        elif adjacent_cell.terrain_str == 'MOUND':
                            adjacent_cell.terrain_color = RIVERBANK_MOUND
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

    @_log_method
    def get_river_banks(self):
        riverbank_cells = []
        for cell in self.cells.values():
            if cell.terrain_str == 'RIVER':
                adjacent_cells = cell.adjacent
                for adjacent_cell in adjacent_cells:
                    if adjacent_cell is not None:
                        adjacent_cell = self.cells[adjacent_cell]
                        if adjacent_cell.terrain_str not in ['RIVER', 'OCEAN', 'SAND', 'MOUND', 'MOUNTAIN', 'HILL', 'LAKE', 'RIVERBANK']:
                            adjacent_cell.terrain_color = RIVERBANK_SAND
                        elif adjacent_cell.terrain_str == 'MOUND':
                            adjacent_cell.terrain_color = RIVERBANK_MOUND
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
                        riverbank_cells.append(adjacent_cell)
        return riverbank_cells


    def random_walk(self, river_cells: list[Cell,]):
        for step in range(random.randint(199, 201)):
            current_cell = self.cells[river_cells[-1]]
            if adjacent_cells := [
                adjacent_cell
                for adjacent_cell in current_cell.adjacent
                if adjacent_cell is not None and self.cells[adjacent_cell].passable
            ]:
                direction = (
                    direction
                    if (step % 20 != 0 or step == 0)
                    else direction - 2
                    if direction >= 2
                    else (direction + 2) % 8
                )
                next_cell = adjacent_cells[(direction + (0 if step % 3 else int(random.uniform(-5, 5)))) % len(adjacent_cells)]
                river_cells.append(next_cell)
        return river_cells

    def deliberate_walk(self, river_cells: list[Cell,], start_cell: Cell, end_cell: Cell):
        start_distance = self.grid.get_distance(start_cell, end_cell)
        current_distance = self.grid.get_distance(start_cell, end_cell)
        while current_distance > 1:
            current_cell = self.cells[river_cells[-1]]
            adjacent_cells = [adjacent_cell for adjacent_cell in current_cell.adjacent if adjacent_cell is not None and self.cells[adjacent_cell].passable and adjacent_cell not in river_cells]
            if not adjacent_cells:
                river_cells.pop(-1)
                break
            else:
                direction = random.randint(0, len(adjacent_cells)-1) if len(adjacent_cells) > 1 else 0
                next_cell = adjacent_cells[direction]
            check_ = 0
            while self.grid.get_distance(next_cell, end_cell) > current_distance and check_  < 8:
                direction += 1
                direction %= len(adjacent_cells)
                check_ += 1
                next_cell = adjacent_cells[direction]
                continue
            river_cells.append(next_cell)
            current_distance = self.grid.get_distance(next_cell, end_cell)
        return river_cells


    @_log_method
    def get_river_by_walk(self, start_cell: Cell, end_cell: Cell = None):
        river_cells = [start_cell]
        if end_cell is None:
            river_cells = self.random_walk(river_cells)
        else:
            river_cells = self.deliberate_walk(river_cells, start_cell, end_cell)
        return [river_cells]
        
    @_log_method
    def set_rivers(self, river_count):
        for river in range(river_count):
            if self.grid.river_count > 0 and not river % 3:
                start: Cell = random.choice(self.grid.rivers[-1])
                end: Cell = random.choice(self.grid.landmasses[start.landmass_index]['coastal_cells'])
            elif river > 2:
                if lake_coastal_cells := self.grid._get_lake_coastal_cells():
                    end: Cell = random.choice(lake_coastal_cells)
                else:
                    end: Cell = random.choice(coast_cells)
            else:
                landmass = self.grid._get_largest_landmass()
                coast_cells = landmass['coastal_cells']
                start: Cell = random.choice(coast_cells)
                if lake_coastal_cells := self.grid._get_lake_coastal_cells():
                    end: Cell = random.choice(lake_coastal_cells)
                else:
                    end: Cell = random.choice(coast_cells)
                while self.grid.get_distance(
                    start.designation, end.designation, 'cells'
                ) < 100 or not [
                    adjacent_cell
                    for adjacent_cell in start.adjacent
                    if adjacent_cell is not None and self.cells[adjacent_cell].passable
                ]:
                    start = random.choice(coast_cells)
                    end = random.choice(lake_coastal_cells) if lake_coastal_cells else random.choice(coast_cells)
            self.generate_realistic_river(start.designation, end.designation)
        riverbanks = self.get_river_banks()
        self.expand_riverbanks(riverbanks)
 
    def seed_forest(self):
        start_cell = self.grid.random_cell()
        while start_cell.clearance_left < 50 or start_cell.clearance_right < 50 or start_cell.clearance_up < 50 or start_cell.clearance_down < 50:
            start_cell = self.grid.random_cell()
        return start_cell

    def find_forest_points(self, start_cell: Cell):
        forest_border_NW = self.grid[start_cell.get_diagonal(-1, -1, random.choice([10,12,16,20]))[-1]]
        forest_border_NE = self.grid[start_cell.get_diagonal(-1, 1, random.choice([10,12,16,20]))[-1]]
        forest_border_SE = self.grid[start_cell.get_diagonal(1, 1, random.choice([10,12,16,20]))[-1]]
        forest_border_SW = self.grid[start_cell.get_diagonal(1, -1, random.choice([10,12,16,20]))[-1]]
        return (forest_border_NW, forest_border_NE, forest_border_SE, forest_border_SW)
        
    def get_forest_borders(self, forest_points: Tuple[Cell, Cell, Cell, Cell]):
        forest_border = []
        for step in range(4):
            forest_step = self.grid.get_walk(forest_points[step], forest_points[(step+1)%4])
            forest_border.extend(forest_step)
        return forest_border

    def expand_forest_border(self, forest_border):
        expanded_forest_border = []
        for cell in forest_border:
            cell = self.grid[cell]
            for adjacent in cell.adjacent:
                if adjacent is not None:
                    adjacent = self.grid[adjacent]
                    if adjacent.passable:
                        expanded_forest_border.append(adjacent.designation)
            expanded_forest_border.append(cell.designation)
        return expanded_forest_border
        
    def get_most_distant_forest_border(self, forest_border, direction):
        most_distant = None
        for cell in forest_border:
            cell = self.grid[cell]
            if most_distant is None:
                most_distant = cell
            else:
                if direction == 'N':
                    if cell.y < most_distant.y:
                        most_distant = cell
                elif direction == 'S':
                    if cell.y > most_distant.y:
                        most_distant = cell
                elif direction == 'E':
                    if cell.x > most_distant.x:
                        most_distant = cell
                elif direction == 'W':
                    if cell.x < most_distant.x:
                        most_distant = cell
        return most_distant
        
    def get_inner_forest_cells(self, start_cell, forest_border):
        for cell in forest_border:
            cell = self.grid[cell]
            for adjacent in cell.adjacent:
                if adjacent is not None:
                    adjacent = self.grid[adjacent]
                    adjacent.passable = False
            cell.passable = False
        inner_forest_cells = start_cell.get_clearance_zone()
        inner_forest_cells = inner_forest_cells.cells
        for cell in inner_forest_cells:
            if cell in forest_border:
                inner_forest_cells.remove(cell)
        for cell in forest_border:
            cell = self.grid[cell]
            for adjacent in cell.adjacent:
                if adjacent is not None:
                    adjacent = self.grid[adjacent]
                    adjacent.passable = True
            cell.passable = True
        forest_cells = []
        forest_cells.extend(forest_border)
        for cell in inner_forest_cells:
            forest_cells.append(cell.designation)
        return forest_cells
    
    def set_forest(self):
        start_cell = self.seed_forest()
        forest_points = self.find_forest_points(start_cell)
        forest_borders = self.get_forest_borders(forest_points)
        expanded_forest_borders = self.expand_forest_border(forest_borders)
        forest_cells = self.get_inner_forest_cells(start_cell, expanded_forest_borders)
        for cell in forest_cells:
            cell = self.grid[cell]
            cell.terrain_str = 'FOREST'
            cell.terrain_raw = 0.0
            cell.terrain_int = 4
            cell.terrain_color = FOREST_GREEN
            cell.terrain_char = '^'
            self.dictTerrain[cell.designation] = {
                'str': cell.terrain_str, 
                'raw': cell.terrain_raw, 
                'int': cell.terrain_int, 
                'color': cell.terrain_color, 
                'cost_in': 2, 
                'cost_out': 2,
                'char': '^'
                }
