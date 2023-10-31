from ..__log__ import log_method as _log_method

from typing import Optional, List, Tuple, Dict, Any
import itertools
import numpy as np


@_log_method
def generate_row_strings(row_count: int) -> List[str]:
    """
    Generate a list of strings representing rows.

    This function generates a list of strings representing rows. The number of rows to generate is specified by the `row_count` parameter.

    Args:
        row_count (int): The number of rows to generate.

    Returns:
        List[str]: A list of strings representing the generated rows.

    Example:
        ```python
        row_strings = generate_row_strings(10)
        print(row_strings)
        # Output: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        ```
    """
    rows = [chr(i + 97) for i in range(26)]
    rows.extend(chr(i + 65) for i in range(26))
    rows.extend(
        chr(i + 97) + chr(j + 97)
        for i, j in itertools.product(range(26), range(26))
    )
    rows.extend(
        chr(i + 65) + chr(j + 97)
        for i, j in itertools.product(range(1, 26), range(26))
    )
    rows.extend(
        chr(i + 97) + chr(j + 97) + chr(k + 97)
        for i, j, k in itertools.product(range(26), range(26), range(26))
    )
    return rows[:row_count]

@_log_method
def generate_column_strings(col_count: int) -> List[str]:
    """
    Generate a list of strings representing columns.

    This function generates a list of strings representing columns. The number of columns to generate is specified by the `col_count` parameter. Each column is represented by a string that is zero-padded to a width of 5 characters.

    Args:
        col_count (int): The number of columns to generate.

    Returns:
        List[str]: A list of strings representing the generated columns.

    Example:
        ```python
        column_strings = generate_column_strings(5)
        print(column_strings)
        # Output: ['00001', '00002', '00003', '00004', '00005']
        ```
    """
    cols = [str(r + 1) for r in range(col_count)][::-1]
    for i in range(col_count):
        cols[i] = cols[i].zfill(5)
    cols.reverse()
    return cols

@_log_method
def get_row_strings(row_count: Optional[int] = None) -> List[str]:
    if row_count is None or row_count < 1:
        raise ValueError("row_count must be an integer > 1")
    return generate_row_strings(row_count)

@_log_method
def get_column_strings(col_count: Optional[int] = None) -> List[str]:
    if col_count is None or col_count < 1:
        raise ValueError("col_count must be an integer > 1")
    return generate_column_strings(col_count)

@_log_method
def generate_cell_strings(row_strings: List[str], col_strings: List[str]) -> List[str]:
    """
    Generate a list of strings representing cells.

    This function generates a list of strings representing cells by combining each row string from `row_strings` with each column string from `col_strings`. The resulting list contains all possible combinations of row and column strings.

    Args:
        row_strings (List[str]): A list of strings representing rows.
        col_strings (List[str]): A list of strings representing columns.

    Returns:
        List[str]: A list of strings representing the generated cells.

    Example:
        ```python
        row_strings = ['a', 'b', 'c']
        col_strings = ['1', '2', '3']
        cell_strings = generate_cell_strings(row_strings, col_strings)
        print(cell_strings)
        # Output: ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
        ```
    """
    return [r + f for r, f in itertools.product(row_strings, col_strings)]

@_log_method
def get_cell_strings(row_strings: List[str], col_strings: List[str]) -> List[str]:
    return generate_cell_strings(row_strings, col_strings)

@_log_method
def get_cell_coordinates(cell_size: int, row_count: int, col_count: int) -> List[Tuple[int, int]]:
    """
    Get the coordinates of each cell in a grid.

    This function calculates the coordinates of each cell in a grid based on the provided `cell_size`, `row_count`, and `col_count` parameters. The coordinates are returned as a list of tuples, where each tuple represents the x and y coordinates of a cell.

    Args:
        cell_size (int): The size of each cell in the grid.
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.

    Returns:
        List[Tuple[int, int]]: A list of tuples representing the coordinates of each cell.

    Example:
        ```python
        cell_coordinates = get_cell_coordinates(10, 3, 4)
        print(cell_coordinates)
        # Output: [(0, 0), (10, 0), (20, 0), (30, 0), (0, 10), (10, 10), (20, 10), (30, 10), (0, 20), (10, 20), (20, 20), (30, 20)]
        ```
    """
    return [
        (
            abs(0 - ((num % col_count) * cell_size)),
            abs(0 - ((num // col_count) * cell_size)),
       )
        for num in range(row_count*col_count)
    ]

@_log_method
def get_grid_dict(cell_strings: List[str], row_strings: List[str], col_strings: List[str], cell_coordinates: List[Tuple[int, int]]) -> Dict[str, Any]:
    """
    Get a dictionary representing a grid.

    This function creates a dictionary representing a grid based on the provided `cell_strings`, `row_strings`, `col_strings`, and `cell_coordinates`. Each cell in the grid is represented by a key-value pair in the dictionary, where the key is the cell string and the value is a dictionary containing various properties of the cell.

    Args:
        cell_strings (List[str]): A list of strings representing cells.
        row_strings (List[str]): A list of strings representing rows.
        col_strings (List[str]): A list of strings representing columns.
        cell_coordinates (List[Tuple[int, int]]): A list of tuples representing the coordinates of each cell.

    Returns:
        Dict[str, Any]: A dictionary representing the grid.

    Example:
        ```python
        cell_strings = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3']
        row_strings = ['a', 'b']
        col_strings = ['1', '2', '3']
        cell_coordinates = [(0, 0), (10, 0), (20, 0), (0, 10), (10, 10), (20, 10)]
        grid_dict = get_grid_dict(cell_strings, row_strings, col_strings, cell_coordinates)
        print(grid_dict)
        # Output: {
        #     'a1': {'designation': 'a1', 'cell_index': 0, 'row_index': 0, 'col_index': 0, 'coordinates': (0, 0), 'quadrant_index': None, 'adjacent': []},
        #     'a2': {'designation': 'a2', 'cell_index': 1, 'row_index': 0, 'col_index': 1, 'coordinates': (10, 0), 'quadrant_index': None, 'adjacent': []},
        #     'a3': {'designation': 'a3', 'cell_index': 2, 'row_index': 0, 'col_index': 2, 'coordinates': (20, 0), 'quadrant_index': None, 'adjacent': []},
        #     'b1': {'designation': 'b1', 'cell_index': 3, 'row_index': 1, 'col_index': 0, 'coordinates': (0, 10), 'quadrant_index': None, 'adjacent': []},
        #     'b2': {'designation': 'b2', 'cell_index': 4, 'row_index': 1, 'col_index': 1, 'coordinates': (10, 10), 'quadrant_index': None, 'adjacent': []},
        #     'b3': {'designation': 'b3', 'cell_index': 5, 'row_index': 1, 'col_index': 2, 'coordinates': (20, 10), 'quadrant_index': None, 'adjacent': []}
        # }
        ```
    """

    return {
        cell: {
            "designation": cell,
            "cell_index": i,
            "row_index": row_strings.index(cell[:-5]),
            "col_index": col_strings.index(cell[-5:]),
            "coordinates": cell_coordinates[i],
            "quadrant_index": None,
            "adjacent": []
        } for i, cell in enumerate(cell_strings)
    }
    
@_log_method
def generate_quadrant_coordinates(row_count: int, col_count: int) -> List[List[Tuple[int, int]]]:
    """
    Get the coordinates of each quadrant in a grid.

    This function calculates the coordinates of each quadrant in a grid based on the provided `row_count` and `col_count` parameters. The grid is divided into four quadrants, and the coordinates of each quadrant are returned as a list of lists, where each inner list represents the coordinates of a quadrant.

    Args:
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.

    Returns:
        List[List[Tuple[int, int]]]: A list of lists representing the coordinates of each quadrant.

    Example:
        ```python
        quadrant_coordinates = get_quadrant_coordinates(4, 6)
        print(quadrant_coordinates)
        # Output: [
        #     [(0, 0), (3, 0), (3, 2), (0, 2)],
        #     [(3, 0), (6, 0), (6, 2), (3, 2)],
        #     [(0, 2), (3, 2), (3, 4), (0, 4)],
        #     [(3, 2), (6, 2), (6, 4), (3, 4)]
        # ]
        ```
    """

    quad_x = [0, col_count//2, col_count, col_count//2]
    quad_y = [0, row_count//2, row_count, row_count//2]
    return [
        [
            (quad_x[i], quad_y[j])[::-1],
            (quad_x[i+1], quad_y[j])[::-1],
            (quad_x[i+1], quad_y[j+1])[::-1],
            (quad_x[i], quad_y[j+1])[::-1]
        ]
        for i, j in itertools.product(range(2), range(2))
    ]
    
@_log_method
def get_quadrant_indices(quadrant_coords: List[List[Tuple[int,int]]], grid_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assign quadrant indices to cells in a grid.

    This function assigns quadrant indices to cells in a grid based on the provided `quadrant_coords` and `grid_dict`. Each cell in the grid is checked against the coordinates of each quadrant, and if the cell falls within a quadrant, its `quadrant_index` property in the `grid_dict` is updated accordingly.

    Args:
        quadrant_coords (List[List[Tuple[int, int]]]): A list of lists representing the coordinates of each quadrant.
        grid_dict (Dict[str, Any]): A dictionary representing the grid.

    Returns:
        Dict[str, Any]: A dictionary representing the updated grid with assigned quadrant indices.

    Example:
        ```python
        updated_grid_dict = get_quadrant_indices(quadrant_coordinates, grid_dict)
        ```
    """

    for i, quad in enumerate(quadrant_coords):
        for cell in grid_dict:
            if (
                quad[0][0] <= grid_dict[cell]['col_index'] < quad[2][0] 
                and 
                quad[0][1] <= grid_dict[cell]['row_index'] < quad[1][1]
            ):
                grid_dict[cell]['quadrant_index'] = i
    return grid_dict

@_log_method
def generate_adjacency(grid_dict: Dict[str, any], row_count: int, col_count: int) -> Dict[str, Any]:
    """
    Assign adjacent cells to each cell in a grid.

    This function assigns adjacent cells to each cell in a grid based on the provided `grid_dict`, `row_count`, and `col_count`. The adjacency is determined based on the position of each cell within the grid. The adjacent cells are stored as a list in the `adjacent` property of each cell in the `grid_dict`.

    Args:
        grid_dict (Dict[str, Any]): A dictionary representing the grid.
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.

    Returns:
        Dict[str, Any]: A dictionary representing the updated grid with assigned adjacent cells.

    Example:
        ```python
        updated_grid_dict = get_adjacency(grid_dict, row_count, col_count)
        ```
    """

    cell_list = list(grid_dict.keys())
    w = col_count
    h = row_count
    for cell, information in grid_dict.items():
        n = information['cell_index']
        r = grid_dict[cell]['row_index']
        f = grid_dict[cell]['col_index']
        if r not in [0, row_count - 1] and f not in [0, col_count - 1]:
            grid_dict[cell]['adjacent'] = [cell_list[n - (w + 1)], cell_list[n - w],
                                            cell_list[n - (w - 1)],
                                            cell_list[n + 1],
                                            cell_list[n + (w + 1)], cell_list[n + w],
                                            cell_list[n + (w - 1)],
                                            cell_list[n - 1]]
        elif r == 0:
            if f == 0:
                grid_dict[cell]['adjacent'] = [cell_list[1], cell_list[w + 1],
                                                cell_list[w]]
            elif f == col_count - 1:
                grid_dict[cell]['adjacent'] = [cell_list[n + w], cell_list[n + (w - 1)],
                                                cell_list[n - 1]]
            else:
                grid_dict[cell]['adjacent'] = [cell_list[n + 1], cell_list[n + (w + 1)],
                                                cell_list[n + w],
                                                cell_list[n + (w - 1)],
                                                cell_list[n - 1]]
        elif r == row_count - 1:
            if f == 0:
                grid_dict[cell]['adjacent'] = [cell_list[n - w], cell_list[n - (w - 1)],
                                                cell_list[n + 1]]
            elif f == col_count - 1:
                grid_dict[cell]['adjacent'] = [cell_list[n - (w + 1)], cell_list[n - w],
                                                cell_list[n - 1]]
            else:
                grid_dict[cell]['adjacent'] = [cell_list[n - (w + 1)], cell_list[n - w],
                                                cell_list[n - (w - 1)],
                                                cell_list[n + 1],
                                                cell_list[n - 1]]
        elif f == 0:
            grid_dict[cell]['adjacent'] = [cell_list[n - w], cell_list[n - (w - 1)],
                                            cell_list[n + 1],
                                            cell_list[n + (w + 1)],
                                            cell_list[n + w]]
        elif f == col_count - 1:
            grid_dict[cell]['adjacent'] = [cell_list[n - (w + 1)], cell_list[n - w],
                                            cell_list[n + w],
                                            cell_list[n + (w - 1)],
                                            cell_list[n - 1]]
    return grid_dict


def get_graph(grid_dict: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Get a graph representation of the grid.

    This function creates a graph representation of the grid based on the provided `grid_dict`. Each cell in the grid is treated as a node in the graph, and the adjacent cells are treated as edges connecting the nodes. The graph is returned as a dictionary, where the keys are the cells and the values are lists of adjacent cells.

    Args:
        grid_dict (Dict[str, Any]): A dictionary representing the grid.

    Returns:
        Dict[str, List[str]]: A dictionary representing the graph.

    Example:
        ```python
        graph = get_graph(grid_dict)
        ```
    """

    return {
        cell: list(info['adjacent'])
        for cell, info in grid_dict.items()
    }

@_log_method    
def process_grid(row_count: int, col_count: int, cell_size: int) -> Dict[str, Any]:
    """
    Process a grid.

    This function processes a grid based on the provided `row_count`, `col_count`, and `cell_size`. It performs the following steps:
    1. Generates row strings.
    2. Generates column strings.
    3. Generates cell strings.
    4. Calculates cell coordinates.
    5. Creates a grid dictionary.
    6. Calculates quadrant coordinates.
    7. Assigns quadrant indices to cells.
    8. Assigns adjacent cells to each cell.
    9. Creates a graph representation of the grid.

    Args:
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.
        cell_size (int): The size of each cell in the grid.

    Returns:
        Dict[str, Any]: A dictionary containing the processed grid data, including row strings, column strings, cell strings, cell coordinates, grid dictionary, quadrant coordinates, and graph representation.

    Example:
        ```python
        row_count = 4
        col_count = 6
        cell_size = 10
        processed_grid = process_grid(row_count, col_count, cell_size)
        print(processed_grid)
        # Output: {
        #     "cell_size": 10,
        #     "row_strings": ["A", "B", "C", "D"],
        #     "col_strings": ["1", "2", "3", "4", "5", "6"],
        #     "cell_strings": [
        #         "A1", "A2", "A3", "A4", "A5", "A6",
        #         "B1", "B2", "B3", "B4", "B5", "B6",
        #         "C1", "C2", "C3", "C4", "C5", "C6",
        #         "D1", "D2", "D3", "D4", "D5", "D6"
        #     ],
        #     "cell_coordinates": [
        #         (0, 0), (10, 0), (20, 0), (30, 0), (40, 0), (50, 0),
        #         (0, 10), (10, 10), (20, 10), (30, 10), (40, 10), (50, 10),
        #         (0, 20), (10, 20), (20, 20), (30, 20), (40, 20), (50, 20),
        #         (0, 30), (10, 30), (20, 30), (30, 30), (40, 30), (50, 30)
        #     ],
        #     "grid_dict": {
        #         "A1": {"designation": "A1", "cell_index": 0, "row_index": 0, "col_index": 0, "coordinates": (0, 0), "quadrant_index": 0, "adjacent": [...]},
        #         ...
        #     },
        #     "quadrant_coords": [
        #         [(0, 0), (15, 0), (15, 20), (0, 20)],
        #         ...
        #     ],
        #     "graph": {
        #         "A1": ["A2", "B2", "B1"],
        #         ...
        #     }
        # }
        ```
    """

    row_strings = get_row_strings(row_count)
    col_strings = get_column_strings(col_count)
    cell_strings = get_cell_strings(row_strings, col_strings)
    cell_coordinates = get_cell_coordinates(cell_size, row_count, col_count)
    grid_dict = get_grid_dict(cell_strings, row_strings, col_strings, cell_coordinates)
    quadrant_coords = generate_quadrant_coordinates(row_count, col_count)
    grid_dict = get_quadrant_indices(quadrant_coords, grid_dict)
    grid_dict = generate_adjacency(grid_dict, row_count, col_count)
    graph = get_graph(grid_dict)
    return {
        "cell_size": cell_size,
        "row_strings": row_strings,
        "col_strings": col_strings,
        "cell_strings": cell_strings,
        "cell_coordinates": cell_coordinates,
        "grid_dict": grid_dict,
        "quadrant_coords": quadrant_coords,
        "graph": graph
    }