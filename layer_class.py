import threading

import pygame
import time


btn_Play = ["Asset/btnPlay.png","Asset/Play_Click.png"]
btn_Quit = ["Asset/btnExit.png","Asset/Exit_Click.png"]

class Button:
    def __init__(self, position ,size,type_button):
        self.rect = pygame.Rect(position,size)
        self.type_button = type_button
        self.sound_click = pygame.mixer.Sound("Asset/click.mp3")
        if type_button == "Play":
            self.image = pygame.image.load(btn_Play[0])
            self.image = pygame.transform.scale(self.image, self.rect.size)
        if type_button == "Exit":
            self.image = pygame.image.load(btn_Quit[0])
            self.image = pygame.transform.scale(self.image, self.rect.size)

        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface) :
        pygame.draw.rect(surface, (255,255,255,0),self.rect ,border_radius=8) # vẽ bề mặt
        surface.blit(self.image, self.rect)     # vẽ ảnh lên bề mat nut

    def is_clicked(self ,event,surface) :
        image_click = None
        if self.type_button == "Play":
            image_click = pygame.image.load(btn_Play[1])
        elif self.type_button == "Exit":
            image_click = pygame.image.load(btn_Quit[1])
        image_click = pygame.transform.scale(image_click, self.rect.size)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.type_button == "Play":
                threading.Thread(target=self.animation_click(surface,image_click)).start()

                return True
            if self.rect.collidepoint(event.pos) and self.type_button == "Exit":
                threading.Thread(target=self.animation_click(surface,image_click)).start()

                return True
        return False
    def animation_click(self,surface ,image_click):
        surface.blit(image_click, self.rect)
        self.sound_click.play()
        pygame.display.update()