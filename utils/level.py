from sprites.wall import Wall
import random

class Level():
    """
    Class controlling and loading level state
    """
    def __init__(self):
         # List of levels
        self.levels = [[["+-+-+-+-+-+-+-+-+"],
                        ["|     |         |"],
                        ["+-+-+ + +-+ +   +"],
                        ["|     | |   |   |"],
                        ["+ +-+-+ + +-+-+ +"],
                        ["| |     | | |   |"],
                        ["+ +-+-+ + + +-+ +"],
                        ["|       |   |   |"],
                        ["+ +-+-+-+-+-+ +-+"],
                        ["|               |"],
                        ["+-+-+-+-+-+-+-+-+"]]]

        # List of generated walls
        self.walls = []

        # List of spots for power ups and tanks
        self.spots = []

        # Setup dimensions of grid
        self.w_w = 4
        self.w_h = 100
        self.top_gap = 50
        self.left_gap = 50
        
        # Load the level
        self.level = random.randint(0, len(self.levels) -1)
        self.level_loader()
        

    def level_loader(self):
        level = self.levels[self.level]

        line_y = self.top_gap
        for l in range(len(level)):        
            line = level[l][0]
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