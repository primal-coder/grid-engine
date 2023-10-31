from ..grid_object import *


_STRUCTURE_DICT = {}

class GridStructure(GridObject):
    @staticmethod
    def create(grid: Any, name: AnyStr, cell: Any):
        if name in _STRUCTURE_DICT.keys():
            structure_attrs = _STRUCTURE_DICT[name]
            return GridStructure(grid, name, cell, **structure_attrs)
        

    def __init__(
        self, 
        grid: Any, 
        name: AnyStr, 
        cell: AnyStr = None, 
        construction_material: AnyStr = None, 
        construction_cost: int = None, 
        maximum_integrity: int = None, 
        tile_color: tuple[int, int, int] = None,
        passable: bool = False
    ):
        super(GridStructure, self).__init__(grid, name, 'structure', cell)
        self._under_construction = False
        self._construction_progress = 0
        self._construction_material = construction_material
        self._construction_cost = construction_cost
        self._constructed_by = None
        self._maximum_integrity = maximum_integrity
        self._integrity = 1.0
        self._siblings = None
        self._parent = None
        self._children = None
        self._stations = None
        self._portal = False
        self._tile_color = tile_color
        self._passable = passable
        
    @property
    def under_construction(self) -> Optional[bool]:
        return self._under_construction
    
    @property
    def construction_progress(self) -> Optional[int]:
        return self._construction_progress
    
    @property
    def construction_material(self) -> Optional[AnyStr]:
        return self._construction_material
    
    @property
    def construction_cost(self) -> Optional[int]:
        return self._construction_cost

    @property
    def integrity(self) -> Optional[int]:
        return self._maximum_integrity * self._integrity
        
    @property
    def tile_color(self):
        return self._tile_color
    
    def _recv_damage(self, damage: int):
        self._integrity -= damage / self._maximum_integrity
        if self._integrity <= 0:
            self._integrity = 0
            self._destroy()
            
    def _destroy(self):
        self.cell.passable = True
        self.cell.remove_object(self)
