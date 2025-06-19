import pygame
import random
from core.EnemyBullet import EnemyBullet
import core.enemy_asset as enemy_asset  # ✅ import theo module để dùng biến toàn cục

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, pos_x, pos_y, enemy_type, bullet_group):
        super().__init__()

        self.image = enemy_asset.ENEMY_IMAGES[enemy_type]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.rect_y = float(self.rect.y)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_type = enemy_type
        self.bullet_group = bullet_group
        self.enemy_bullets = pygame.sprite.Group()

        self.shoot_delay = random.randint(2000, 4000)
        self.last_shot = pygame.time.get_ticks()
        self.speed_y = 100
        self.last_update = pygame.time.get_ticks()

        self.exploded = False
        self.explosion_image = enemy_asset.EXPLOSION_IMAGE
        self.explosion_sound = enemy_asset.EXPLOSION_SOUND
        self.explosion_duration = 300
        self.explosion_start_time = None

    def update(self):
        now = pygame.time.get_ticks()
        dt = (now - self.last_update) / 1000.0
        self.last_update = now

        if not self.exploded:
            self.shoot(now)

        if self.exploded:
            if now - self.explosion_start_time >= self.explosion_duration:
                self.kill()
            return

        self.rect_y += self.speed_y * dt
        self.rect.y = int(self.rect_y)

        if self.rect.top > self.screen_height:
            self.kill()

    def shoot(self, now):
        if now - self.last_shot >= self.shoot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullet_group.add(bullet)
            self.last_shot = now

    def explode(self):
        self.exploded = True
        self.explosion_start_time = pygame.time.get_ticks()
        self.explosion_sound.play()
        self.image = self.explosion_image
