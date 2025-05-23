import pygame
import math
from core.Bullet import Bullet
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("Asset/sound/sound_bullet.mp3")
shoot_sound.set_volume(0.1)
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        x, y = position
        self.position_x = x
        self.position_y = y
        self.original_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.time_last_shot = 0
        self.time_cooldown = 500
        self.bullets = []


    def move(self, keys):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        # Chuẩn hóa nếu đang di chuyển theo đường chéo
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx = dx / length
            dy = dy / length

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Giới hạn di chuyển của phi thuyền trong khung hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 700:
            self.rect.bottom = 700
    def shoot(self ):
        time_current = pygame.time.get_ticks()
        if time_current - self.time_last_shot > self.time_cooldown:
            self.time_last_shot = time_current
            bullet =  Bullet(self.rect.centerx -10, self.rect.top,color=(255, 0, 0))
            self.bullets.append(bullet)
            shoot_sound.play()
            print("Ban")

    def draw(self, surface):
        surface.blit(self.image, self.rect)
