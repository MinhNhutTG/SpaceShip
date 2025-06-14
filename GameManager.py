import pygame
import os
from dotenv import load_dotenv

mapImage = [
    "Asset/Maps/level1.png",
    "Asset/Maps/level2.jpg",
    "Asset/Maps/level2.png",
    "Asset/Maps/level3.png"
]
class GameManager:
    def __init__(self):
        self.current_level = int(os.getenv("LEVEL"))
        self.max_current_level = 5
        self.point = 120

    def next_level(self):
        print("Next level")
        self.current_level += 1
        self.point*=self.current_level



    def load_map(self):
        print("Loading map "+ str(self.current_level))

        return pygame.image.load("Asset/Maps/level" + str(self.current_level) + ".png")

    def update_level_env(self):
        with open(".env", "r") as file:
            lines = file.readlines()

        with open(".env", "w") as file:
            for line in lines:
                if line.startswith("LEVEL="):
                    file.write(f"LEVEL={str(self.current_level)}\n")
                else:
                    file.write(line)