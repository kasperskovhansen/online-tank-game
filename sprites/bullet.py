import pygame
from math import cos, sin, pi
from sprites.power_up import get_type
import random

class Bullet(pygame.sprite.Sprite):
    # Setup
    def __init__(self, x, y, ang, tank_id, power_up, sprite_groups):
        super().__init__()        
        self.power_up = power_up   
        self.bullet_image = None                
        self.bullet_image = pygame.image.load("assets/power_ups/" + self.power_up["type"] + ".png")
        self.bullet_image = pygame.transform.scale(self.bullet_image, (self.power_up["bullet_size"][0], self.power_up["bullet_size"][1]))
        self.image = pygame.transform.rotate(self.bullet_image, 0)        
        self.rect = self.image.get_rect()   
        self.x_pos = 0
        self.y_pos = 0
        self.old_x = x
        self.old_y = y        
        self.ang = ang
        self.rect_coords = None
        if "bullet_spread" in self.power_up:
            self.ang += random.random() * self.power_up["bullet_spread"] - self.power_up["bullet_spread"] // 2
        self.vel = self.power_up["bullet_speed"]
        if "frag_speed" in self.power_up:
            self.vel += random.random() * self.power_up["frag_speed"] - self.power_up["frag_speed"] // 2
        self.start_ticks = pygame.time.get_ticks()
        self.last_not_colliding = [self.x_pos, self.y_pos] 
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.tank_id = tank_id
        self.firing = True
        self.sprite_groups = sprite_groups
            
    def explode(self):
        print("Explode!!!")    
        for f in range(self.power_up["fragments"]):
            self.sprite_groups['bullets_list'].add(Bullet(self.rect.centerx + cos((self.ang + random.randint(0, 360))*pi/180) * 15, self.rect.centery - + sin(self.ang*pi/180) * 15, self.ang, self.tank_id, get_type(4), self.sprite_groups))
 
    # Set new coordinates
    def set_coords(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y     

    def polar_to_rect(self):
        pass
    

    # Update position handling player hits and wall rebounce
    def update(self, walls_list, players_list):
        # Kill if time has run out
        this_player = None
        if pygame.time.get_ticks() - self.start_ticks > self.power_up["bullet_lifespan"]:
            for player in players_list:
                if player.tank_id == self.tank_id:
                    this_player = player
                    if player.power_up["type"] == self.power_up["type"]:
                        if player.power_up["bullet_refill"] and player.power_up["max_bullets"] - player.power_up["num_bullets"] > 0:
                            player.power_up["num_bullets"] += 1
                        elif not player.power_up["bullet_refill"]:
                            player.power_up["num_bullets_destroyed"] += 1
                            if player.power_up["num_bullets_destroyed"] == player.power_up["max_bullets"]:
                                player.power_up = get_type(0)                        
            if self.power_up["type"] == "bomb":
                this_player.detonate_bomb()
            else:
                self.kill()            
        elif self.power_up["type"] == "missile" and pygame.time.get_ticks() - self.power_up["bullets_timer"] > self.power_up["homing_off_time"]:
            self.power_up["homing"] = True
            image_name = ""
            if self.power_up["target"] == 0:
                image_name = "_red"
            elif self.power_up["target"] == 1:
                image_name = "_blue"            
            self.bullet_image = pygame.image.load("assets/power_ups/missile" + image_name + ".png")
            self.bullet_image = pygame.transform.scale(self.bullet_image, (self.power_up["bullet_size"][0], self.power_up["bullet_size"][1]))
            self.image = pygame.transform.rotate(self.bullet_image, 0)     
        # Calculate new coords and move
        self.old_x = self.old_x + self.x_pos
        self.old_y = self.old_y - self.y_pos
        self.x_pos = cos(self.ang*pi/180) * self.vel
        self.y_pos = sin(self.ang*pi/180) * self.vel  
        if self.power_up["type"] == "fragment":
            self.power_up["rotation"] = (self.power_up["rotation"] + self.vel * 4) % 360            
            self.image = pygame.transform.rotate(self.bullet_image, self.power_up["rotation"])
        else:
            self.image = pygame.transform.rotate(self.bullet_image, self.ang)
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
            if self.power_up["type"] == "fragment":
                if self.vel > 3:
                    return
                else:
                    self.kill()
                # self.vel = 0
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