def maze_copy(maze):
    new_maze = []    
    for row in maze:
        new_maze.append(row.copy())    
    return new_maze