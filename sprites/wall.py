import pygame

class Wall(pygame.sprite.Sprite):
    # Setup
    def __init__(self, x, y, w, h):
        super().__init__()        
        self.image = pygame.Surface((w, h))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()   
        self.rect.left = x
        self.rect.top = y
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    # Draw wall
    def draw(self,screen):
        pygame.draw.rect(screen, (200,200,200), self.rect)