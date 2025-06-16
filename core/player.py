import pygame
import math
from core.Bullet import Bullet
from core.HUD import HUD
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("Asset/sound/sound_bullet.mp3")
shoot_sound.set_volume(0.1)

Images=["Asset/player/player.png"]
TypeBullet = ["type1","type2","type3","type4"]

HUD.init(font_size=25)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        x, y = position
        self.position_x = x
        self.position_y = y
        self.original_image = pygame.image.load(Images[0]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.time_last_shot = 0
        self.time_cooldown = 500
        self.type_bullet = TypeBullet[0]
        self.type_bullet_previous = TypeBullet[0]
        self.has_special_bullet = False
        self.bullets = []
        self.hidden = False
        self.hidden_start_time = 0
        self.hidden_duration = 700
        self.lives = 3
        self.score = 0
        self.level = None
        self.bullets_group = pygame.sprite.Group()



    def move(self, keys):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        # Chuẩn hóa nếu đang di chuyển theo đường chéo
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx = dx / length
            dy = dy / length

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Giới hạn di chuyển của phi thuyền trong khung hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 700:
            self.rect.bottom = 700



    def shoot(self):
        print("Loai dan dang ban la "+ str(self.type_bullet))
        if not self.hidden:
            time_current = pygame.time.get_ticks()
            if time_current - self.time_last_shot > self.time_cooldown:
                self.time_last_shot = time_current
                if not self.has_special_bullet :
                    if self.type_bullet == "type1":
                        self.shoot_level_1()
                    elif self.type_bullet == "type2":
                        self.shoot_level_2()
                    elif self.type_bullet == "type3" :
                        self.shoot_level_3()
                else :

                    self.type_bullet = "type4"
                    self.shoot_level_4()

                shoot_sound.play()
        return 0

    def shoot_level_1(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, type_bullet=TypeBullet[0])
        self.add_bullet(bullet)

    def shoot_level_2(self):
        for i in range(3):
            bullet = Bullet(self.rect.centerx, self.rect.top, type_bullet=TypeBullet[1], offset_index=i)
            self.add_bullet(bullet)

    def shoot_level_3(self):
        offsets = [-30, 0, 30]
        for dx in offsets:
            bullet = Bullet(self.rect.centerx + dx, self.rect.top, type_bullet=TypeBullet[2], angle=0)
            self.add_bullet(bullet)

    def shoot_level_4(self):

        angles = [-30, -15, 0, 15, 30]
        for angle in angles:
            bullet = Bullet(self.rect.centerx, self.rect.top, type_bullet=TypeBullet[3], angle=angle)
            self.add_bullet(bullet)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)
        self.bullets_group.add(bullet)

    def draw(self, surface):
        if not self.hidden:
            surface.blit(self.image, self.rect)
        HUD.draw(surface, self.lives, self.score,self.level)


    def take_hidden(self):
        """Kích hoạt trạng thái ẩn (miễn thương) trong 2 giây."""
        self.hidden = True
        self.hidden_start_time = pygame.time.get_ticks()

    def update(self):

        if self.hidden and pygame.time.get_ticks() - self.hidden_start_time >= self.hidden_duration:
            self.hidden = False

        self.bullets_group.update()

        screen_height = 700
        self.bullets = [b for b in self.bullets if not b.is_off_screen(screen_height)]

        for bullet in self.bullets_group.copy():
            if bullet.is_off_screen(screen_height):
                self.bullets_group.remove(bullet)

        HUD.update(self.score, self.lives, self.level)



    def kill(self):
        if not self.hidden:
            self.lives -= 1

    def kill_score(self, score):
        if not self.hidden:
            self.score += score
    def heal(self):
        if self.lives < 5:
            self.lives +=1

