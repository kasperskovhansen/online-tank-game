import numpy as np
import random
# from maze_gen import maze_gen, export_maze
from datetime import datetime
import os
from time import sleep

def export_maze_steps(steps):
    np.savetxt("maze_steps.csv", steps, delimiter=",", fmt='%s')

def directions(maze, pos, check_for=['1'], inverse=True, steps=2):
    # Directions to check for. Move "steps" steps
    dirs_to_check = [[-steps, 0], [0, steps], [steps, 0], [0, -steps]]
    y, x = pos  # Coordinates
    dirs = []  # Lists for directions
    dirs_inverse = []
    for dir in dirs_to_check:
        if y + dir[0] >= 0 and x + dir[1] >= 0 and y + dir[0] < 2*len(maze) and x + 2*dir[1] < len(maze[0]):
            if not maze[y + dir[0]][x + dir[1]] in check_for:
                # This direction is not checked. Add to dirs_inverse
                dirs_inverse.append([y + dir[0], x + dir[1]])
                # dirs_inverse.append([y + 2*dir[0], x + 2*dir[1]])
                # maze[y + dir[0], x + dir[1]] = 'v'
            else:
                # This direction is marked. Add to dirs
                dirs.append([y + dir[0], x + dir[1]])
                # dirs.append([y + 2*dir[0], x + 2*dir[1]])
                # maze[y + dir[0], x + dir[1]] = 'v'
    if inverse:  # Decide what to return
        return dirs_inverse
    return dirs

def maze_solve(maze, start_pos, end_pos):          
    
    global should_break      
    if start_pos[0] == None or start_pos[1] == None or end_pos[0] == None or end_pos[1] == None:
        return False
    maze[start_pos[0]][start_pos[1]] = 'O'
    maze[end_pos[0]][end_pos[1]] = 'X'
    
    # for r in range(len(maze)):  # Print the maze we are working with
    #     line = ''
    #     for c in range(len(maze[0])):
    #         line += str(maze[r][c])
    #     print(line)

    data = [[[start_pos, 0]]]  # Create first layer of data array

    should_break = False
    iteration = 0
    idx = 0
    while True:    
        current_fields = data[-1]        
        new_line = []
        
        for i in range(len(current_fields)):            
            field = current_fields[i]            
            free_fields = directions(maze, [field[0][0], field[0][1]], check_for = [' ', '', 'X'], inverse = False, steps=1)            
            
            for f in range(len(free_fields)):                
                new_field = free_fields[f]                                
                if maze[new_field[0]][new_field[1]] == maze[end_pos[0]][end_pos[1]]:       
                    should_break = True          
                    idx = f - 1                
                # maze[new_field[0]][new_field[1]] = iteration % 10
                maze[new_field[0]][new_field[1]] = 1
                new_line.append([new_field, i])
                if should_break:
                    # print("Breaking")
                    break
            if should_break:
                # print("Breaking 2")
                break        

        data.append(new_line)
        if len(new_line) == 0:
            return False
        # for r in range(len(maze)):  # Print the maze we are working with
        #     line = ''
        #     for c in range(len(maze[0])):
        #         line += str(maze[r][c])
        #     print(line)

        # sleep(1/1000)
        # os.system('clear')


        iteration += 1        

        if should_break:
            break

    steps = []
    for i in range(len(data)):
        curr_row = data[len(data) - i - 1]
        cell = curr_row[idx]
        steps.insert(0, cell[0])   
        idx = cell[1]    
    return steps


# start_time_gen = datetime.now()  # Start stopwatch
# maze = maze_gen(x_cells=150, y_cells=20, passages=20, stringify=False, entrances=False)
# # maze = maze_gen(x_cells=1280, y_cells=800-44, passages=0, stringify=False, entrances=False)
# # maze = maze_gen(x_cells=50, y_cells=20, passages=50, stringify=False, entrances=False)

# # Stop stopwatch and print time
# print("Maze generated in: {}".format(datetime.now() - start_time_gen))

# start_pos = [1, 1]
# end_pos = [len(maze) - 2, len(maze[0]) - 2]

# start_time_solve = datetime.now()  # Start stopwatch
# steps = maze_solve(maze.copy(), start_pos.copy(), end_pos.copy())


# # print(steps)  # Steps

# print('Solved:')
# for step in steps:
#     maze[step[0]][step[1]] = '#'
# maze[start_pos[0]][start_pos[1]] = 'O'
# maze[end_pos[0]][end_pos[1]] = 'X'

# export_maze(maze)
# export_maze_steps(steps)

# for r in range(len(maze)):  # Print the maze we are working with
#     line = ''
#     for c in range(len(maze[0])):
#         line += maze[r][c]
#     print(line)

# # Stop stopwatch and print time
# print("Maze solved in: {}".format(datetime.now() - start_time_solve))