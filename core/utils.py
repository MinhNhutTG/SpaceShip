# utils.py
import pygame

#load anh no
# def load_explosion_frames():
#     explosion_frames = []
#     for i in range(1, 7):
#         image = pygame.image.load(f"Asset/explosion/explosion{i}.png").convert_alpha()
#         image = pygame.transform.scale(image, (50, 50))
#         explosion_frames.append(image)
#     return explosion_frames
def load_explosion_frames():
    frames = []
    for i in range(1, 7):
        try:
            image = pygame.image.load(f"Asset/explosion/explosion{i}.png").convert_alpha()
            image = pygame.transform.scale(image, (50, 50))
            frames.append(image)
        except Exception as e:
            print(f"❌ Lỗi load explosion{i}.png:", e)
    return frames
