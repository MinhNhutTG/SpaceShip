import pygame
import os
from dotenv import load_dotenv

mapImage = [
    "Asset/Maps/level1.png",
    "Asset/Maps/level2.png",
    "Asset/Maps/level3.png"
]
class GameManager:
    def __init__(self):
        self.current_level = os.getenv("LEVEL")
        self.max_current_level = 5
    def load_map(self):
        return pygame.image.load("Asset/Maps/level" + str(self.current_level) + ".png")
