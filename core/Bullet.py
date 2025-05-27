import pygame

Bullet_Image = ["Asset/bullet/bullet.png"]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-10, color=(255, 255, 0), width=20, height=25):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color
        self.original_image = pygame.image.load(Bullet_Image[0]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width,height))



    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)




    def is_off_screen(self, screen_height):
        return self.rect.bottom < 0 or self.rect.top > screen_height
