import pygame
import os
from dotenv import load_dotenv
from core.Music import Music
from core.scene import Scene
from UI.Button import Button


load_dotenv()

WIDTH = int(os.getenv("WIDTH_SCREEN"))
HEIGHT= int(os.getenv("HEIGHT_SCREEN"))

class MenuScene(Scene):
    def __init__(self,manager):
        super().__init__(manager)
        self.background = pygame.image.load("Asset\\bg_game_start.png")
        self.btn_play = Button((WIDTH / 2 - 120, HEIGHT / 2 - 200), (200, 60), "Play")
        self.btn_quit = Button((WIDTH / 2 - 120, HEIGHT / 2 - 100 ), (200, 60), "Exit")

        Music.play_sound_intro()
        Music.music_play()

    def handle_events(self, events, screen):
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            if self.btn_play.is_clicked(event ,screen):
                print("hello")
            if self.btn_quit.is_clicked(event ,screen):
                print("bye")

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        self.btn_play.draw(screen)
        self.btn_quit.draw(screen)