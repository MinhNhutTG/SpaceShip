import pygame
import os
from dotenv import load_dotenv
from core.scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from core.enemy_asset import init_enemy_assets

load_dotenv()

WIDTH = int(os.getenv("WIDTH_SCREEN"))
HEIGHT = int(os.getenv("HEIGHT_SCREEN"))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
init_enemy_assets()  # ✅ Gọi sau khi có screen
clock = pygame.time.Clock()
running = True
scene_manager = SceneManager(MenuScene(manager=None))
scene_manager.current_scene.manager = scene_manager

def main():

    while running:
        dt = clock.tick(60) / 1000.0  # 60 FPS
        scene_manager.current_scene.handle_events(pygame.event.get(),screen)
        scene_manager.current_scene.update(screen,dt)
        scene_manager.current_scene.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
