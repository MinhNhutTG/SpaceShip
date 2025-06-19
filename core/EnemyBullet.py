import pygame
import os
from dotenv import load_dotenv
load_dotenv()


WIDTH_SCREEN = int(os.getenv("WIDTH_SCREEN"))
HEIGHT_SCREEN = int(os.getenv("HEIGHT_SCREEN"))

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))  # Màu đỏ
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = 700  # tốc độ bắn xuống (pixel/s)

    def update(self, dt):
        self.rect.y += int(self.speed_y * dt)
        if self.rect.top > HEIGHT_SCREEN:  # Nếu vượt quá màn hình (có thể điều chỉnh theo chiều cao thật)
            self.kill()