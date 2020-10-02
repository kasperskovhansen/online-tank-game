import pygame
from math import cos, sin, pi
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, ang):
        super().__init__()        
        
        self.image = pygame.Surface((4, 4))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()   
        self.x_pos = 0
        self.y_pos = 0
        print(self.x_pos, self.y_pos)
        self.old_x = x
        self.old_y = y
        self.ang = ang
        self.vel = 6
        self.timer = 0      
        self.last_not_colliding = [self.x_pos, self.y_pos]  

    def set_coords(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y     

    def update(self, walls):
        self.old_x = self.old_x + self.x_pos
        self.old_y = self.old_y - self.y_pos
        self.x_pos = cos(self.ang*pi/180) * self.vel
        self.y_pos = sin(self.ang*pi/180) * self.vel        
        self.rect = self.image.get_rect()

        self.set_coords(self.old_x + self.x_pos, self.old_y - self.y_pos)      
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)   
        if len(wall_hit_list) == 0:
            self.last_not_colliding = [self.rect.centerx, self.rect.centery]     
        for wall in wall_hit_list:
            if self.x_pos > 0:
                if self.last_not_colliding[0] < wall.rect.left and self.rect.right > wall.rect.left:
                    self.ang -= 180 + 2 * (self.ang % 180)                    
                    self.set_coords(self.last_not_colliding[0], self.last_not_colliding[1])
            if self.x_pos < 0:
                if self.last_not_colliding[0] > wall.rect.right and self.rect.left < wall.rect.right:
                    self.ang -= 180 + 2 * (self.ang % 180)                    
                    self.set_coords(self.last_not_colliding[0], self.last_not_colliding[1])

            if self.y_pos < 0:
                if self.last_not_colliding[1] < wall.rect.top and self.rect.bottom > wall.rect.top:
                    self.ang += 2 * (180 - (self.ang % 360))
                    self.set_coords(self.last_not_colliding[0], self.last_not_colliding[1])
            if self.y_pos > 0:
                if self.last_not_colliding[1] > wall.rect.bottom and self.rect.top < wall.rect.bottom:
                    self.ang += 2 * (180 - (self.ang % 360))
                    self.set_coords(self.last_not_colliding[0], self.last_not_colliding[1])