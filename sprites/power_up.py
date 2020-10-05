import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    # Setup
    def __init__(self, x, y, level_spot):
        super().__init__()        
        self.image = pygame.Surface((10, 10))
        self.type = random.randint(0,1)
        self.types = {0: "bomb", 1: "railgun"}
        self.color = (200,200,200)
        if self.types[self.type] == "bomb":
            self.color = (200,0,200)
        if self.types[self.type] == "railgun":
            self.color = (0,200,200)
        print(self.color)

        self.image.fill(self.color)
        self.rect = self.image.get_rect()   
        self.rect.centerx = x
        self.rect.centery = y
        self.level_spot = level_spot
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    # Draw power up
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)