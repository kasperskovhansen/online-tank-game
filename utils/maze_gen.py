import numpy as np
from random import randint
from datetime import datetime
start_time = datetime.now()  # Start stopwatch


def export_maze(maze):
    np.savetxt("maze.csv", maze, delimiter=",", fmt='%s')

def directions(maze, pos, check_for=['1'], inverse=True, steps=2):
    # Directions to check for. Move "steps" steps
    dirs_to_check = [[0, steps], [0, -steps], [steps, 0], [-steps, 0]]
    y, x = pos  # Coordinates
    dirs = []  # Lists for directions
    dirs_inverse = []
    for dir in dirs_to_check:
        if y + dir[0] >= 0 and x + dir[1] >= 0 and y + dir[0] < len(maze) and x + dir[1] < len(maze[0]):
            if not maze[y + dir[0]][x + dir[1]] in check_for:
                # This direction is not checked. Add to dirs_inverse
                dirs_inverse.append([y + dir[0], x + dir[1]])
            else:
                # This direction is marked. Add to dirs
                dirs.append([y + dir[0], x + dir[1]])
    if inverse:  # Decide what to return
        return dirs_inverse
    return dirs


def maze_gen(canvas_w=100, canvas_h=100, y_cells=3, x_cells=3, wall_cell_ratio=10, passages=100, entrances = False, stringify=True):
    """ Find links """
    maze = np.zeros([y_cells * 2 + 1, x_cells * 2 + 1],
                    dtype=str)  # Setup of empty maze
    stringified_maze = []  # More readable export format
    pos = [1, 1]  # Start pos: (y, x)
    stack = []  # List of previous positions
    while True:
        choices = directions(maze, pos)  # Possible choises to move
        maze[pos[0]][pos[1]] = 1  # Mark pos as visited
        if len(choices) > 0:
            stack.append(pos)  # Add this pos to stack
            # Decide where to go next
            new_pos = choices[randint(0, len(choices) - 1)]
            # Mark new link in maze
            maze[int((pos[0] + new_pos[0]) / 2)
                 ][int((pos[1] + new_pos[1]) / 2)] = 'L'
            pos = new_pos  # new_pos is the next pos.
        elif len(stack) > 0:
            stack.pop()  # We hit a dead end. Going back one step
            if len(stack) == 1:
                break  # If stack has one element, we are done
            pos = stack[len(stack) - 1]  # pos is the lastest element in stack
        else:
            break
    """ Remove a number of walls """
    for i in range(round(y_cells * x_cells * passages / 100)):
        y = randint(1, y_cells * 2 - 1)
        x = None
        if y % 2 == 1:  # Determine possible x-vals on behalf of chosen y
            x = randint(0, x_cells - 2) * 2 + 2
        else:
            x = randint(0, x_cells - 1) * 2 + 1
        maze[y][x] = ' '

    """ Fill walls with correct signs """
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            current_char = maze[r][c]  # The char at this position right now
            char = ' '
            if current_char == '1' or current_char == 'L':  # If current character is a link or visited
                char = ' '
            elif not current_char:  # Otherwise add a wall
                if r % 2 == 0:
                    if c % 2 == 0:
                        char = '+'
                    else:
                        char = '-'
                else:
                    if c % 2 == 0:
                        char = '|'

            maze[r][c] = char  # Update maze

    for r in range(len(maze)):  # Remove redundant plus signs
        for c in range(len(maze[0])):
            if maze[r][c] == '+':
                nearby_spaces = directions(maze, [r, c], check_for=[
                                        ' '], inverse=False, steps=1)
                if len(nearby_spaces) == 4:
                    maze[r][c] = ' '

    if entrances:  # Create entrances
        hole = randint(1, len(maze) - 1)
        maze[hole - (hole - 1) % 2][0] = " "

        hole2 = randint(1, len(maze) - 1)
        maze[hole2 - (hole2 - 1) % 2][len(maze[0]) - 1] = " "

    if stringify:  # Return maze
        for row in maze:
            line = ''
            for char in row:
                line += char
            stringified_maze.append([line])
        return stringified_maze
    return maze


# maze = maze_gen(y_cells=10, x_cells=30)  # Generate a maze
# for row in maze:  # Print the generated maze
#     print(row[0])

# Stop stopwatch and print time
# print("Time: {}".format(datetime.now() - start_time))
