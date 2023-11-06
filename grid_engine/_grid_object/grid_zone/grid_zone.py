import random
from typing import Any, AnyStr, Union, Optional
from grid_engine._utility import QuietDict as _QuietDict
from grid_engine._cell import Cell
from ..grid_object import _BaseGridObject

class GridZone(_BaseGridObject):
    _zone_type = None
    _center_cell = None
    _color = None
    _area = None
    _cells = None
    
    @property
    def area(self) -> Optional[int]:
        """The area of the GridZone. Equal to the length of the GridZone.cells attribute."""
        return self._area

    @property
    def cells(self) -> Optional[list[Cell, ]]:
        return self._cells
    
    @property
    def zone_type(self) -> Optional[AnyStr]:
        return self._zone_type
    
    @property
    def center_cell(self) -> Optional[Any]:
        return self._center_cell
    
    """A grid object that occupies more than one cell. A good example of this on the world map, or overworld, would be
    a town or city, on the local map a tavern would be best represented with GridZone"""

    def __init__(self, grid: Any, name: AnyStr, zone_type: AnyStr, center_cell: Union[AnyStr, type(Cell)] = None, color: tuple[int, int, int] = None):
        #logger.log(77, f'Creating new GridZone object {name} of type {zone_type} at {center_cell.designation}')
        super(GridZone, self).__init__(grid, name, 'zone', center_cell)
        self._zone_type = zone_type
        self._center_cell = self.cell  # relative to the center cell in (rank_index, file_index) format.
        self._color = color
        #logger.log(77, f'Center cell rank, file is {self._center_cell.row_index, self._center_cell.col_index}')
        #logger.log(77, f'Center cell coordinates are {self._center_cell.coordinates}')
        self._cells = _QuietDict()
        self._area = None
        #logger.log(77, f'GridZone {self.name} created at {self._center_cell.coordinates} with {len(self.cells)} cells')

    def _add_cell(self, cell: type(Cell)):
        """
        Adds a cell to the GridZone.
        """
        self._cells[cell.designation] = cell
        self._area = len(self._cells)
        self._add_zone_to_cells()
        
    def _remove_cell(self, cell: type(Cell)):
        """
        Removes a cell from the GridZone.
        """
        self._cells.pop(cell.designation)
        self._area = len(self._cells)
        self._add_zone_to_cells()
        
    def _add_cells(self, cells: list[type(Cell)]):
        """
        Adds a list of cells to the GridZone.
        """
        for cell in cells:
            self._cells[cell.designation] = cell
        self._area = len(self._cells)
        self._add_zone_to_cells()
        
    def _expand_to_area(self, area_radius: int):
        """
        Expands the GridZone to the specified area size.
        """
        if not self._center_cell:
            return
        if not area_radius:
            return
        if area_radius == 1:
            return
        if area_radius > 1:
            cell_set = self.grid.get_area(self.center_cell, area_radius)
            self._cells.update({cell.designation: cell for cell in cell_set})
            self._area = len(self._cells)
        self._add_zone_to_cells()

    def _add_zone_to_cells(self):
        for cell in self.cells:
            if self.cells[cell].entry_zones[f'{self.zone_type}s'].get(self.name) is None:
                self.cells[cell].add_zone(self) 


class GridRegion(GridZone):
    """A subclass of GridZone that represents a region of landmass on the world map."""
    def __init__(self, grid: Any, name: AnyStr, center_cell: Union[AnyStr, type(Cell)] = None, color: tuple[int, int, int] = None):
        super(GridRegion, self).__init__(grid, name, 'region', center_cell, color)
        self._cells = _QuietDict()
        self._area = None
        self._expand_to_landmass_edges()
        self._add_zone_to_cells()
        #logger.log(77, f'GridRegion {self.name} created at {self._center_cell.coordinates} with {len(self.cells)} cells')
                   
    def _expand_to_landmass_edges(self):
        """
        Expands the GridRegion to the edges of the landmass where the center cell is located.
        """
        if not self._center_cell:
            return  # Cannot expand without a center cell.

        land = self.grid.find_landmass_cells(self._center_cell)
        self._cells.update({cell.designation: cell for cell in land})
        self._area = len(self._cells)
        
class GridArea(GridZone):
    """A subclass of GridZone which may be used to represent any given area on the grid."""
    def __init__(self, grid: Any, name: AnyStr, center_cell: Union[AnyStr, type(Cell)] = None, color: tuple[int, int, int] = None, area_radius: int = 1):
        super(GridArea, self).__init__(grid, name, 'area', center_cell, color)
        self._cells = _QuietDict()
        self._area = None
        self._expand_to_area(area_radius)
        self._add_zone_to_cells()
        #logger.log(77, f'GridArea {self.name} created at {self._center_cell.coordinates} with {len(self.cells)} cells')