import csv
import heapq

# Directions for moving (up, down, left, right)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def read_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        
    start_row = int(lines[0].partition('#')[0].strip())  # Starting X
    start_col = int(lines[1].partition('#')[0].strip())  # Starting Y
    battery = int(lines[2].partition('#')[0].strip())  # Starting Battery
    move_cost = int(lines[3].partition('#')[0].strip())  # Movement Cost
    vacuum_cost = int(lines[4].partition('#')[0].strip())  # Vacuuming Cost
    
    # Reading the grid, starting from the 5th line in the csv file
    grid = []
    for line in lines[5:]:
        clean_line = line.partition('#')[0].strip()  # Remove comments and strip whitespace
        if clean_line:
            # Appeing to the grid list the grid values and converts them into integers and splits them with commas
            grid.append([int(cell) for cell in clean_line.split(',')])
    # Extracting the file contents
    return start_row, start_col, battery, move_cost, vacuum_cost, grid

# Function for checking the bounds of the map
# We check if the row is between 0 and length of the grid
# Similarly, the columns are checked to ensure that they are between 0 and length of the first column, assuming that all rows have the same number of columns
# Finally we check that at the position (row, column) there is not tile with number 9001
def check_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != 9001  # 9001 is a wall

def clean(start_row, start_col, battery, move_cost, vacuum_cost, grid):
    dirt_cleaned = 0
    squares_cleaned = 0
    visited = set()
    priority_queue = []
    map = {}  # Map for trackong the movement, which will help to backtrack the path
    remaining_battery = battery  # Track correct battery

    # Pushing elements on the priority queue
    # by negating the value on the grid, the max-heap structure is achieved by prioritizing the highest values
    heapq.heappush(priority_queue, (-grid[start_row][start_col], start_row, start_col, battery))
    
    map[(start_row, start_col)] = None  
    final_position = (start_row, start_col)

    while priority_queue:
        dirt, row, column, rem_battery = heapq.heappop(priority_queue)

        if (row, column) in visited:
            continue
        visited.add((row, column))

        # If there's dirt, vacuum it
        if grid[row][column] > 0 and rem_battery >= vacuum_cost:
            dirt_cleaned += grid[row][column]
            rem_battery -= vacuum_cost  # Deduct vacuum cost
            squares_cleaned += 1
            grid[row][column] = 0  # Mark as cleaned

        # Update battery at each step
        remaining_battery = rem_battery  

        # Try moving to adjacent squares
        for move_row, move_column in directions:
            new_row = row + move_row
            new_column = column + move_column
            if check_bounds(grid, new_row, new_column) and (new_row, new_column) not in visited:
                if rem_battery >= move_cost:
                    new_battery = rem_battery - move_cost  # Deduct movement cost before pushing
                    heapq.heappush(priority_queue, (-grid[new_row][new_column], new_row, new_column, new_battery))
                    map[(new_row, new_column)] = (row, column)  # Track the path
                    final_position = (new_row, new_column)  # Update last position

    # **Reconstruct Path from map**
    path = []
    while final_position is not None:
        path.append(final_position)
        final_position = map[final_position]
    path.reverse()  # Reverse to get correct order

    return dirt_cleaned, squares_cleaned, path, remaining_battery

# TEST
start_row, start_column, battery, move_cost, vacuum_cost, grid = read_file("data.csv")
dirt_cleaned, squares_cleaned, path, remaining_battery = clean(start_row, start_column, battery, move_cost, vacuum_cost, grid)

print("Dirt Cleaned:", dirt_cleaned) 
print("Squares Cleaned:", squares_cleaned) 
print("Path Taken:", path)
print("Remaining Battery:", remaining_battery)
