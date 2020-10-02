import pygame
from math import cos, sin, pi

class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()        
        if color == "red":
            self.image = pygame.image.load("assets/red_tank.png") 
        self.image = pygame.transform.rotate(self.image, 0)     
        self.image_clean = self.image.copy()  
        self.rect = self.image.get_rect()   
        self.x_pos = 0
        self.y_pos = 0
        self.old_x = 200
        self.old_y = 200
        self.ang = 0
        self.vel = 0        
        self.disconnected = False
        self.encoded_changes = {}

    def parse_changes(self, encoded_changes):
        for key, value in encoded_changes.items():
            print("{}, {}".format(key, value))

    def speed(self, keys):
        if keys[pygame.K_w]:
            self.vel = 5
        elif keys[pygame.K_s]:
            self.vel = -3
        else:
            if not self.vel:
                return
            self.vel = 0
        self.encoded_changes["vel"] = self.vel
    
    def turn(self, keys):
        if keys[pygame.K_a]:
            self.ang += 5
        elif keys[pygame.K_d]:
            self.ang -= 5      
        self.encoded_changes["ang"] = self.ang


    def move(self):
        keys = pygame.key.get_pressed()
        self.speed(keys)
        self.turn(keys)
        self.old_x = self.old_x + self.x_pos
        self.old_y = self.old_y - self.y_pos
        self.x_pos = cos(self.ang*pi/180) * self.vel
        self.y_pos = sin(self.ang*pi/180) * self.vel
        # print("cos: {} sin {}".format(cos(self.ang*pi/180) * 2, sin(self.ang*pi/180) * 2))
        # print("cos: {} sin {}".format(cos(self.ang*pi/180) * -1, sin(self.ang*pi/180) * -1))
        # print("vel: {} ang: {} x,y: ({}, {})".format(self.vel, self.ang, self.x_pos, self.y_pos))        
        
        self.image = pygame.transform.rotate(self.image_clean, self.ang)
        self.rect = self.image.get_rect()

        self.update()

    def set_coords(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y        


    def update(self):
        self.set_coords(self.old_x + self.x_pos, self.old_y - self.y_pos)        
        