import threading
import time
from enum import nonmember

import pygame
import os

image = ""

class PopupMessage:
    def __init__(self, position , message,size = (500,100) , duration=2000 , submessage = None):
        self.position = position
        self.rect = pygame.Rect(self.position,size)
        self.color =  (61,144,215)
        self.duration = duration
        self.start_time = None
        self.expired = True
        self.message = message
        self.sub_message = submessage
        self.font = pygame.font.Font("Asset/font/Press_Start_2P/PressStart2P-Regular.ttf", 25)
        self.font_sub = pygame.font.Font("Asset/font/Press_Start_2P/PressStart2P-Regular.ttf", 20)

    def show(self):
        self.start_time = pygame.time.get_ticks()

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < self.duration:
            # Vẽ popup
            pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, width=2, border_radius=8)

            # Render dòng chính
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 20))

            # Render dòng phụ
            text_surface_sub = self.font_sub.render(self.sub_message, True, (255, 255, 255))
            text_rect_sub = text_surface_sub.get_rect(center=(self.rect.centerx, text_rect.bottom + 20))

            # Vẽ chữ
            surface.blit(text_surface, text_rect)
            surface.blit(text_surface_sub, text_rect_sub)
        else:
            self.expired = False

