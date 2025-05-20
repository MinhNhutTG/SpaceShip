import time
import pygame
import os
from dotenv import load_dotenv
from layer_class  import Button
from GameManager import GameManager

load_dotenv()

WIDTH = int(os.getenv("WIDTH_SCREEN"))
HEIGHT = int(os.getenv("HEIGHT_SCREEN"))

# pygame setup
pygame.init()
game_manager = GameManager()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.mixer.music.load("Asset/theme.mp3")
pygame.mixer.music.play(-1)

def menu():
    background = pygame.image.load("Asset\\bg_game_start.png")
    btn_play = Button((WIDTH / 2 - 120, HEIGHT / 2 - 200), (200, 60), "Play")
    btn_Quit = Button((WIDTH / 2 - 120, HEIGHT / 2 - 100 ), (200, 60), "Exit")
    run_menu = True
    while run_menu:
        screen.blit(background, (0, 0))

        btn_play.draw(screen)
        btn_Quit.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            if btn_play.is_clicked(event,screen):
                main_game()
                print("Start game")
            if btn_Quit.is_clicked(event,screen):
                run_menu = False
                print("Quit")
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 6


def main_game():

    background = game_manager.load_map()

    run_menu = True
    time.sleep(1)
    pygame.mixer.music.stop()
    while run_menu:
        screen.fill("purple")
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False

        pygame.display.flip()
        clock.tick(60)
menu()