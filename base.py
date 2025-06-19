import pygame
import os
from dotenv import load_dotenv
from core.scene_manager import SceneManager
from scenes.menu_scene import MenuScene

load_dotenv()

WIDTH = int(os.getenv("WIDTH_SCREEN"))
HEIGHT = int(os.getenv("HEIGHT_SCREEN"))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
scene_manager = SceneManager(MenuScene(manager=None))
scene_manager.current_scene.manager = scene_manager

def main():

    while running:
        dt = clock.tick(90) / 1000.0  # 60 FPS
        scene_manager.current_scene.handle_events(pygame.event.get(),screen)
        scene_manager.current_scene.update(screen,dt)
        scene_manager.current_scene.render(screen)
        pygame.display.flip()
        clock.tick(90)  # limits FPS to 6

if __name__ == '__main__':
    main()
