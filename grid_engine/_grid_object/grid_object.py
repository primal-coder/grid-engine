from grid_engine._cell import Cell
from abc import ABC
from typing import Optional, Any, AnyStr, Union
from uuid import uuid4


class _AbstractGridObject(ABC):
    _object_id = None
    _name = None
    _grid = None
    _cell = None
    _object_type = None   

    @property
    def object_id(self) -> Optional[int]:
        return self._object_id
    
    @property
    def name(self) -> Optional[AnyStr]:
        return self._name
    
    @name.setter
    def name(self, name: AnyStr):
        self._name = name
        
    @property
    def grid(self) -> Optional[Any]:
        return self._grid

    @property
    def cell(self) -> type(Cell):
        return self._cell
    
    @cell.setter
    def cell(self, cell: Any):
        if cell is not None:
            self._cell = cell
        elif self._cell is not None:
            self._cell = None
                
    @property
    def object_type(self) -> Optional[AnyStr]:
        return self._object_type
    
    @property
    def cell_name(self) -> Optional[AnyStr]:
        if self.cell is not None:
            return self.cell.designation
            
    @property
    def position(self) -> Optional[Any]:
        if self.cell is not None:
            return self.cell.coordinates
    
    @property
    def x(self) -> Optional[int]:
        if self.cell is not None:
            return self.cell.coordinates[0]
    
    @property
    def y(self) -> Optional[int]:
        if self.cell is not None:
            return self.cell.coordinates[1]
    
    
class _BaseGridObject(_AbstractGridObject):
    def __init__(self, grid: Any, name: AnyStr, object_type: AnyStr, cell: Union[AnyStr, type(Cell)] = None):
        super(_BaseGridObject, self).__init__()
        self._object_id = uuid4().hex[-4:]
        self.name = name
        self._grid = grid
        self._object_type = object_type
        init_cell = self.grid.random_cell(attr=('passable', True)) if cell is None else cell
        init_cell = self.grid[cell] if isinstance(cell, str) else init_cell
        self.cell = init_cell


class GridObject(_BaseGridObject):
    def __init__(self, grid: Any, name: AnyStr, object_type: AnyStr, cell: Union[AnyStr, type(Cell)]  = None):
        super(GridObject, self).__init__(grid, name, object_type, cell)