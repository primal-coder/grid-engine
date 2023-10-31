from abc import ABC as _ABC
from typing import Union as _Union, Optional as _Optional


class Grid:
    pass


class Cell:
    pass


class GridGroup(_ABC):
    """
    A class to represent a group of cells on the grid.
    """

    def __init__(self, grid: Grid, title: str, cells: list, legacy: bool = False):
        self.grid = grid
        self.title = title
        self.cells = [grid.cells[cell] for cell in cells]
        self.legacy = legacy
        self.initiate_group()

    def initiate_group(self):
        """Adds the group to the cells in the group."""
        for cell in self.cells:
            cell.join_group(self.title, self)

    def add_cell(self, cell):
        """Adds a cell to the group and adds the group to the cell."""

        self.cells.append(cell)
        cell.join_group(self.title, self)

    def in_group(self, cell: _Union[str, Cell]):
        """Checks if a cell is in the group"""
        if isinstance(cell, str):
            cell = self.grid.cells[cell]
        cell_designations = [cell.designation for cell in self.cells]
        if (
            isinstance(cell, str)
            and cell in cell_designations
            or not isinstance(cell, str)
            and isinstance(cell, Cell)
            and cell in self.cells
        ):
            return True

        elif isinstance(cell, (str, Cell)):
            return False
            
    def remove_cell(self, cell):
        """Removes a cell from the group"""
        if self.in_group(cell):
            self.cells.remove(cell)
        else:
            return False

    def __json__(self):
        """
        Serializes the GridGroup object as a JSON object.
        """
        
        cells_designations = [cell.designation for cell in self.cells]
        return {
            "title": self.title,
            "cells": cells_designations,
            "legacy": self.legacy
        }


class GridNeighborhood:
    """A class to represent a neighborhood of cells.

    Args:
        grid (Grid): The grid object to which the neighborhood belongs.
        focus (Cell): The cell object that is the focus of the neighborhood.

    Attributes:
        grid (Grid): The grid object to which the neighborhood belongs.
        focus (Cell): The cell object that is the focus of the neighborhood.
        cell_addresses (list): A list of cell objects that are the addresses of the neighborhood.
        neighbors (list): A list of objects that are the occupants of the cells in the neighborhood
    """

    def __init__(self,
                 grid: _Optional[Grid] = None,
                 focus: _Optional[_Union[Cell, str]] = None,
                 radius: _Optional[int] = None,
            ):
        self.grid = grid
        self.focus = focus
        self.radius = radius if radius is not None else 1
        self.neighbors = None
        self.cell_addresses = self.get_cell_addresses()
        
    def __call__(self):
        return self.cell_addresses

    def get_cell_addresses(self):
        addresses = [self.grid.cells[address] for address in self.focus.adjacent]
        if self.radius == 1:
            return addresses
        for _ in range(self.radius):
            level = []
            for address in addresses:
                extension = [self.grid.cells[adj] for adj in address.adjacent if self.grid.cells[adj] not in addresses]
                level.extend(extension)
            level = set(level)
            level = list(level)
            addresses.extend(level)
        return addresses

    def update(self):
        self.neighbors = [address.occupant for address in self.cell_addresses if address.occupied]
