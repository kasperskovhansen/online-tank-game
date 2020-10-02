import pygame
from math import cos, sin, pi
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, ang):
        super().__init__()        
        
        self.image = pygame.Surface((4, 4))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()   
        self.x_pos = x
        self.y_pos = -y
        print(self.x_pos, self.y_pos)
        self.old_x = 0
        self.old_y = 0
        self.ang = ang #+  random.random()*20-10
        self.vel = 6
        self.timer = 0

        self.update()

    def set_coords(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y     

    def update(self):
        self.old_x = self.old_x + self.x_pos
        self.old_y = self.old_y - self.y_pos
        self.x_pos = cos(self.ang*pi/180) * self.vel
        self.y_pos = sin(self.ang*pi/180) * self.vel        
        self.rect = self.image.get_rect()

        self.set_coords(self.old_x + self.x_pos, self.old_y - self.y_pos)        
        