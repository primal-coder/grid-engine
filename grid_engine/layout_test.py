from collections import deque
import random


def generate_layout(grid):
        
        min_room_width = 5
        min_room_height = 5
        max_room_width = 20
        max_room_height = 20
        
        center_cell = grid.cells[len(grid.cells) // 2 + (len(grid.cols)//2)]
        edge_cells = grid.get_edge_cells()
        start_cell = center_cell.col[-2]
        floor_cells = set()
        wall_cells = set()
        room_cells = set()
        room_count = 0
        visited = set()
        queue = deque([start_cell])
        
        def visit(cell):
            if cell not in visited:
                visited.add(cell)
                floor_cells.add(cell)
                
        def layout_first_room(current_cell):
            room_width = max(random.randint(min_room_width, max_room_width), clearance_x)
            room_height = max(random.randint(min_room_height, max_room_height), clearance_y)
            room_cell_count = room_width * room_height
            if current_cell.clearance_left >= room_width//2 and current_cell.clearance_right >= room_width//2:
                room_anchor = current_cell.row[current_cell.col_index - room_width//2]
                room_center = current_cell.col[current_cell.row_index - room_height//2]
                room_x = room_anchor.col_index
                room_y = room_anchor.row_index
                room_set = set()
                for Set in [floor_cells, room_set, visited]:
                    for xcell in range(room_width):
                        for ycell in range(room_height):
                            Set.add(grid.cells[(room_x + xcell, room_y + ycell)])
                room_cells.add(room_set)
                queue.add(random.choice())
                room_count += 1

        def get_room_edges(room_set):
            room_edge = set()
            for cell in room_set:
                adjacent_cells = [grid[adj] for adj in cell.adjacent]
                if any(adj_cell not in room_set for adj_cell in adjacent_cells):
                    room_edge.add(cell)
            return room_edge
        
        while queue:
            
            current_cell = queue.popleft()
            
            if current_cell in [start_cell, start_cell.up]:
                visit(current_cell)
                queue.append(current_cell.up)
                continue
            elif current_cell not in visited:
                visit(current_cell)
                if room_count == 0:
                    layout_first_room(current_cell)
                    room_edges = get_room_edges(room_cells[0])
                    next_hall_prestart = random.choice(list(room_edges))
                    next_hall_start = random.choice([
                            grid[adj] for adj in next_hall_prestart.adjacent 
                            if grid[adj] not in room_cells[0] and 
                            grid[adj] not in visited
                        ])