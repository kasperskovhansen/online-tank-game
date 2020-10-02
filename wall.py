import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()        
        self.image = pygame.Surface((w, h))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()   
        self.rect.left = x
        self.rect.top = y        