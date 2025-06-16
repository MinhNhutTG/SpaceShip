import pygame
import math

Bullet_Images = [
    "Asset/bullet/bullet.png",
    "Asset/bullet/bullet2.png",
    "Asset/bullet/bullet3.png",
    "Asset/bullet/bullet4.png"
]


type_to_index = {
    "type1": 0,
    "type2": 1,
    "type3": 2,
    "type4": 3
}

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type_bullet , angle=0, offset_index=0):
        super().__init__()
        self.angle = angle
        self.type = type_bullet


        # Load image
        image_index = type_to_index.get(type_bullet, 0)
        self.original_image = pygame.image.load(Bullet_Images[image_index]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (20, 25))
        self.rect = self.image.get_rect(center=(x, y))

        if self.type == "type1":
            self.dx = 0
            self.dy = -12 #toc do dan

        elif self.type == "type2":
            self.dx = 0
            self.dy = -3
            self.rect.y -= offset_index * 40

        elif self.type == "type3":
            self.dx = angle * 4
            self.dy = -6

        elif self.type == "type4":
            radians = math.radians(angle)
            self.dx = math.sin(radians) * 10
            self.dy = -math.cos(radians) * 10
            self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self, screen_height):
        return self.rect.bottom < 0 or self.rect.top > screen_height
