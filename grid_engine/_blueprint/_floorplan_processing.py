import numpy as np
import networkx as nx

MIN_ROOM_WIDTH = 0.1
MIN_ROOM_HEIGHT = 0.1
MAX_ROOM_WIDTH = 0.6
MAX_ROOM_HEIGHT = 0.3
MIN_ROOM_COUNT = 0.5
MAX_ROOM_COUNT = 0.75
MAX_ROOM_AREA = 0.5
MIN_ROOM_HALL_COUNT = 1
MAX_ROOM_HALL_COUNT = 5

def initialize_grid(row_count, col_count):
    return np.zeros((row_count, col_count))

def does_intersect(room_a, room_b):
    return not (room_a[0] + room_a[2] + 3 < room_b[0] or room_a[0] > room_b[0] + room_b[2] + 3 or room_a[1] + room_a[3] + 3 < room_b[1] or room_a[1] > room_b[1] + room_b[3] + 3)

def gen_count(dimensions, cell_size):                           # gen_count((100, 100), 1)
    x_min = int((dimensions[0] // cell_size) * MIN_ROOM_COUNT)  # x_min = 50
    y_min = int((dimensions[1] // cell_size) * MIN_ROOM_COUNT)  # y_min = 50
    size_factor = int((dimensions[0] * MIN_ROOM_WIDTH))         # size_factor = 10
    if x_min > y_min:                                           # if 50 > 50:
        min_count = (x_min + (x_min - y_min))    #   min_count = 50 + (50 - 50) // 10 ~ 5
    else:                                                       # else:  
        min_count = (y_min + (y_min - x_min))    #   min_count = 50 + (50 - 50) // 10 ~ 5
    x_max = int((dimensions[0] // cell_size) * MAX_ROOM_COUNT)  # x_max = 70
    y_max = int((dimensions[1] // cell_size) * MAX_ROOM_COUNT)  # y_max = 70
    if x_max > y_max:                                           # if 70 > 70:     
        max_count = x_max + (x_max - y_max)      #   max_count = 70 + (70 - 70) // 10 ~ 7
    else:                                                       # else:        
        max_count = y_max + (y_max - x_max)      #   max_count = 70 + (70 - 70) // 10 ~ 7
    return np.random.randint(min_count, max_count) // 10              # return random.randint(5, 7)

def gen_room_coords(grid):
    min_room_width = int(grid.shape[1] * MIN_ROOM_WIDTH)
    min_room_height = int(grid.shape[0] * MIN_ROOM_HEIGHT)
    max_room_width = int(grid.shape[1] * MAX_ROOM_WIDTH)
    max_room_height = int(grid.shape[0] * MAX_ROOM_HEIGHT)
    room_x = np.random.randint(3, grid.shape[1] - max_room_width -3)
    room_y = np.random.randint(3, grid.shape[0] - max_room_height - 3)
    room_width =  np.random.randint(min_room_width, max_room_width)
    room_height = np.random.randint(min_room_height, max_room_height)
    room_area = room_width * room_height
    max_room_area = int(grid.shape[0] * grid.shape[1] * MAX_ROOM_AREA)
    if room_area > max_room_area:
        excess = room_area - max_room_area
        room_width -= excess // room_height
    return room_x, room_y, room_width, room_height    
    
def generate_rooms(room_count, grid):
    rooms = []
    while len(rooms) < room_count:
        new_room = gen_room_coords(grid)
        if not any(does_intersect(new_room, room) for room in rooms):
            rooms.append(new_room)
    return rooms

def find_rooms_edges(rooms, grid):
    for room in rooms:
        grid[room[1]:room[1]+room[3], room[0]:room[0]+room[2]] = 1
        grid[room[1]:room[1]+1, room[0]:room[0]+room[2]] = 2  # Top edge
        grid[room[1]+room[3]-1:room[1]+room[3], room[0]:room[0]+room[2]] = 2  # Bottom edge
        grid[room[1]:room[1]+room[3], room[0]:room[0]+1] = 2  # Left edge
        grid[room[1]:room[1]+room[3], room[0]+room[2]-1:room[0]+room[2]] = 2  # Right edge
    return grid
                    
def generate_floorplan(cell_size: int = None, dimensions: tuple[int, int] = None):
    grid = initialize_grid(dimensions[1] // cell_size, dimensions[0] // cell_size)
    room_count = gen_count(dimensions, cell_size)
    rooms = generate_rooms(room_count, grid)
    grid = find_rooms_edges(rooms, grid)
    return grid

def print_floorplan(floorplan):
    for row in floorplan:
        print(''.join(str(int(cell)) for cell in row))
    print()

