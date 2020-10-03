from wall import Wall

def level_interpreter(level):
    # List of levels
    levels = [[["+ +-+-+-+-+-+-+-+"],
              ["|     |         |"],
              ["+-+-+ + +-+ +   +"],
              ["|     | |   |   |"],
              ["+ +-+-+ + +-+-+ +"],
              ["| |     | |     |"],
              ["+ +-+-+ + + +-+ +"],
              ["|       |   |   |"],
              ["+-+-+-+-+-+-+-+-+"]]]

    # Select current level
    level = levels[level - 1]

    # Setup dimensions of grid
    w_w = 4
    w_h = 100
    top_gap = 50
    left_gap = 50

    # List of walls generated
    walls = []
    
    line_y = top_gap
    for l in range(len(level)):        
        line = level[l][0]
        # Decide whether row is w_w or w_h high
        if l % 2 == 0:
            row_h = w_w
        else:
            row_h = w_h

        col_x = left_gap
        for c in range(len(line)):
            character = line[c]
            # Decide whether col is w_w or w_h wide
            if c % 2 == 1:
                col_w = w_h
            else:
                col_w = w_w

            # Decide what type of wall should be added
            if character == "+":
                walls.append(Wall(col_x,line_y,w_w,w_w))
            elif character == "|":
                walls.append(Wall(col_x,line_y,w_w,w_h))
            elif character == "-":
                walls.append(Wall(col_x,line_y,w_h,w_w))

            col_x += col_w
        line_y += row_h

    return walls