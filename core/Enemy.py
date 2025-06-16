import pygame
import random

# explosion_image = pygame.image.load("Asset/effect/explosion.png")
# explosion_image = pygame.transform.scale(explosion_image, (50, 50))
# explosion_sound = pygame.mixer.Sound("Asset/sound/explosion.wav")
# explosion_sound.set_volume(0.2)

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, enemy_type=1, custom_position=False):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_type = enemy_type
        self.image = self.load_image(enemy_type)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()


        if not custom_position:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)

        # Gán tốc độ di chuyển
        self.set_speed(enemy_type)

    def load_image(self, enemy_type):
        """Chọn ảnh cho enemy theo loại"""
        if enemy_type == 1:
            return pygame.image.load("Asset/enemy/enemyship_level4.png")
        elif enemy_type == 2:
            return pygame.image.load("Asset/enemy/enemyship_level2.png")
        elif enemy_type == 3:
            return pygame.image.load("Asset/enemy/enemyship_level5.png")
        else:
            # Nếu loại không hợp lệ, tạo hình màu đỏ thay thế
            temp_image = pygame.Surface((50, 50))
            temp_image.fill((255, 0, 0))
            return temp_image

    def set_speed(self, enemy_type):
        """Thiết lập tốc độ dựa vào loại enemy"""
        if enemy_type == 1:
            self.speed_x = random.choice([-1, 1])  # di chuyển trái/phải
            self.speed_y = random.randint(1, 2)    # di chuyển xuống
        elif enemy_type == 2:
            self.speed_x = random.choice([-2, -1, 1, 2])
            self.speed_y = random.randint(2, 3)
        elif enemy_type == 3:
            self.speed_x = random.choice([-3, -2, 2, 3])
            self.speed_y = random.randint(3, 4)
        else:
            self.speed_x = 0
            self.speed_y = 1

    def update(self):
        """Cập nhật vị trí tàu địch mỗi khung hình"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Nếu chạm biên trái/phải thì quay đầu
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1

        # Nếu vượt khỏi màn hình dưới thì đặt lại từ trên
        if self.rect.top > self.screen_height:
            self.reset_position()


    def reset_position(self):
        """Đặt lại vị trí và tốc độ khi enemy đi khỏi màn hình"""
        self.rect.x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.set_speed(self.enemy_type)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

