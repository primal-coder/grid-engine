from __future__ import annotations

from collections import deque

from .._grid_group import GridGroup

import logging as _logging

from abc import ABC
from typing import Optional as _Optional, Union as _Union
import weakref
import numpy as np
import pyglet


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

class Grid(ABC):
    pass
    
class AbstractGridObject(ABC):
    pass

class _Neighborhood(ABC):
    pass

class CellEventMeta(type):
    _EVENT_TYPES = ['on_occupy', 'on_vacate', 'on_construct', 'on_destruct', 'on_entitle', 'on_divest']
    _HANDLER_TYPES = ['occupy', 'vacate', 'construct', 'destruct', 'entitle', 'divest']
    dispatcher = pyglet.event.EventDispatcher()
    for event_type, handler_type in zip(_EVENT_TYPES, _HANDLER_TYPES):
        dispatcher.register_event_type(event_type)

    def __new__(cls, name, bases, attrs):
        attrs['dispatcher'] = cls.dispatcher
        return type.__new__(cls, name, bases, attrs)


class AbstractCell(metaclass=type):
    """Abstract cell class. Contains the basic attributes and methods of a cell."""
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
    _entry_object = None
    _entry_unit = None
    _entry_zone = None
    _entry_effect = None
    _entry_fow = None
    _passable = None
    
    _occupied = False
    _occupant = None
    _constructed = False
    _construction = None

    _entitled = False
    _title = None
    _entity = None

    
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
            self._up_left = self.parentgrid[self.adjacent[0]]
            # self._up_left = self.parentgrid.get_cell_by_position(self.x - self.size, self.y + self.size)
        return self._up_left

    @property
    def up(self):
        """Returns the cell adjacent in the up direction"""
        if self.row == self.parentgrid.first_row:
            self._up = None
        else:
            self._up = self.parentgrid[self.adjacent[1]]
            # self._up = self.col[self.col.index(self)+1]
        return self._up
    
    @property
    def up_right(self):
        """Returns the cell adjacent in the up-right direction"""
        if self.row == self.parentgrid.first_row or self.col == self.parentgrid.last_col:
            self._up_right = None
        else:
            self._up_right = self.parentgrid[self.adjacent[2]]
            # self._up_right = self.parentgrid.get_cell_by_position(self.x + self.size, self.y + self.size)
        return self._up_right
    
    @property
    def clearance_up(self):
        """Returns the number of cells in the up direction that are passable"""
        if self.row == self.parentgrid.first_row:
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
        if self.row == self.parentgrid.last_row or self.col == self.parentgrid.last_col:
            self._down_right = None
        else:
            self._down_right = self.parentgrid[self.adjacent[4]]
            # self._down_right = self.parentgrid.get_cell_by_position(self.x + self.size, self.y - self.size)
        return self._down_right    
    
    @property
    def down(self):
        """Returns the cell adjacent in the down direction"""
        if self.row == self.parentgrid.last_row:
            self._down = None
        else:
            self._down = self.parentgrid[self.adjacent[5]]
            # self._down = self.col[self.col.index(self) - 1]
        return self._down

    @property
    def down_left(self):
        """Returns the cell adjacent in the down-left direction"""
        if self.row == self.parentgrid.last_row or self.col == self.parentgrid.first_col:
            self._down_left = None
        else:
            self._down_left = self.parentgrid[self.adjacent[6]]
            # self._down_left = self.parentgrid.get_cell_by_position(self.x - self.size, self.y - self.size)
        return self._down_left

    @property
    def clearance_down(self):
        """Returns the number of cells in the down direction that are passable"""
        if self.row == self.parentgrid.last_row:
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
            self._left = self.parentgrid[self.adjacent[7]]
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
            self._right = self.parentgrid[self.adjacent[3]]
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
    def clearance_zone(self):
        """Returns the clearance zone of the cell"""
        return self.get_clearance_zone()
    
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
        self.array[0, 0] = entry_terrain
    
    @property
    def entry_object(self):
        """Returns the dict entry for the cell related to objects"""
        return self._entry_object
    
    @entry_object.setter
    def entry_object(self, entry_object: dict[str, any]):
        """Sets the dict entry for the cell related to objects"""
        self._entry_object = entry_object
        self.array[0, 1] = entry_object
            
    @property
    def entry_unit(self):
        """Returns the dict entry for the cell related to units"""
        return self._entry_unit
    
    @entry_unit.setter
    def entry_unit(self, entry_unit: dict[str, any]):
        """Sets the dict entry for the cell related to units"""
        self._entry_unit = entry_unit
        self.array[0, 2] = entry_unit
        
    @property
    def entry_zone(self):
        """Returns the dict entry for the cell related to zones"""
        return self._entry_zone
    
    @entry_zone.setter
    def entry_zone(self, entry_zone: dict[str, any]):
        """Sets the dict entry for the cell related to zones"""
        self._entry_zone = entry_zone
        self.array[0, 3] = entry_zone
        
    @property
    def entry_effect(self):
        """Returns the dict entry for the cell related to effects"""
        return self._entry_effect
    
    @entry_effect.setter
    def entry_effect(self, entry_effect: dict[str, any]):
        """Sets the dict entry for the cell related to effects"""
        self._entry_effect = entry_effect
        self.array[0, 4] = entry_effect
        
    @property
    def entry_fow(self):
        """Returns the dict entry for the cell related to fog of war"""
        return self._entry_fow
    
    @entry_fow.setter
    def entry_fow(self, entry_fow: dict[str, any]):
        """Sets the dict entry for the cell related to fog of war"""
        self._entry_fow = entry_fow
        self.array[0, 5] = entry_fow
        
    @property
    def passable(self):
        """Returns the passable value of the cell"""
        return self._passable
    
    @passable.setter
    def passable(self, value):
        """Sets the passable value of the cell. Additionally, the main entry and grid array are updated."""
        self._passable = value
        self.entry['passable'] = value
        
    @property
    def occupied(self):
        """Returns True if the cell is occupied, False otherwise"""
        return self._occupied
    
    @occupied.setter
    def occupied(self, value):
        """Sets the occupied value of the cell"""
        self._occupied = value
        
    @property
    def occupant(self):
        """Returns the occupant of the cell"""
        return self._occupant
    
    @occupant.setter
    def occupant(self, value):
        """Sets the occupant of the cell"""
        self._occupant = value
        
    @property
    def constructed(self):
        """Returns True if the cell is constructed, False otherwise"""
        return self._constructed
    
    @constructed.setter
    def constructed(self, value):
        """Sets the constructed value of the cell"""
        self._constructed = value
        
    @property
    def construction(self):
        """Returns the construction of the cell"""
        return self._construction
    
    @construction.setter
    def construction(self, value):
        """Sets the construction of the cell"""
        self._construction = value

    @property
    def entitled(self):
        """Returns True if the cell is entitled, False otherwise"""
        return self._entitled
    
    @entitled.setter
    def entitled(self, value):
        """Sets the entitled value of the cell"""
        self._entitled = value
        
    @property
    def title(self):
        """Returns the title of the cell"""
        return self._title
    
    @title.setter
    def title(self, value):
        """Sets the title of the cell"""
        self._title = value
    
    @property
    def entity(self):
        """Returns the entity of the cell"""
        return self._entity

    @entity.setter
    def entity(self, value):
        """Sets the entity of the cell"""
        self._entity = value

def _dynamic_cell_decorator(cell: Cell = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(cell = cell, *args, **kwargs)
        return wrapper
    return decorator

class Cell(AbstractCell, metaclass=CellEventMeta):

    def __repr__(self):
        return str(f'{self.designation}({self.row_index}, {self.col_index})')

    def __init__(
            self,
            designation: _Optional[str] = None,
            row: _Optional[str] = None,
            col: _Optional[str] = None,
            parentgrid: _Optional[Grid] = None,
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

            self._array = np.array([{} for _ in range(6)], dtype=type(any)).reshape(1, 6)

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
                self._cost_in = self.parentgrid.dictTerrain[self.designation]['cost_in']
                self._cost_out = self.parentgrid.dictTerrain[self.designation]['cost_out']
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
            
            self._shape = None

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
        
    @property
    def shape(self):
        """Returns the shape of the cell"""
        return self._shape
    
    @shape.setter
    def shape(self, value):
        """Sets the shape of the cell"""
        self._shape = value

    def __lt__(self, other):
        return self.cell_index < other.cell_index
    
    def __le__(self, other):
        return self.cell_index <= other.cell_index
    
    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.cell_index == other.cell_index
        
    def __contains__(self, cells):
        if isinstance(cells, list):
            return self.cell_index in [cell.cell_index for cell in cells]

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
        diagonal = []
        queue = deque([self])
        ys = [None, 'up', 'down']
        xs = [None, 'right', 'left']
        y = ys[yaxis]
        x = xs[xaxis]
        for _ in range(distance):
            current_cell = queue.popleft()
            cell = getattr(current_cell, f'{y}_{x}')
            if cell is not None:
                diagonal.append(cell.designation)
                queue.append(cell)
            else:
                break
        return diagonal
    
    def recv_occupant(self, occupant):
        """
        Receives an occupant signal from a GridEntity. 
        Triggers the dispatcher for the 'on_vacate' event if the cell is occupied 
        and the value of occupant is the same as the value of self.occupant. 
        Triggers the dispatcher of the 'on_occupy' event if the cell is unoccupied.
        
        GridEntity <-> 'recv_occupant'
        |               ||          ||
        |               Cell(In)    Cell(out)
        |               ||          ||
        |               'on_vacate' 'on_occupy'
        |               ||          ||
        |___________'remove_unit'_'add_unit'________GridArray
                                                        ||
                                                    [0, 0, b]
        
        
        
        """
        if self.occupant is not None:
            if self.occupant == occupant:
                self.on_vacate()
                return
            return
        self.on_occupy(occupant)
        return
                
    def on_entitle(self, entity):
        """Sets the cell as entitled by an entity. Updates the title and entity attributes. Handles the on_entitle event."""
        self.entitled = True
        self.entity = entity
        self.title = entity.title

    def on_divest(self):
        """Sets the cell as unentitled. Updates the title and entity attributes. Handles the on_divest event."""
        self.entitled = False
        self.entity = None
        self.title = None

    def on_occupy(self, occupant):
        """Sets the cell as occupied by an occupant. Updates the occupant attribute."""
        self.occupant = occupant
        self.add_unit(occupant)
        self.occupied = True

    def on_vacate(self):
        """Sets the cell as unoccupied. Updates the occupant attribute. Handles the on_vacate event."""
        self.remove_unit(self.occupant)
        self.occupant = None
        self.occupied = False

    def on_construct(self, construction):
        """Sets the cell as constructed. Updates the construction attribute. Handles the on_construct event."""
        self.constructed = True
        self.construction = construction

    def on_destruct(self):
        """Sets the cell as unconstructed. Updates the construction attribute. Handles the on_destruct event."""
        self.passable = True
        self.constructed = False
        self.construction = None

    def dig(self):
        self.terrain_str = 'GROUND'
        self.terrain_raw = 0
        self.terrain_int = 0
        self.terrain_color = None
        self.terrain_char = ' '
        self.terrain_shape = None
        self.passable = True

    def build(self, orientation: _Optional[bool] = None):
        if orientation is not None:
            self.terrain_char = '|' if orientation else '-'
        self.terrain_str = 'WALL'
        self.terrain_raw = 1
        self.terrain_int = 3
        self.passable = False

    def add_object(self, grid_object: AbstractGridObject):
        """Adds a GridObject to the cell. Updates the entry_object attribute. Also updates the grid array.
        If the object is a structure, the on_construct event is handled. If the object has a tile_color attribute, the overlay is painted. 
        If the object has a passable attribute, the passable attribute of the cell is updated."""
        otype = f'{grid_object.object_type}s'
        if self.entry_object[f'{otype}'] is None:
            self.entry_object[f'{otype}'] = {}
        self.entry_object[f'{otype}'].update({grid_object.name: grid_object})
        self.parentgrid.dictObject[self.col_index][self.row_index] = self.entry_object
        if otype == 'items':
            if hasattr(grid_object, 'tile_color') and getattr(self.parentgrid, 'scene', None) is not None:
                self.overlay_color = grid_object.tile_color
                self.overlay = self.paint_overlay(batch=self.parentgrid.scene.batch_delegate.cell_batch)

        elif otype == 'structures':
            self.on_construct(grid_object)
            if hasattr(grid_object, 'tile_color') and getattr(self.parentgrid, 'scene', None) is not None:
                self.overlay_color = grid_object.tile_color
                self.overlay = self.paint_overlay(batch=self.parentgrid.scene.batch_delegate.cell_batch)
            if hasattr(grid_object, 'passable'):
                self.passable = grid_object.passable
            
        
    def remove_object(self, grid_object):
        """Removes a GridObject from the cell. Updates the entry_object attribute. Also updates the grid array.
        """
        otype = f'{grid_object.object_type}s'
        if self.entry_object[f'{otype}'][grid_object.name] is not None:
            self.entry_object[f'{otype}'][grid_object.name] = None
            del self.entry_object[f'{otype}'][grid_object.name]
            self.parentgrid.dictObject[self.col_index][self.row_index] = self.entry_object
            if otype == 'structures':
                self.on_destruct()
                if hasattr(grid_object, 'tile_color') and getattr(self.parentgrid, 'scene', None) is not None:
                    self.overlay_color = None
                    self.overlay = self.paint_overlay(batch=self.parentgrid.scene.batch_delegate.cell_batch)
                if hasattr(grid_object, 'passable'):
                    self.passable = True

    def add_zone(self, zone):
        """Adds a GridZone to the cell. Updates the entry_zone attribute. Also updates the grid array.
        If the zone has a color attribute, it is applied to the overlay. The overlay can be painted using the
        paint_overlay method."""
        ztype = f'{zone.zone_type}s'
        if self.entry_zone[f'{ztype}'] is None:
            self.entry_zone[f'{ztype}'] = {}
        self.entry_zone[f'{ztype}'].update({zone.name: zone})
        zone._add_cell(self)
        if zone._color is not None:
           self.overlay_color = zone._color
        # self.paint.delete()
        # self.paint = None
        # self.overlay = self.paint_overlay(batch=self.parentgrid.scene.batch_delegate.cell_batch)

    def get_region(self):
        """Returns the region of the cell."""
        if self.entry_zone['regions'] is not None:
            return self.entry_zone['regions']
        
    def add_unit(self, unit):
        """Adds a GridUnit to the cell. Updates the entry_unit attribute. Also updates the grid array."""
        # if hasattr(unit, 'actor_type'):
        #     utype = f'{unit.actor_type}s'
        # elif hasattr(unit, 'parent'):
        #     utype = f'{unit.parent.actor_type}s'
        utype = 'players'
        if self.entry_unit[f'{utype}'] is None:
            self.entry_unit[f'{utype}'] = {}
        self.entry_unit[f'{utype}'].update({unit.name: unit})
        self.parentgrid.dictUnit[self.col_index][self.row_index] = self.entry_unit
        
        
    def remove_unit(self, unit):
        """Removes a GridUnit from the cell. Updates the entry_unit attribute. Also updates the grid array."""
        # utype = f'{unit.actor_type}s'
        utype = 'players'
        if self.entry_unit[f'{utype}'][unit.name] is not None:
            self.entry_unit[f'{utype}'][unit.name] = None
            del self.entry_unit[f'{utype}'][unit.name]
        if self.entry_unit[f'{utype}'] == {}:
            self.entry_unit[f'{utype}'] = None
        self.parentgrid.dictUnit[self.col_index][self.row_index][2] = self.entry_unit
            

                    
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

    def join_feature(self, feature_title, feature):
        self.entry_zone['features'][feature_title] = feature
        
    def leave_feature(self, feature_title):
        self.entry_zone['features'][feature_title].remove_cell(self)
        self.entry_zone['features'][feature_title] = None
        del self.entry_zone['features'][feature_title]        

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
        

    def init_array(self):
        self.array = self.parentgrid.grid_array[self.col_index, self.row_index]


    def refresh(self, dt):
        self.parentgrid.grid_array[self.file_index, self.rank_index] = self.array
        
    def _request_shape(self):
        """Requests the shape of the cell from the parent grid."""
        if not self.overlay_color:
            return self.x, self.y, self.size, self.size, self.terrain_color
        else:
            return self.x, self.y, self.size, self.size, self.overlay_color
        
    def __json__(self):
        return {
            "designation": self.designation,
            "coordinates": self.coordinates,
            "adjacent": self.adjacent,
            "groups": [group.__json__() for group in self.groups.values()]
        }