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
    # Keeping track of the path we went through to reconstruct later
    map[(start_row, start_col)] = None
    # Keeping track of the last position   
    final_position = (start_row, start_col)

    # While loop which executes until there are elements in the priority_queue
    while priority_queue:
        # Removing and returning the values from the heap queue
        dirt, row, column, rem_battery = heapq.heappop(priority_queue)
        # Checking if the square was already visited to avoid same reprocessing
        if (row, column) in visited:
            continue
        visited.add((row, column))

        # Presence of dirt is checked and that there is enough battery
        if grid[row][column] > 0 and rem_battery >= vacuum_cost:
            dirt_cleaned += grid[row][column] # Incrementing dirt value based on the square value
            rem_battery -= vacuum_cost # deducting vacuuming cost
            squares_cleaned += 1 # incerements squares cleaned
            grid[row][column] = 0 # Marks square as cleaned

        # Keeping track of the battery
        remaining_battery = rem_battery  

        # For loop which iterates over all four moving directions
        for move_row, move_column in directions:
            new_row = row + move_row # Computation of new row position 
            new_column = column + move_column # Computation of new row column
            # The verification is made for the new position that it is not wall and already not in the visited set
            if check_bounds(grid, new_row, new_column) and (new_row, new_column) not in visited:
                # Checking if there is enough battery for moving
                if rem_battery >= move_cost:
                    new_battery = rem_battery - move_cost  # Reducing battery by the movement cost
                    # Adding the new position to the priority queue, including the new battery
                    heapq.heappush(priority_queue, (-grid[new_row][new_column], new_row, new_column, new_battery))
                    map[(new_row, new_column)] = (row, column)  # Tracking the path (from and to)
                    final_position = (new_row, new_column)  # Updating the last position of the vacuuming

    # The path is reconstructed to display exactly the same path the vacuum cleaner took
    path = [] # list for string the path
    # We iterate from the final position until the starting position and when there are no elements left, it stops
    while final_position is not None:
        # In each iteration the positions are added to the path list
        path.append(final_position)
        # By this backward movement along the path is achieved
        final_position = map[final_position]
    path.reverse()  # Reversing the path to get correct order (start to end)

    return dirt_cleaned, squares_cleaned, path, remaining_battery

# TEST
# Assigning the variables to the returned values
start_row, start_column, battery, move_cost, vacuum_cost, grid = read_file("data.csv")
dirt_cleaned, squares_cleaned, path, remaining_battery = clean(start_row, start_column, battery, move_cost, vacuum_cost, grid)

print("Dirt Cleaned:", dirt_cleaned) 
print("Squares Cleaned:", squares_cleaned) 
print("Path Taken:", path)
print("Remaining Battery:", remaining_battery)
