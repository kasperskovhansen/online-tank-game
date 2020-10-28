from sprites.wall import Wall
from utils.maze_gen import maze_gen
from utils.maze_copy import maze_copy
import random

class Level():
    """
    Class controlling and loading level state
    """
    def __init__(self):
         # List of levels
        # self.levels = [[["+-+-+-+-+-+-+-+-+"],
        #                 ["|     |         |"],
        #                 ["+-+-+ + +-+ +   +"],
        #                 ["|     | |   |   |"],
        #                 ["+ +-+-+ + +-+-+ +"],
        #                 ["| |       | |   |"],
        #                 ["+ +-+-+ + + +-+ +"],
        #                 ["|       |   |   |"],
        #                 ["+ +-+-+ +-+-+ +-+"],
        #                 ["|           |   |"],
        #                 ["+ +-+-+ +   +-+ +"],
        #                 ["|       |       |"],
        #                 ["+-+-+-+-+-+-+-+-+"]]]

        # List of generated walls
        self.walls = []

        # List of spots for power ups and tanks
        self.spots = []

        # Setup dimensions of grid
        self.maze_w = 16
        self.maze_h = 8

        # Walls
        self.w_w = 5
        self.w_h = 55
        self.top_gap = 50
        self.left_gap = 12
        
        # Load the level
        # self.level = random.randint(0, len(self.levels) -1)
        self.level = None
        self.level_list_clean = []
        self.level_list_path = []

        # self.level = gen_maze()
        self.level_loader()
        
    def field_from_pos(self, pos):
        line_y = self.top_gap

        field_x = None
        field_y = None
        for l in range(len(self.level)):        
            line = self.level[l][0]
            # Decide whether row is self.w_w or self.w_h high
            if l % 2 == 0:
                row_h = self.w_w
            else:
                row_h = self.w_h

            col_x = self.left_gap

            if not field_x:
                for c in range(len(line)):
                    character = line[c]
                    # Decide whether col is self.w_w or self.w_h wide
                    if c % 2 == 1:
                        col_w = self.w_h
                        # Add free spot coords to list but only on odd col and row numbers
                        if l % 2 == 1:
                            if character == " ":
                                self.spots.append([col_x + self.w_h / 2, line_y + self.w_h / 2, True])
                    else:
                        col_w = self.w_w                    
                                    
                    if col_x <= pos[0] and pos[0] < col_x + col_w:                        
                        field_x = c
                    col_x += col_w
            if line_y <= pos[1] and pos[1] < line_y + row_h:                
                field_y = l
                break
            line_y += row_h

        return [field_y, field_x]

    def pos_from_field(self, field):
        x = field[1]
        y = field[0]        

        x_pos = self.left_gap
        y_pos = self.top_gap

        to_add = 0
        for i in range(x):
            to_add = self.w_w if i % 2 == 1 else self.w_h
            x_pos += to_add
        x_pos -= to_add // 2

        to_add = 0
        for j in range(y):
            to_add = self.w_w if j % 2 == 1 else self.w_h
            y_pos += to_add
        y_pos -= to_add // 2
        return [x_pos, y_pos]

    def level_loader(self):
        # level = self.levels[self.level]
        self.level = maze_gen(x_cells = self.maze_w, y_cells = self.maze_h, passages = 70)             
        print(self.level)
        for row in self.level:
            print("Row:")
            print(row[0])
            line = []
            for char in row[0]:
                line.append(char)
            print("Line: ")
            print(line)
            self.level_list_clean.append(line)
        self.level_list_path = maze_copy(self.level_list_clean)
            

        line_y = self.top_gap
        for l in range(len(self.level)):        
            line = self.level[l][0]
            print(line)
            # Decide whether row is self.w_w or self.w_h high
            if l % 2 == 0:
                row_h = self.w_w
            else:
                row_h = self.w_h

            col_x = self.left_gap
            for c in range(len(line)):
                character = line[c]
                # Decide whether col is self.w_w or self.w_h wide
                if c % 2 == 1:
                    col_w = self.w_h
                    # Add free spot coords to list but only on odd col and row numbers
                    if l % 2 == 1:
                        if character == " ":
                            self.spots.append([col_x + self.w_h / 2, line_y + self.w_h / 2, True])
                else:
                    col_w = self.w_w                

                # Decide what type of wall should be added
                if character == "+":
                    self.walls.append(Wall(col_x, line_y, self.w_w, self.w_w))
                elif character == "|":
                    self.walls.append(Wall(col_x, line_y, self.w_w, self.w_h))
                elif character == "-":
                    self.walls.append(Wall(col_x, line_y, self.w_h, self.w_w))
                
                col_x += col_w
            line_y += row_h

    def get_free_spot(self, should_lock=True):
        tries = 0
        free_spot = False
        while not free_spot and tries < len(self.spots):
            tries += 1
            spot_num = random.randint(0, len(self.spots) -1)
            if self.spots[spot_num][2]:
                if should_lock:
                    self.spots[spot_num][2] = False
                return self.spots[spot_num][0], self.spots[spot_num][1], spot_num

        return False

    def set_free_spot(self, spot_num):
        self.spots[spot_num][2] = True
        print(self.spots)