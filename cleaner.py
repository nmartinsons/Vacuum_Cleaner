import csv
import heapq

# Directions for moving
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def read_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        
    start_row = int(lines[0].partition('#')[0].strip())  # Starting X
    start_col = int(lines[1].partition('#')[0].strip())  # Starting Y
    battery = int(lines[2].partition('#')[0].strip())  # Starting Battery
    move_cost = int(lines[3].partition('#')[0].strip())  # Movement Cost
    vacuum_cost = int(lines[4].partition('#')[0].strip())  # Vacuuming Cost
    
    grid = []
    for line in lines[5:]:
        clean_line = line.partition('#')[0].strip()  # Remove comments and strip whitespace
        if clean_line:  # Ignore empty lines
            grid.append([int(cell) for cell in clean_line.split(',')])
    return start_row, start_col, battery, move_cost, vacuum_cost, grid

def check_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != 9001  # 9001 is a wall

def clean(start_row, start_col, battery, move_cost, vacuum_cost, grid):
    dirt_cleaned = 0
    squares_cleaned = 0
    visited = set()
    priority_queue = []
    parent_map = {}  # To track the path correctly

    # Push the starting position (negated dirt value for max-heap)
    heapq.heappush(priority_queue, (-grid[start_row][start_col], start_row, start_col, battery))
    parent_map[(start_row, start_col)] = None  # Start of path

    final_position = (start_row, start_col)

    while priority_queue:
        dirt, row, column, rem_battery = heapq.heappop(priority_queue)

        if (row, column) in visited:
            continue
        visited.add((row, column))

        # Clean if possible and dirt is positive
        if grid[row][column] > 0 and rem_battery >= vacuum_cost:
            dirt_cleaned += grid[row][column]
            rem_battery -= vacuum_cost
            squares_cleaned += 1
            grid[row][column] = 0  # Mark as cleaned (set dirt to 0)

        # Try moving to adjacent squares
        for move_row, move_column in directions:
            new_row = row + move_row
            new_column = column + move_column
            if check_bounds(grid, new_row, new_column) and (new_row, new_column) not in visited:
                if rem_battery >= move_cost:
                    heapq.heappush(priority_queue, (-grid[new_row][new_column], new_row, new_column, rem_battery - move_cost))
                    parent_map[(new_row, new_column)] = (row, column)  # Track where we came from
                    final_position = (new_row, new_column)  # Update last visited position

    # **Reconstruct Path from parent_map**
    path = []
    while final_position is not None:
        path.append(final_position)
        final_position = parent_map[final_position]
    path.reverse()  # Reverse to get the correct order

    return dirt_cleaned, squares_cleaned, path, rem_battery

# Example Usage:
start_row, start_column, battery, move_cost, vacuum_cost, grid = read_file("data.csv")
dirt_cleaned, squares_cleaned, path, rem_battery = clean(start_row, start_column, battery, move_cost, vacuum_cost, grid)

print("Dirt Cleaned:", dirt_cleaned) 
print("Squares Cleaned:", squares_cleaned) 
print("Path Taken:", path)
print("Remaining Battery:", rem_battery)
