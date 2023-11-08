import itertools
import random
from . import Blueprint
from . import Grid

from collections import deque

def generate_blueprint(dimensions: tuple[int, int] = None):
    blueprint = Blueprint.BaseGridBlueprint(cell_size=1, grid_dimensions=dimensions)
    for cell in blueprint.dictGrid.copy():
            blueprint.dictGrid[cell]['passable'] = True
    terrain_dict = {
        cell: {'str': 'NULL', 'raw': 0, 'int': 0, 'color': None, 'cost_in': None, 'cost_out': None, 'char': None}
        for cell in blueprint.dictGrid
    }
    blueprint.dictTerrain = terrain_dict
    return blueprint

class Dungeon(Grid.Grid):
    def __init__(self, dimensions):
        blueprint = generate_blueprint(dimensions)
        blueprint = self.init_fill(blueprint)
        super().__init__(blueprint, with_terrain=False)
        
    def init_fill(self, blueprint):
        limit = (blueprint.col_count * blueprint.row_count * 2) // 5
        count = 0
        while count < limit:
            cell = random.choice(blueprint.cell_list)
            if blueprint.dictTerrain[cell]['raw'] == 0:
                blueprint.dictTerrain[cell]['raw'] = 1
                blueprint.dictTerrain[cell]['int'] = 1
                blueprint.dictTerrain[cell]['str'] = 'BASE'
                count += 1
        return blueprint
            
    def get_edge_cells(self):
        return sorted(self.first_row + self.last_row + self.first_col + self.last_col, key=lambda cell: cell.cell_index)

    def pass_one(self):
        for i, j in itertools.product(range(self.blueprint.col_count), range(self.blueprint.row_count)):
            count = 0
            cell = self[(i, j)]
            for adj in cell.adjacent:
                adj = self[adj]
                if adj.terrain_raw == 1:
                    count += 1
            self.dictTerrain[cell.designation] = (
                {
                    'str': 'NULL',
                    'raw': 0,
                    'int': 0,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                }
                if count in [0, 1, 2]
                else {
                    'str': 'BASE',
                    'raw': 1,
                    'int': 1,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                } if count in [5, 6, 7, 8]
                else {
                    'str': 'NULL',
                    'raw': 0,
                    'int': 0,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                }
            )
    
    def pass_two(self):
        for i, j in itertools.product(range(self.blueprint.col_count), range(self.blueprint.row_count)):
            count = 0
            cell = self[(i, j)]
            for adj in cell.adjacent:
                adj = self[adj]
                if adj.terrain_raw == 1:
                    count += 1
            self.dictTerrain[cell.designation] = (
                {
                    'str': 'NULL',
                    'raw': 0,
                    'int': 0,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                }
                if count == 5
                else {
                    'str': 'BASE',
                    'raw': 1,
                    'int': 1,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                }
            )
            
    def pass_three(self):
        for i, j in itertools.product(range(self.blueprint.col_count), range(self.blueprint.row_count)):
            count = 0
            cell = self[(i, j)]
            for adj in cell.adjacent:
                adj = self[adj]
                if adj.terrain_raw == 1:
                    count += 1
            self.dictTerrain[cell.designation] = (
                {
                    'str': 'NULL',
                    'raw': 0,
                    'int': 0,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                }
                if count > 2
                else {
                    'str': 'BASE',
                    'raw': 1,
                    'int': 1,
                    'color': None,
                    'cost_in': None,
                    'cost_out': None,
                    'char': None,
                }
            )
            
                    