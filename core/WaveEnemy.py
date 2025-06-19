import pygame
import math
from core.Enemy import EnemyShip

class WaveEnemyShip(EnemyShip):
    def __init__(self, position, amplitude=30, speed=100, wave_speed=2, screen_size=(1000, 700)):
        # Enemy type 1 tương ứng với enemyship_level2.png
        super().__init__(position, enemy_type=1, screen_size=screen_size)
        self.amplitude = amplitude
        self.speed = speed
        self.wave_speed = wave_speed
        self.base_y = position[1]
        self.start_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        dt = (now - self.last_update) / 1000.0
        self.last_update = now

        t = (now - self.start_time) / 1000.0
        self.rect.x += int(self.speed * dt)
        self.rect.y = int(self.base_y + self.amplitude * math.sin(self.wave_speed * t))

        if self.rect.x > self.screen_width + 50:
            self.kill()
