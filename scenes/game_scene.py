from logging import Manager

import pygame

from core.Music import Music
from core.scene import Scene
from core.player import Spaceship
from GameManager import GameManager


class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.background = pygame.image.load("Asset/Maps/level2.png")
        self.font = pygame.font.SysFont("Arial", 30)
        self.spaceship = Spaceship( 300 // 2, 300 - 100, "Asset/player/player.png")

        # vị trí bắt đầu
        Music.play_sound_main()
        Music.music_play()

    def handle_events(self, events,screen):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.spaceship.move(keys)

    def render(self, screen):
        screen.fill((0, 0, 50))
        screen.blit(self.background, (0, 0))
        self.spaceship.draw(screen)
