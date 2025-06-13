import pygame
pygame.init()
class HUD:
    font = None

    @staticmethod
    def init(font_size=30):
        """Khởi tạo font và các thiết lập cần thiết."""
        HUD.font =  pygame.font.Font("Asset/font/Press_Start_2P/PressStart2P-Regular.ttf", 25)

    @staticmethod
    def update(score=None, lives=None,level=None):
        """Cập nhật thông tin điểm và mạng."""
        if score is not None:
            HUD.score = score
        if lives is not None:
            HUD.lives = lives
        if level is not None:
            HUD.level = level

    @staticmethod
    def draw(screen,lives,score,level):
        """Vẽ HUD lên màn hình."""
        if HUD.font is None:
            raise ValueError("HUD not initialized. Call HUD.init() first.")

        score_text = HUD.font.render(f"Score: " + str(score), True, (255, 255, 255))
        lives_text = HUD.font.render(f"Lives: " + str(lives), True, (255, 0, 0))
        level_text = HUD.font.render(f"Level: " + str(level), True, (255, 0, 0))

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(level_text, (10, 70))
