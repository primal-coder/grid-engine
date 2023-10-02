from abc import ABC
from typing import Union as _Union

class Grid:
    pass

class Cell:
    pass

class GridGroup(ABC):
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
        cell_designations = [cell.designation for _ in self.cells]
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