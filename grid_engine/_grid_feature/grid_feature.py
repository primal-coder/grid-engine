from __future__ import annotations
from abc import ABCMeta, ABC, abstractmethod
from grid_engine._utility import QuietDict

from typing import Optional, List, Tuple, Any, Union, AnyStr

class Grid(ABC):
    pass

class Cell(ABC):
    pass

class AbstractGridFeature(QuietDict, ABC):
    def __init__(self, grid: Grid, cells: List[Cell], title: str):
        self.grid = grid
        self.cells = cells
        self.title = title
        self.initiate_feature()

    def initiate_feature(self):
        for cell in self.cells:
            cell.join_feature(self.title, self)

    def add_cell(self, cell: Cell):
        self.cells.append(cell)
        cell.join_feature(self.title, self)

    def remove_cell(self, cell: Cell):
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            return False

    def in_feature(self, cell: Cell):
        return cell in self.cells

    def __json__(self):
        cells_designations = [cell.designation for cell in self.cells]
        return {
            "title": self.title,
            "cells": cells_designations,
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.title})"

    def __eq__(self, other):
        if isinstance(other, AbstractGridFeature):
            return self.title == other.title
        else:
            return False

    def __hash__(self):
        return hash(self.title)

    def __sub__(self, other):
        if isinstance(other, AbstractGridFeature):
            for cell in self.cells.copy():
                if cell in other.cells:
                    self.remove_cell(cell)

    def __add__(self, other):
        if isinstance(other, AbstractGridFeature):
            for cell in other.cells:
                self.add_cell(cell)

    def __len__(self):
        return len(self.cells)

    def __iter__(self):
        return iter(self.cells)

    def __getitem__(self, key):
        return self.cells[key]

    def __setitem__(self, key, value):
        self.cells[key] = value

    def __delitem__(self, key):
        del self.cells[key]

    def __contains__(self, item):
        return item in self.cells

    def __reversed__(self):
        return reversed(self.cells)

    def __copy__(self):
        return self.__class__(self.grid, self.cells.copy(), self.title)

    def __deepcopy__(self, memo):
        return