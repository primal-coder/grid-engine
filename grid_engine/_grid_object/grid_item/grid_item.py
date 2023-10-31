import pyglet
from typing import Any, AnyStr, Optional
from ..grid_object import GridObject

class GridItem(GridObject):
    _picked_up_at = None
    _picked_up_by = None
    _dropped_at = None
    _dropped_by = None
    def __init__(self, grid: Any, name: AnyStr, cell: AnyStr = None, img_path: AnyStr = None):
        super(GridItem, self).__init__(grid, name, 'item', cell)
        if cell is not None:
            cell.add_object(self)
        if img_path is not None:
            self.img = pyglet.image.load(img_path)
            self.sprite = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y, batch=self.grid.grid_batch)
            self.sprite.scale = self.grid.cell_size / self.sprite.width
            
        
    @property
    def cell(self) -> Optional[Any]:
        return self._cell
    
    @cell.setter
    def cell(self, cell: Any):
        if cell is not None:
            self._cell = cell
            if self.picked_up_at is not None:       # meaning the object until this point was held by a
                self._dropped_at = self._cell.designation       # character and is thus being dropped
                self._picked_up_at = None
        elif self._cell is not None:        # the setting value is None and the current value isn't 
            self._picked_up_at = self._cell.designation     # thus the object is being picked up by a character

    @property
    def picked_up_at(self) -> Optional[Any]:
        return self._picked_up_at
    
    @property
    def dropped_at(self) -> Optional[Any]:
        return self._dropped_at
    
    @property
    def picked_up_by(self) -> Optional[Any]:
        return self._picked_up_by
    
    @property
    def dropped_by(self) -> Optional[Any]:
        return self._dropped_by
