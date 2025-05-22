# import pygame
# import os
# from dotenv import load_dotenv
# from UI.Button import Button
# from GameManager import GameManager
# from PopupMessage import PopupMessage
# from Music import Music
#
# load_dotenv()
#
# WIDTH = int(os.getenv("WIDTH_SCREEN"))
# HEIGHT = int(os.getenv("HEIGHT_SCREEN"))
#
# # pygame setup
# pygame.init()
# game_manager = GameManager()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()
# running = True
#
#
# def menu():
#     Music.play_sound_intro()
#     background = pygame.image.load("Asset\\bg_game_start.png")
#     btn_play = Button((WIDTH / 2 - 120, HEIGHT / 2 - 200), (200, 60), "Play")
#     btn_quit = Button((WIDTH / 2 - 120, HEIGHT / 2 - 100 ), (200, 60), "Exit")
#     run_menu = True
#     while run_menu:
#         screen.blit(background, (0, 0))
#
#         btn_play.draw(screen)
#         btn_quit.draw(screen)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run_menu = False
#             if btn_play.is_clicked(event,screen):
#                 Music.music_stop()
#                 main_game()
#                 print("Start game")
#
#             if btn_quit.is_clicked(event,screen):
#                 run_menu = False
#                 print("Quit")
#         pygame.display.flip()
#         clock.tick(60)  # limits FPS to 6
#
#
# def main_game():
#     Music.play_sound_main()
#     background = game_manager.load_map()
#     popup = PopupMessage((200, 100),message="Level 1")
#     popup.show()
#     run_menu = True
#
#     while run_menu:
#         screen.fill("purple")
#         screen.blit(background, (0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run_menu = False
#
#
#         popup.draw(screen)
#
#         pygame.display.flip()
#         clock.tick(60)
#
#
# menu()