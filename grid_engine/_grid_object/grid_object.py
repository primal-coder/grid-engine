from abc import ABC
from typing import Optional, Any, AnyStr
from uuid import uuid4

class AbstractGridObject(ABC):
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
    def cell(self) -> Optional[Any]:
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
        return self.cell.coordinates
    
    @property
    def x(self) -> Optional[int]:
        return self.cell.coordinates[0]
    
    @property
    def y(self) -> Optional[int]:
        return self.cell.coordinates[1]
    
    
class BaseGridObject(AbstractGridObject):
    def __init__(self, grid: Any, name: AnyStr, object_type: AnyStr, cell: AnyStr = None):
        super(BaseGridObject, self).__init__()
        self._object_id = uuid4().hex[-4:]
        self.name = name
        self._grid = grid
        self._object_type = object_type
        init_cell = self.grid.random_cell(attr=('passable', True)) if cell is None else cell
        self.cell = init_cell


class GridObject(BaseGridObject):
    def __init__(self, grid: Any, name: AnyStr, object_type: AnyStr, cell: AnyStr = None):
        super(GridObject, self).__init__(grid, name, object_type, cell)
        self._object_type = object_type