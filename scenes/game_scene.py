import pygame
from GameManager import GameManager
from core.scene import Scene

game_manager = GameManager()
class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = game_manager.load_map()

    def render(self, screen):
        screen.blit(self.background, (0, 0))
