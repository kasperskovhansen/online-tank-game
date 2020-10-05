import pygame

class PowerUp(pygame.sprite.Sprite):
    # Setup
    def __init__(self, x, y, level_spot):
        super().__init__()        
        self.image = pygame.Surface((10, 10))
        self.image.fill((200,200,200))
        self.rect = self.image.get_rect()   
        self.rect.centerx = x
        self.rect.centery = y
        self.level_spot = level_spot
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    # Draw power up
    def draw(self,screen):
        pygame.draw.rect(screen, (200,200,200), self.rect)