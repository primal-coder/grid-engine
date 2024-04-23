from uuid import uuid4

class _AbstractRoom:
    _grid_blueprint = None
    _room_id = None
    _room_name = None
    _room_type = None
    _room_dimensions = None
    _room_position = None
    _room_doors = None
    _room_cells = None
    _room_cell_data = None
    
    @property
    def grid_blueprint(self):
        return self._grid_blueprint
    
    @property
    def room_id(self):
        return self._room_id
    
    @room_id.setter
    def room_id(self, value):
        self._room_id = value
        
    @property
    def room_name(self):
        return self._room_name
    
    @room_name.setter
    def room_name(self, value):
        self._room_name = value
        
    @property
    def room_type(self):
        return self._room_type
    
    @room_type.setter
    def room_type(self, value):
        self._room_type = value
        
    @property
    def room_dimensions(self):
        return self._room_dimensions
    
    @room_dimensions.setter
    def room_dimensions(self, value):
        self._room_dimensions = value
        
    @property
    def room_position(self):
        return self._room_position
    
    @room_position.setter
    def room_position(self, value):
        self._room_position = value
        
    @property
    def room_doors(self):
        return self._room_doors
    
    @room_doors.setter
    def room_doors(self, value):
        self._room_doors = value
        
    @property
    def room_cells(self):
        return self._room_cells
    
    @room_cells.setter
    def room_cells(self, value):
        self._room_cells = value
        
    @property
    def room_cell_data(self):
        return self._room_cell_data
    
    @room_cell_data.setter
    def room_cell_data(self, value):
        self._room_cell_data = value
        
class BaseRoom(_AbstractRoom):
    def __init__(
        self, 
        grid_blueprint, 
        room_position: tuple[int, int], 
        room_dimensions: tuple[int, int], 
        room_id: str = None, 
        room_name: str = None, 
        room_type: str = None, 
        room_doors: list[tuple[int, int]] = None, 
        room_cells: list[tuple[int, int]] = None, 
        room_cell_data: list[tuple[int, int]] = None
    ):
        self.grid_blueprint = grid_blueprint
        self.room_position = room_position
        self.room_dimensions = room_dimensions
        self.room_id = room_id if room_id else uuid4().hex
        self.room_name = room_name if room_name else f"Room {self.room_id[-4:]}"
        self.room_type = room_type if room_type else "Generic"
        self.room_doors = room_doors
        self.room_cells = room_cells
        self.room_cell_data = room_cell_data
        
class 