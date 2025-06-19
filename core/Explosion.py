import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, frames, frame_rate=25): # chỉnh thời gian load mỗi frame
        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=position)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate  # mili giây giữa các frame

    def update(self):
        print(f"🌀 Explosion frame {self.index} đang update")  # THÊM LOG
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.frames):
                print("🔥 Explosion kết thúc")  # Xác nhận xong
                self.kill()
            else:
                self.image = self.frames[self.index]
