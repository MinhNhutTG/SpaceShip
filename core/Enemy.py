import pygame
import random
from core.EnemyBullet import EnemyBullet

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, pos_x, pos_y, enemy_type , bullet_group):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_type = enemy_type
        self.bullet_group =bullet_group
        self.enemy_bullets = pygame.sprite.Group()
        self.shoot_delay = 2000  # milliseconds
        self.last_shot = pygame.time.get_ticks()

        self.original_image = self.loadImage()
        self.image = pygame.transform.scale(self.original_image, (70, 70))
        self.rect = self.image.get_rect()

        # Vị trí khởi tạo
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.rect_y = float(self.rect.y)

        # Vận tốc chỉ theo trục dọc
        self.speed_y = 100  # tốc độ rơi dọc (pixel/s)
        self.last_update = pygame.time.get_ticks()

        self.exploded = False
        self.explosion_image = pygame.image.load("Asset/enemy/explosion.png").convert_alpha()
        self.explosion_sound = pygame.mixer.Sound("Asset/sound/reward.mp3")
        self.explosion_duration = 300  # milliseconds
        self.explosion_start_time = None

    def loadImage(self):
        path = ""
        if self.enemy_type == "type1":
            path = "Asset/enemy/enemyship_level2.png"
        elif self.enemy_type == "type2":
            path = "Asset/enemy/enemyship_level3.png"
        elif self.enemy_type == "type3":
            path = "Asset/enemy/enemyship_level4.png"
        elif self.enemy_type == "type4":
            path = "Asset/enemy/enemyship_level5.png"
        return pygame.image.load(path).convert_alpha()

    def update(self):
        now = pygame.time.get_ticks()
        dt = (now - self.last_update) / 1000.0
        self.last_update = now

        if not self.exploded:
            self.shoot(now)

        if self.exploded:
            if now - self.explosion_start_time >= self.explosion_duration:
                self.kill()  # Xóa khỏi sprite group
            return  # không di chuyển nữa

        # Di chuyển xuống dưới
        self.rect_y += self.speed_y * dt
        self.rect.y = int(self.rect_y)

        # Nếu rơi khỏi màn hình, reset vị trí
        if self.rect.top > self.screen_height:
            self.kill()
            print("Da huy enemy")





    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.enemy_bullets.draw(surface)

    def explode(self):
        self.exploded = True
        self.explosion_start_time = pygame.time.get_ticks()
        self.explosion_sound.play()
        self.image = pygame.transform.scale(self.explosion_image, (50, 50))

    def shoot(self, now):
        if now - self.last_shot >= self.shoot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullet_group.add(bullet)
            self.last_shot = now