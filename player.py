import pygame
from bullet import Bullet
from math import cos, sin, pi
import globals

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
        self.old_x = x
        self.old_y = y
        self.ang = 0
        self.vel = 0        
        self.last_not_colliding = [self.old_x, self.old_y]
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
            self.ang += 8
        elif keys[pygame.K_d]:
            self.ang -= 8     
        self.encoded_changes["ang"] = self.ang


    def move(self, walls):
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

        self.update(walls)

    def shoot(self):
        print("x y ({}, {})".format(self.rect.centerx, self.rect.centery))
        bullet = Bullet(self.rect.centerx + cos(self.ang*pi/180) * 25, self.rect.centery - + sin(self.ang*pi/180) * 25, self.ang)
        return bullet       


    def update(self, walls):
        self.rect.centerx = self.old_x + self.x_pos
        self.rect.centery = self.old_y - self.y_pos
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)        
        if len(wall_hit_list) == 0:
            self.last_not_colliding = [self.rect.centerx, self.rect.centery]
        for wall in wall_hit_list:
            self.rect.centerx = self.last_not_colliding[0]
            self.rect.centery = self.last_not_colliding[1]
            self.old_x = self.last_not_colliding[0]
            self.old_y = self.last_not_colliding[1]
            # if self.x_pos > 0:                
            # elif self.x_pos < 0 and self.rect.left > wall.rect.right:
            #     self.rect.left = wall.rect.right

        # wall_hit_list = pygame.sprite.spritecollide(self, walls, False)     
        # for wall in wall_hit_list:
        #     self.rect.centery = self.old_y
        #     if self.y_pos > 0 and self.rect.bottom < wall.rect.top:
        #         self.rect.bottom = wall.rect.top
        #     elif self.y_pos < 0 and self.rect.top < wall.rect.bottom:
        #         self.rect.top = wall.rect.bottom   
        