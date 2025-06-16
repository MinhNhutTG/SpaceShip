import pygame
import random

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, screen_width):
        super().__init__()
        self.type = item_type

        if self.type == "health":
            self.image = pygame.image.load("Asset/items/health.png")
        else:
            self.image = pygame.image.load("Asset/items/ammo.png")

        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height

        self.speed_y = random.randint(2, 3)
        self.speed_x = random.choice([-1, 0, 1])

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
