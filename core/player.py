import pygame
import math
from core.Bullet import Bullet
from core.HUD import HUD
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("Asset/sound/sound_bullet.mp3")
shoot_sound.set_volume(0.1)

Images=["Asset/player/player.png"]

HUD.init(font_size=25)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        x, y = position
        self.position_x = x
        self.position_y = y
        self.original_image = pygame.image.load(Images[0]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.time_last_shot = 0
        self.time_cooldown = 500
        self.bullets = []
        self.hidden = False
        self.hidden_start_time = 0
        self.hidden_duration = 700
        self.lives = 3
        self.score = 0
        self.bullets_group = pygame.sprite.Group()


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
        if not self.hidden:
            time_current = pygame.time.get_ticks()
            if time_current - self.time_last_shot > self.time_cooldown:
                self.time_last_shot = time_current
                bullet =  Bullet(self.rect.centerx -10, self.rect.top,color=(255, 0, 0))
                self.bullets.append(bullet)
                self.bullets_group.add(bullet)
                shoot_sound.play()

        return 0

    def draw(self, surface):
        if not self.hidden:
            surface.blit(self.image, self.rect)
        HUD.draw(surface, self.lives, self.score)


    def take_hidden(self):
        """Kích hoạt trạng thái ẩn (miễn thương) trong 2 giây."""
        self.hidden = True
        self.hidden_start_time = pygame.time.get_ticks()

    def update(self):
        """Cập nhật trạng thái ẩn nếu đang hoạt động."""
        if self.hidden:
            now = pygame.time.get_ticks()
            if now - self.hidden_start_time >= self.hidden_duration:
                self.hidden = False
            HUD.update(self.score, self.lives)

    def kill(self):
        if not self.hidden:
            self.lives -= 1

    def kill_score(self, score):
        if not self.hidden:
            self.score += score