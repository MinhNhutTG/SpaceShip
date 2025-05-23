import pygame
import os
from core.Music import Music
from core.scene import Scene
from core.player import Spaceship
from dotenv import load_dotenv
from PopupMessage import PopupMessage
from GameManager import GameManager
from core.Bullet import Bullet


load_dotenv()
game_manager = GameManager()

WIDTH_SCREEN = int(os.getenv("WIDTH_SCREEN"))
HEIGHT_SCREEN = int(os.getenv("HEIGHT_SCREEN"))

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.paused = True
        self.background = game_manager.load_map()
        self.font = pygame.font.SysFont("Arial", 30)
        self.spaceship = Spaceship( (WIDTH_SCREEN / 2, HEIGHT_SCREEN * 3/4 ), "Asset/player/player.png")



        # vị trí bắt đầu
        Music.play_sound_main()
        Music.music_play()

    def handle_events(self, events,screen):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.paused:
                    self.spaceship.shoot()
                if event.key == pygame.K_ESCAPE:
                    if self.paused is True:
                        self.paused = False
                    else:
                        self.paused = True



    def update(self):
        keys = pygame.key.get_pressed()
        self.spaceship.move(keys)

        for bullet in self.spaceship.bullets:
            bullet.update()


    def render(self, screen):
        if self.paused:
            screen.blit(self.background, (0,0))
            screen.fill((0, 0, 50))
            screen.blit(self.background, (0, 0))
            self.spaceship.draw(screen)

            for bullet in self.spaceship.bullets:
                bullet.draw(screen)

        else :
            notification = PopupMessage((WIDTH_SCREEN * 2/8, HEIGHT_SCREEN / 2 ), "GAME PAUSE " , submessage="Press ESC To Continue")
            notification.show()
            notification.draw(screen)


