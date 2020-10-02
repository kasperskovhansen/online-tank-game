from wall import Wall

def level_interpreter(level):
    w_w = 5
    w_h = 100
    
    lines = level.splitlines()
    walls = []

    line_y = 0
    for l in range(len(lines)):
        line = lines[l]
        print(l)
        if l % 2 == 1:
            row_h = w_w
        else:
            row_h = w_h

        col_x = 50
        for c in range(len(line)):
            character = line[c]
            print([character, c])
            
            if c % 2 == 1:
                col_w = w_h
            else:
                col_w = w_w

            if character == "+":
                walls.append(Wall(col_x,line_y,w_w,w_w))
            elif character == "|":
                walls.append(Wall(col_x,line_y,w_w,w_h))
            elif character == "-":
                walls.append(Wall(col_x,line_y,w_h,w_w))

            col_x += col_w
        line_y += row_h

    return walls