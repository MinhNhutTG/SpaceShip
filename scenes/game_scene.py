import pygame
import os
from core.Music import Music
from core.scene import Scene
from core.player import Spaceship
from dotenv import load_dotenv
from PopupMessage import PopupMessage
from GameManager import GameManager
from core.Enemy import EnemyShip
from core.HUD import HUD

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
        self.spaceship = Spaceship( (WIDTH_SCREEN / 2, HEIGHT_SCREEN * 3/4 ))
        self.enemies = pygame.sprite.Group()


        rows = 2
        columns = 9
        spacing_x = 80
        spacing_y = 60
        offset_x = 100
        offset_y = 30

        for row in range(rows):
            for col in range(columns):

                enemy_type = (col % 3) + 1
                enemy = EnemyShip(WIDTH_SCREEN, HEIGHT_SCREEN, enemy_type=enemy_type ,custom_position=True)
                enemy.rect.x = offset_x + col * spacing_x
                enemy.rect.y = offset_y + row * spacing_y
                print(type(enemy))
                self.enemies.add(enemy)

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

    def handle_collisions(self):
        hits = pygame.sprite.spritecollide(self.spaceship, self.enemies, True)
        if hits:
            self.spaceship.kill()
            self.spaceship.kill_score(10)
            self.spaceship.take_hidden()



    def update(self):
        if self.spaceship.lives > 0:
            keys = pygame.key.get_pressed()
            self.spaceship.move(keys)
            self.spaceship.update()

            for bullet in self.spaceship.bullets:
                bullet.update()

            self.enemies.update()

            self.handle_collisions()





    def render(self, screen):
        if self.paused:
            screen.blit(self.background, (0,0))
            screen.fill((0, 0, 50))
            screen.blit(self.background, (0, 0))
            self.spaceship.draw(screen)

            for bullet in self.spaceship.bullets:
                bullet.draw(screen)
            self.enemies.draw(screen)

        else :
            notification = PopupMessage((WIDTH_SCREEN * 2/8, HEIGHT_SCREEN / 2 ), "GAME PAUSE " , submessage="Press ESC To Continue")
            notification.show()
            notification.draw(screen)


