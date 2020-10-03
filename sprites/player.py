import pygame
from sprites.bullet import Bullet
from math import cos, sin, pi

# Load sound effects
pygame.init()
bad_move = pygame.mixer.Sound('sounds/bad_move.wav')
bad_move.set_volume(0.5)

class Player(pygame.sprite.Sprite):
    # Setup
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
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.tank_id = 0
        self.hit_by = None
        self.num_bullets = 5

    # Network multiplayer stuff
    def parse_changes(self, encoded_changes):
        for key, value in encoded_changes.items():
            print("{}, {}".format(key, value))

    # Change tank moving speed
    def speed(self, keys):
        if keys[pygame.K_w]:
            self.vel = 4
        elif keys[pygame.K_s]:
            self.vel = -2
        else:
            if not self.vel:
                return
            self.vel = 0
        self.encoded_changes["vel"] = self.vel
    
    # Change tank direction
    def turn(self, keys):
        if keys[pygame.K_a]:
            self.ang += 5
        elif keys[pygame.K_d]:
            self.ang -= 5     
        self.encoded_changes["ang"] = self.ang

    # Move player to new position and update afterwards
    def move(self, walls_list, bullets_list):
        keys = pygame.key.get_pressed()
        self.speed(keys)
        self.turn(keys)
        self.old_x = self.old_x + self.x_pos
        self.old_y = self.old_y - self.y_pos
        self.x_pos = cos(self.ang*pi/180) * self.vel
        self.y_pos = sin(self.ang*pi/180) * self.vel       
        self.image = pygame.transform.rotate(self.image_clean, self.ang)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        self.update(walls_list, bullets_list)

    # Fire a new bullet
    def shoot(self):
        # Only fire if player has not fired all rounds
        if self.num_bullets > 0:
            self.num_bullets -= 1
            bullet = Bullet(self.rect.centerx + cos(self.ang*pi/180) * 15, self.rect.centery - + sin(self.ang*pi/180) * 15, self.ang, self.tank_id)
            return bullet       
        else:
            return None

    # Update pos if not hitting a wall or hit by bullet
    def update(self, walls_list, bullets_list):
        # Check if hit by a bullet
        if self.hit_by != None:
            print("Player: {} hit by player: {}".format(self.tank_id, self.hit_by))
            bad_move.play()
            self.hit_by = None

        # Move tank
        self.rect.centerx = self.old_x + self.x_pos
        self.rect.centery = self.old_y - self.y_pos             

        # If move wasn't allowed, move back
        wall_hit_list = pygame.sprite.spritecollide(self, walls_list, False, collided=pygame.sprite.collide_mask)        
        if len(wall_hit_list) == 0:
            self.last_not_colliding = [self.rect.centerx, self.rect.centery]
        for wall in wall_hit_list:
            self.rect.centerx = self.last_not_colliding[0]
            self.rect.centery = self.last_not_colliding[1]
            self.old_x = self.last_not_colliding[0]
            self.old_y = self.last_not_colliding[1]
            