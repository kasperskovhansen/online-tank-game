import pygame
from math import cos, sin, pi
import random

class Bullet(pygame.sprite.Sprite):
    # Setup
    def __init__(self, x, y, ang, tank_id):
        super().__init__()        
        self.image = pygame.Surface((4, 4))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()   
        self.x_pos = 0
        self.y_pos = 0
        self.old_x = x
        self.old_y = y
        self.ang = ang
        self.vel = 6
        self.start_ticks = pygame.time.get_ticks()
        self.last_not_colliding = [self.x_pos, self.y_pos] 
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.tank_id = tank_id
        self.firing = True
 
    # Set new coordinates
    def set_coords(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y     

    # Update position handling player hits and wall rebounce
    def update(self, walls_list, players_list):
        # Kill if time has run out
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000
        if seconds > 8:
            for player in players_list:
                if player.tank_id == self.tank_id:
                    player.num_bullets += 1
            self.kill()

        # Calculate new coords and move
        self.old_x = self.old_x + self.x_pos
        self.old_y = self.old_y - self.y_pos
        self.x_pos = cos(self.ang*pi/180) * self.vel
        self.y_pos = sin(self.ang*pi/180) * self.vel        
        self.rect = self.image.get_rect()
        self.set_coords(self.old_x + self.x_pos, self.old_y - self.y_pos)      
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        # Don't kill player if bullet hasn't left shooter yet
        firing_seq_over = True
        player_hit_list = pygame.sprite.spritecollide(self, players_list, False, collided=pygame.sprite.collide_mask)
        for player in player_hit_list:
            if player.tank_id == self.tank_id and self.firing:
                print("Still firing")
                firing_seq_over = False
            if not self.firing:
                player.hit_by = self.tank_id
                for player_hitting in players_list:
                    if player_hitting.tank_id == self.tank_id:
                        player_hitting.num_bullets += 1
                self.kill()
        if self.firing and firing_seq_over:
            self.firing = False
            print("Firing sequence over")

        # Rebounce
        wall_hit_list = pygame.sprite.spritecollide(self, walls_list, False)   
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