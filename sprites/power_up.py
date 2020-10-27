import pygame
import random


def get_type(power_up_type):
    # types = {0: {"type": "normal", "num_bullets": 1, "bullet_lifespan": 500, "bullet_refill": True, "bullets_rpm": False, "bullets_timer": None, "bullets_spread": 0, "bullet_size": 4}, 1: {"type": "bomb", "num_bullets": 1, "bullet_lifespan": 5000, "bullet_refill": False,
    types = {
        0: {
            "type": "normal",
            "num_bullets": 1,
            "num_bullets_destroyed": 0,
            "can_take_new": True,
            "max_bullets": 1,
            "bullet_lifespan": 2000,
            "bullet_refill": True,
            "bullet_size": 4,
            "bullet_speed": 6,
            "bullets_rpm": False,
            "bullets_timer": None,
            "bullets_spread": 0,
            "fragments": 0,
            "should_explode": 1,
        },
        1: {
            "type": "bomb",
            "num_bullets": 1,
            "num_bullets_destroyed": 0,
            "can_take_new": False,
            "max_bullets": 1,
            "bullet_lifespan": 5000,
            "bullet_refill": False,
            "bullet_size": 8,
            "bullet_speed": 4,
            "bullets_rpm": False,
            "bullets_timer": None,
            "bullets_spread": 0,
            "fragments": 30,
            "should_explode": 2,
        },
        2: {
            "type": "minigun",
            "num_bullets": 10,
            "num_bullets_destroyed": 0,
            "can_take_new": False,
            "max_bullets": 10,
            "bullet_spread": 10,
            "bullet_lifespan": 3000,
            "bullet_refill": False,
            "bullet_size": 2,
            "bullet_speed": 7,
            "bullets_rpm": 400,
            "bullets_timer": None,
            "bullets_spread": 2,
            "fragments": 0,
            "should_explode": 1,
        },
        3: {
            "type": "fragment",
            "num_bullets": 1,
            "num_bullets_destroyed": 0,
            "max_bullets": 1,
            "bullet_spread": 360,
            "bullet_lifespan": 10000,
            "bullet_refill": False,
            "bullet_size": 5,
            "bullet_speed": 4,
            "bullets_rpm": 400,
            "bullets_timer": None,
            "bullets_spread": 360,
            "fragments": 0,
            "should_explode": 1,
        }
    }
    if power_up_type == "all":
        return types
    return types[power_up_type]


class PowerUp(pygame.sprite.Sprite):
    # Setup
    def __init__(self, x, y, level_spot):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.type = random.randint(1, 2)

        self.color = (200, 200, 200)
        if get_type(self.type)["type"] == "bomb":
            self.color = (200, 0, 200)
        if get_type(self.type)["type"] == "minigun":
            self.color = (0, 200, 200)        

        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.level_spot = level_spot
        self.types = get_type("all")
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    # Draw power up
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
