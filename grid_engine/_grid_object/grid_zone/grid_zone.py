import random
from grid_engine._utility import QuietDict as _QuietDict
from ..grid_object import *

class GridZone(BaseGridObject):
    """A grid object that occupies more than one cell. A good example of this on the world map, or overworld, would be
    a town or city, on the local map a tavern would be best represented with GridZone"""

    def __init__(self, grid: Any, name: AnyStr, zone_type: AnyStr, center_cell: object = None, color: tuple[int, int, int] = None, area_size: int = None):
        logger.log(77, f'Creating new GridZone object {name} of type {zone_type} at {center_cell.designation}')
        super(GridZone, self).__init__(grid, name, 'zone', center_cell.designation)
        self._zone_type = zone_type
        self._center_cell = center_cell   # relative to the center cell in (rank_index, file_index) format.
        self._color = color
        logger.log(77, f'Center cell rank, file is {self._center_cell.row_index, self._center_cell.col_index}')
        logger.log(77, f'Center cell coordinates are {self._center_cell.coordinates}')
        self._cells = _QuietDict()
        self._area = None
        self._expand_to_area(area_size)
#        self._adjust_area_shape()
        self.add_zone_to_cells()
        logger.log(77, f'GridZone {self.name} created at {self._center_cell.coordinates} with {len(self.cells)} cells')

    def _expand_to_area(self, area_size: int):
        """
        Expands the GridZone to the specified area size.
        """
        if not self._center_cell:
            return
        if not area_size:
            return
        if area_size == 1:
            return
        if area_size > 1:
            cell_set = self.grid.get_area(self._center_cell, area_size)
            self._cells.update({cell.designation: cell for cell in cell_set})

    def _adjust_area_shape(self):
        cell_items = list(self.cells.items.items())
        random.shuffle(cell_items)
        for cell_name, zone_cell in cell_items:
            uncell_ct = 0
            for adj_cell in zone_cell.adjacent:
                cell = self.grid[adj_cell]
                if cell not in self.cells:
                    uncell_ct += 1
            if uncell_ct >= 5 and random.random() > 0.7:
                del self.cells[zone_cell.designation]
                            
    def expand_to_landmass_edges(self):
        """
        Expands the GridZone to the edges of the landmass where the center cell is located.
        """
        if not self._center_cell:
            return  # Cannot expand without a center cell.

        land = self.grid.find_landmass_cells(self._center_cell)
        self._cells.update({cell.designation: cell for cell in land})
        self._area = len(self._cells)

    def add_zone_to_cells(self):
        for cell in self.cells:
            self.cells[cell].add_zone(self)

    @property
    def area(self) -> Optional[int]:
        return self._area

    @property
    def cells(self) -> Optional[list]:
        return self._cells
    
    @property
    def zone_type(self) -> Optional[AnyStr]:
        return self._zone_type
