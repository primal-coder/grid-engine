from __future__ import annotations as _annotations
from collections import deque as _deque

from abc import ABC as _ABC
from typing import Optional as _Optional

_ZONE_COLOR_MAP = {
        'regions' : (255, 0, 0, 255)
}


def capture_parentgrid(cls):
    def decorator(cell=None,  parentgrid=None):
        def __getstate__(self):
            state = self.__dict__.copy()
            del state['parentgrid']
            return state

        def __setstate__(self, state):
            self.__dict__.update(state)
            setattr(self, 'parentgrid', parentgrid)

        cls.__getstate__ = __getstate__
        cls.__setstate__ = __setstate__
        return cls

    return decorator

class _Grid(_ABC):
    pass
    
class _Neighborhood(_ABC):
    pass

class _AbstractCell:
    __slots__ = (
        'parentgrid', 
        'entry',
        'designation', 
        'cell_index', 
        'row_index', 
        'col_index', 
        'quadrant_index', 
        'coordinates', 
        'x', 
        'y', 
        'size', 
        'width', 
        'height', 
        'adjacent', 
        'quadrant', 
        'terrain_str', 
        'terrain_raw', 
        'terrain_int', 
        'terrain_color',
        'terrain_char', 
        'terrain_shape', 
        'groups', 
        'neighborhood', 
    )
    _up_left = None
    _up = None
    _up_right = None
    _clearance_up = None
    _down_right = None
    _down = None
    _down_left = None
    _clearance_down = None
    _clearance_y = None
    _left = None
    _clearance_left = None
    _right = None
    _clearance_right = None
    _clearance_x = None

    _cost_in = None
    _cost_out = None
    _array = None
    _entry_terrain = None
    _passable = None
    
    def __init__(self, cell_designation = None, row = None, col = None, parentgrid = None):
        self._null = None

    @property
    def null(self):
        return self._null

    @null.setter
    def null(self, value):
        self._null = value

    @property
    def up_left(self):
        """Returns the cell adjacent in the up-left direction"""
        if self.row == self.parentgrid.last_row or self.col == self.parentgrid.first_col:
            self._up_left = None
        else:
            self._up_left = self.parentgrid[self.adjacent[2]]
            # self._up_left = self.parentgrid.get_cell_by_position(self.x - self.size, self.y + self.size)
        return self._up_left

    @property
    def up(self):
        """Returns the cell adjacent in the up direction"""
        if self.row == self.parentgrid.last_row:
            self._up = None
        else:
            self._up = self.parentgrid[self.adjacent[3]]
            # self._up = self.col[self.col.index(self)+1]
        return self._up
    
    @property
    def up_right(self):
        """Returns the cell adjacent in the up-right direction"""
        if self.row == self.parentgrid.last_row or self.col == self.parentgrid.last_col:
            self._up_right = None
        else:
            self._up_right = self.parentgrid[self.adjacent[4]]
            # self._up_right = self.parentgrid.get_cell_by_position(self.x + self.size, self.y + self.size)
        return self._up_right
    
    @property
    def clearance_up(self):
        """Returns the number of cells in the up direction that are passable"""
        if self.row == self.parentgrid.last_row:
            self._clearance_up = 0
        else:
            clearance = 0
            place_in_col = self.col.index(self)
            col_len = len(self.col)
            steps_to_top = col_len - place_in_col
            for step in range(steps_to_top):
                if self.col[place_in_col + step].passable:
                    clearance += 1
                else:
                    break
            self._clearance_up = clearance
        return self._clearance_up

    @property
    def down_right(self):
        """Returns the cell adjacent in the down-right direction"""
        if self.row == self.parentgrid.first_row or self.col == self.parentgrid.last_col:
            self._down_right = None
        else:
            self._down_right = self.parentgrid[self.adjacent[6]]
            # self._down_right = self.parentgrid.get_cell_by_position(self.x + self.size, self.y - self.size)
        return self._down_right    
    
    @property
    def down(self):
        """Returns the cell adjacent in the down direction"""
        if self.row == self.parentgrid.first_row:
            self._down = None
        else:
            self._down = self.parentgrid[self.adjacent[7]]
            # self._down = self.col[self.col.index(self) - 1]
        return self._down

    @property
    def down_left(self):
        """Returns the cell adjacent in the down-left direction"""
        if self.row == self.parentgrid.first_row or self.col == self.parentgrid.first_col:
            self._down_left = None
        else:
            self._down_left = self.parentgrid[self.adjacent[0]]
            self._down_left = self.parentgrid.get_cell_by_position(self.x - self.size, self.y - self.size)
        return self._down_left

    @property
    def clearance_down(self):
        """Returns the number of cells in the down direction that are passable"""
        if self.row == self.parentgrid.first_row:
            self._clearance_down = 0
        else:
            clearance = 0
            place_in_col = self.col.index(self)
            steps_to_bottom = place_in_col
            for step in range(steps_to_bottom):
                if self.col[steps_to_bottom - step].passable:
                    clearance += 1
                else:
                    break
            self._clearance_down = clearance
        return self._clearance_down

    @property
    def clearance_y(self):
        """Returns the total number of cells in the up and down directions that are passable"""
        return self.clearance_up + self.clearance_down

    @property
    def left(self):
        """Returns the cell adjacent in the left direction"""
        if self.col == self.parentgrid.first_col:
            self._left = None
        else:
            self._left = self.parentgrid[self.adjacent[1]]
            # self._left = self.row[self.row.index(self) - 1]
        return self._left
    
    @property
    def clearance_left(self):
        """Returns the number of cells in the left direction that are passable"""
        if self.col == self.parentgrid.first_col:
            self._clearance_left = 0
        else:
            clearance = 0
            place_in_row = self.row.index(self)
            steps_to_left = place_in_row
            for step in range(steps_to_left):
                if self.row[steps_to_left - step].passable:
                    clearance += 1
                else:
                    break
            self._clearance_left = clearance
        return self._clearance_left

    @property
    def right(self):
        """Returns the cell adjacent in the right direction"""
        if self.col == self.parentgrid.last_col:
            self._right = None
        else:
            self._right = self.parentgrid[self.adjacent[5]]
        return self._right
    
    @property
    def clearance_right(self):
        """Returns the number of cells in the right direction that are passable"""
        if self.col == self.parentgrid.last_col:
            self._clearance_right = 0
        else:
            clearance = 0
            place_in_row = self.row.index(self)
            len_row = len(self.row)
            steps_to_right = len_row - place_in_row
            for step in range(steps_to_right):
                if self.row[place_in_row + step].passable:
                    clearance += 1
                else:
                    break
            self._clearance_right = clearance
        return self._clearance_right

    @property
    def clearance_x(self):
        """Returns the total number of cells in the left and right directions that are passable"""
        return self.clearance_left + self.clearance_right

    
    @property
    def cost_in(self):
        """Returns the cost to move into the cell"""
        return self._cost_in

    @property
    def cost_out(self):
        """Returns the cost to move out of the cell"""
        return self._cost_out

    @property
    def array(self):
        """Returns the array of the cell"""
        return self._array
    
    @array.setter
    def array(self, value):
        """Sets the array of the cell"""
        self._array = value
        self.entry = value[0]
        self.entry_terrain = value[1]
            
    @property
    def entry_terrain(self):
        """Returns the dict entry for the cell related to terrain"""
        return self._entry_terrain
    
    @entry_terrain.setter
    def entry_terrain(self, entry_terrain: dict[str, any]):
        """Sets the dict entry for the cell related to terrain"""
        self._entry_terrain = entry_terrain
        self._cost_in = entry_terrain['cost_in']
        self._cost_out = entry_terrain['cost_out']
    
    @property
    def passable(self):
        """Returns the passable value of the cell"""
        return self._passable
    
    @passable.setter
    def passable(self, value):
        """Sets the passable value of the cell. Additionally, the main entry and grid array are updated."""
        self._passable = value
        self.entry['passable'] = value
        self.array[0]['passable'] = value

   

def _dynamic_cell_decorator(cell: Cell = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(cell = cell, *args, **kwargs)
        return wrapper
    return decorator

class Cell(_AbstractCell):

    def __repr__(self):
        return str(f'{self.designation}({self.row_index}, {self.col_index})')

    def __init__(
            self,
            designation: _Optional[str] = None,
            row: _Optional[str] = None,
            col: _Optional[str] = None,
            parentgrid: _Optional[_Grid] = None,
    ) -> None:
        self.parentgrid = parentgrid
        if parentgrid is not None:
            self.with_terrain = self.parentgrid.with_terrain
            self.entry = self.parentgrid.blueprint.dictGrid[designation]

            self.designation = designation if designation is not None else row + col
            self.cell_index = self.entry['cell_index']

            self.row_name = designation[:-5] if row is None else row
            self.row_index = self.entry['row_index']

            self.col_name = designation[-5:] if col is None else col
            self.col_index = self.entry['col_index']

            self.array = self.parentgrid.grid_array[self.col_index][self.row_index]

            self.coordinates = self.entry['coordinates']
            self.x = self.coordinates[0]
            self.y = self.coordinates[1]

            self.size = self.parentgrid.cell_size
            self.width = self.size
            self.height = self.size

            self.adjacent = self.entry['adjacent']
            if self.with_terrain:
                self._entry_terrain = self.parentgrid.dictTerrain[self.designation]
                self.terrain_str = self.parentgrid.dictTerrain[self.designation]['str']
                self.terrain_raw = self.parentgrid.dictTerrain[self.designation]['raw']
                self.terrain_int = self.parentgrid.dictTerrain[self.designation]['int']
                self.terrain_color = self.parentgrid.dictTerrain[self.designation]['color']
                self.terrain_char = self.parentgrid.dictTerrain[self.designation]['char']

            self.overlay_color = None
            self.stored_overlay_color = None

            self.quadrant_index = self.entry['quadrant_index']
            self._passable = self.entry['passable']

            self.groups = {}
            self._in_zone = False
            self._in_region = False
            self._landmass_index = None
            self._body_of_water_index = None
            self._is_coastal = False

            for key, val in self.entry.items():
                if key not in list(self.entry)[:7]:
                    setattr(self, key, val)

            self.neighborhood = _Neighborhood
        
        # self.paint = None
        # self.paint = self.paint_terrain(batch=self.parentgrid.grid_batch)


    # def _setup_row_col(self):
    #     self.row = self.parentgrid.get_row_by_name(self.row_name)
    #     self.col = self.parentgrid.get_col_by_name(self.col_name)

    @property
    def row(self):
        """Returns the row of the cell"""
        return self.parentgrid.get_row_by_name(self.row_name)
    
    @property
    def col(self):
        """Returns the column of the cell"""
        return self.parentgrid.get_col_by_name(self.col_name)

    
    @property
    def in_zone(self):
        """Returns True if the cell is in a zone, False otherwise"""
        return self.entry_zone is not None
    
    @property
    def in_region(self):
        """Returns True if the cell is in a region, False otherwise"""
        return self.entry_zone['regions'] is not None

    @property
    def landmass_index(self):
        """Returns the landmass index of the cell"""
        return self._landmass_index

    @landmass_index.setter
    def landmass_index(self, value):
        """Sets the landmass index of the cell"""
        self._landmass_index = value

    @property
    def body_of_water_index(self):
        """Returns the body of water index of the cell"""
        return self._body_of_water_index
    
    @body_of_water_index.setter
    def body_of_water_index(self, value):
        """Sets the body of water index of the cell"""
        self._body_of_water_index = value

    @property
    def is_coastal(self):
        """Returns True if the cell is coastal, False otherwise"""
        return self._is_coastal
    
    @is_coastal.setter
    def is_coastal(self, value):
        """Sets the is_coastal value of the cell"""
        self._is_coastal = value
        
        
    def __lt__(self, other):
        return self.cell_index < other.cell_index
    
    def __le__(self, other):
        return self.cell_index <= other.cell_index
    
    def __eq__(self, other):
        return self.cell_index == other.cell_index
    
    def __ne__(self, other):
        return self.cell_index != other.cell_index
    
    def __gt__(self, other):
        return self.cell_index > other.cell_index
    
    def __ge__(self, other):
        return self.cell_index >= other.cell_index
    
    def __hash__(self):
        return hash(self.designation)
        
    def cell_decorator(self, func):
        """Decorator for cell methods that require the cell as an argument"""
        def wrapper(*args, **kwargs):
            return func(cell = self, *args, **kwargs)
        return wrapper
    
    def get_clearance_zone(self):
        """Returns a GridGroup of all cells in the clearance zone of the cell"""
        clearance_zone = GridGroup(self.parentgrid, f'{self.designation}_clearance_zone', [])
        clearance_in_row = []
        clearance_in_col = []
        for cell in self.row[self.row.index(self) - self.clearance_left:self.row.index(self) + self.clearance_right + 1]:
            clearance_in_row.append(cell)
            clearance_zone.add_cell(cell)
        for cell in self.col[self.col.index(self) - self.clearance_down:self.col.index(self) + self.clearance_up + 1]:
            clearance_in_col.append(cell)
            clearance_zone.add_cell(cell)
        for cell in clearance_in_row:
            for celly in cell.col[cell.col.index(cell) - cell.clearance_down:cell.col.index(cell) + cell.clearance_up + 1]:
                if celly.passable and celly != cell:
                    clearance_zone.add_cell(celly)
        for cell in clearance_in_col:
            for cellx in cell.row[cell.row.index(cell) - cell.clearance_left:cell.row.index(cell) + cell.clearance_right + 1]:
                if cellx.passable and cellx != cell:
                    clearance_zone.add_cell(cellx)
        for cell in clearance_zone.cells:
            if not cell.passable:
                clearance_zone.remove_cell(cell)
        return clearance_zone
    
    def get_diagonal(self, xaxis, yaxis, distance):
        """Returns a GridGroup of all cells in the diagonal of the cell in the specified direction and distance.
        
        Args:
            xaxis (int): -1 for left, 1 for right
            yaxis (int): -1 for down, 1 for up
            distance (int): The distance in cells of the diagonal
            
        Returns:
            GridGroup: The diagonal of the cell
        """
        diagonal = GridGroup(self.parentgrid, f'{self.designation}_diagonal', [])
        queue = _deque([self])
        ys = [None, 'up', 'down']
        xs = [None, 'right', 'left']
        y = ys[yaxis]
        x = xs[xaxis]
        for _ in range(distance):
            current_cell = queue.popleft()
            cell = getattr(current_cell, f'{y}_{x}')
            diagonal.add_cell(cell)
            queue.append(cell)
        return diagonal
                    
    def _set_quadrant(self):
        """Sets the quadrant of the cell based on the cell's designation."""
        for quadrant in self.parentgrid.quadrants:
            if self.designation in quadrant['cells']:
                self.quadrant_index = self.parentgrid.quadrants.index(quadrant)
                self.entry['quadrant_index'] = self.quadrant_index
                self.entry['quadrant'] = self.quadrant
                
    def get_groups(self):
        """Returns the groups of the cell."""
        return self.groups

    def join_group(self, group_name: _Optional[str] = None, group: _Optional[GridGroup] = None):
        """Adds a GridGroup to the cell. Updates the groups attribute. Also updates the grid array."""
        self.groups[group_name] = group

    def leave_group(self, group_name: str):
        """Removes a GridGroup from the cell. Updates the groups attribute. Also updates the grid array."""
        group = self.groups[group_name]
        group.remove_cell(self)
        self.groups = {key: value for key, value in self.groups.items() if key != group_name}

    def in_neighborhood(self, neighbor):
        """Returns True if the cell is in the neighborhood of the neighbor cell, False otherwise."""
        return self in neighbor.get_neighborhood()
    
    def paint_terrain(self, batch: _Optional[pyglet.graphics.Batch] = None):
        """Paints the terrain of the cell. The paint can be removed using the delete method."""
        return (
            pyglet.shapes.Rectangle(
                self.x,
                self.y,
                self.size,
                self.size,
                color=self.terrain_color,
                batch=batch,
            )
        )
        
    def update(self):
        """Updates the cell."""
        for key in self.entry.keys():
            if key not in list(self.entry.keys())[:5]:
                self.entry[key] = getattr(self, key)
        self.size = self.parentgrid.cell_size
        self.width = self.size
        self.height = self.size
        self.refresh()

    def refresh(self, dt):
        self.parentgrid.grid_array[self.file_index, self.rank_index] = self.array

    def __json__(self):
        return {
            "designation": self.designation,
            "coordinates": self.coordinates,
            "adjacent": self.adjacent,
            "groups": [group.__json__() for group in self.groups.values()]
        }