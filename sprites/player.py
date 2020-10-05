import pygame
from sprites.bullet import Bullet
from math import cos, sin, pi
import random
from utils.download_audio import download_audio

# Load sound effects
pygame.init()
bad_move = pygame.mixer.Sound('sounds/bad_move.wav')
bad_move.set_volume(0.5)

hee_hee = pygame.mixer.Sound('sounds/hee_hee.wav')
hee_hee.set_volume(1)

jeg_tror_såmænd = pygame.mixer.Sound('sounds/jeg_tror_såmænd.wav')
hee_hee.set_volume(1)
faktisk_lige_er_død = pygame.mixer.Sound('sounds/faktisk_lige_er_død.wav')
faktisk_lige_er_død.set_volume(1)

class Player(pygame.sprite.Sprite):
    # Setup
    def __init__(self, color, x, y, level_spot, tank_id, username):
        super().__init__()       
        self.tank_image = None 

        # Tank images
        if color == "red":
            self.tank_image = pygame.image.load("assets/red_tank.png") 
        elif color == "blue":
            self.tank_image = pygame.image.load("assets/blue_tank.png") 
        elif color == "yellow":
            self.tank_image = pygame.image.load("assets/yellow_tank.png") 
        elif color == "green":
            self.tank_image = pygame.image.load("assets/green_tank.png") 

        # Explode frames
        self.explode_frames = []
        self.frames = 9
        for i in range(self.frames):
            self.explode_frames.append(pygame.image.load("assets/explosion/" + str(i+1) + ".png"))
        self.anim_count = 0
        self.anim_frame = 0

        # Setup
        self.image = pygame.transform.rotate(self.tank_image, 0)     
        self.image_clean = self.image.copy()  
        self.rect = self.image.get_rect()   
        self.x_pos = 0
        self.y_pos = 0
        self.old_x = x
        self.old_y = y
        self.ang = random.randint(0, 3) * 90
        self.vel = 0   
        self.last_not_colliding = [self.old_x, self.old_y]
        self.disconnected = False
        self.encoded_changes = {}
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.tank_id = tank_id
        self.hit_by = None
        self.level_spot = level_spot
        self.num_bullets = 5
        self.can_move = True
        self.explode_ticks = None
        self.dying = False
        self.points = 0    
        self.username = username
        download_audio(self.username) 
        self.play_death_sound_step = None
        self.visible = True

    # Network multiplayer stuff
    def parse_changes(self, encoded_changes):
        for key, value in encoded_changes.items():
            print("{}, {}".format(key, value))

    # Change tank moving speed
    def speed(self, keys):
        if self.tank_id == 0:
            if keys[pygame.K_w]:
                self.vel = 6
            elif keys[pygame.K_s]:
                self.vel = -4
            else:
                if not self.vel:
                    return
                self.vel = 0
        elif self.tank_id == 1:
            if keys[pygame.K_UP]:
                self.vel = 6
            elif keys[pygame.K_DOWN]:
                self.vel = -4
            else:
                if not self.vel:
                    return
                self.vel = 0
        self.encoded_changes["vel"] = self.vel
    
    # Change tank direction
    def turn(self, keys):
        if self.tank_id == 0:
            if keys[pygame.K_a]:
                self.ang += 9
            elif keys[pygame.K_d]:
                self.ang -= 9     
        elif self.tank_id == 1:
            if keys[pygame.K_LEFT]:
                self.ang += 9
            elif keys[pygame.K_RIGHT]:
                self.ang -= 9    
        self.encoded_changes["ang"] = self.ang

    # Move player to new position and update afterwards
    def move(self, walls_list, bullets_list):
        if not self.hit_by == None:
            return self.update(walls_list, bullets_list)
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

        return self.update(walls_list, bullets_list)

    # Fire a new bullet
    def shoot(self):
        if self.dying:
            return
        # Only fire if player has not fired all rounds
        elif self.num_bullets > 0 and self.hit_by == None:
            self.num_bullets -= 1
            bullet = Bullet(self.rect.centerx + cos(self.ang*pi/180) * 15, self.rect.centery - + sin(self.ang*pi/180) * 15, self.ang, self.tank_id)
            return bullet       
        else:
            return None

    def explode(self):       
        to_return = None
        if self.dying == False:
            self.play_death_sound_step = "play_jeg_tror_såmænd"
        if self.play_death_sound_step != None:
            # hee_hee.play()
            to_return = self.play_death_sound()
            
        self.dying = True 
        if self.anim_count == 0:
            self.image = self.explode_frames[0]
            self.anim_count += 1
            self.explode_ticks = pygame.time.get_ticks()            
        elif pygame.time.get_ticks() - self.explode_ticks > 50 and self.anim_count < len(self.explode_frames):
            if self.anim_count >= self.frames -1:
                self.visible = False
                self.hit_by = None
            else:
                self.explode_ticks = pygame.time.get_ticks()
                self.image = self.explode_frames[self.anim_count]  
                self.anim_count += 1        
        self.rect = self.image.get_rect()     
        self.rect.centerx = self.old_x     
        self.rect.centery = self.old_y     
        return to_return

    # Update pos if not hitting a wall or hit by bullet
    def update(self, walls_list, bullets_list):
        # Check if hit by a bullet
        if self.hit_by != None or self.play_death_sound_step != None:
            return self.explode()
            
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def play_death_sound(self):
        if self.play_death_sound_step == "play_jeg_tror_såmænd":
            self.play_death_sound_step = "play_jeg_tror_såmænd_done"
            pygame.mixer.music.load('sounds/jeg_tror_såmænd.wav')
            pygame.mixer.music.set_endevent( pygame.USEREVENT )
            pygame.mixer.music.play(0)
            return {"tank_id": self.tank_id, "next_step": "play_username"}
        elif self.play_death_sound_step == "play_username":
            self.play_death_sound_step = "play_username_done"
            pygame.mixer.music.load('sounds/usernames/' + str(self.username) + '.mp3')
            pygame.mixer.music.set_endevent( pygame.USEREVENT )
            pygame.mixer.music.play(0)
            return {"tank_id": self.tank_id, "next_step": "play_faktisk_lige_er_død"}
        elif self.play_death_sound_step == "play_faktisk_lige_er_død":
            faktisk_lige_er_død.play(0)
            self.play_death_sound_step = None
            self.kill()
            return None
            