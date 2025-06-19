import pygame
import os
import math
from core.Music import Music
from core.scene import Scene
import random
from core.player import Spaceship
from dotenv import load_dotenv
from PopupMessage import PopupMessage
from GameManager import GameManager
from core.Enemy import EnemyShip
from core.HUD import HUD
import time
from core.item import Item

load_dotenv()
game_manager = GameManager()

WIDTH_SCREEN = int(os.getenv("WIDTH_SCREEN"))
HEIGHT_SCREEN = int(os.getenv("HEIGHT_SCREEN"))


class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.paused = True
        self.spawn_item = False
        self.game_over = False
        self.background = game_manager.load_map() # bị co kéo
        self.enemy_bullets_group = pygame.sprite.Group()
        self.font = pygame.font.SysFont("Arial", 30)
        self.spaceship = Spaceship( (WIDTH_SCREEN / 2, HEIGHT_SCREEN * 3/4 ))
        self.spaceship.level = game_manager.current_level
        self.enemies = pygame.sprite.Group()
        self.level_up = False
        self.level_upStartTime =  0
        self.level_up_duringTime = 6
        self.items = pygame.sprite.Group()
        self.turn_change_bullet = 0
        self.has_specical_bullet = False
        self.bullet_powerup_start = None
        self.bullet_powerup_duringTime = 5000
        self.bg_scroll = 0
        self.scroll_speed = 2
        self.last_formation_spawn_time = pygame.time.get_ticks()
        self.formation_spawn_interval = 3000  # 3 giây

        # vị trí bắt đầu
        Music.play_sound_main()
        Music.music_play()



    def handle_events(self, events,screen):
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_ESCAPE:

                        from scenes.menu_scene import MenuScene
                        self.manager.change_scene(MenuScene(self.manager))

                if event.key == pygame.K_SPACE and self.paused:
                  self.spaceship.shoot()
                if event.key == pygame.K_ESCAPE:
                    if self.paused is True:
                        self.paused = False
                    else:
                        self.paused = True

    def handle_collisions(self):
        # Va chạm giữa enemy và player
        hits = pygame.sprite.spritecollide(self.spaceship, self.enemies, False)
        for enemy in hits:
            if not enemy.exploded:
                enemy.explode()
                self.spaceship.kill()
                self.spaceship.take_hidden()

        # Va chạm giữa đạn và enemy
        hits2 = pygame.sprite.groupcollide(self.spaceship.bullets_group, self.enemies, True, False)
        if hits2:
            self.spaceship.kill_score(10)
            for bullet in hits2.keys():
                if bullet in self.spaceship.bullets:
                    self.spaceship.bullets.remove(bullet)
            for enemies in hits2.values():
                for enemy in enemies:
                    if not enemy.exploded:
                        enemy.explode()

                        # 20% rơi item
                        if random.random() < 0.2:
                            item_type = random.choice(["health", "ammo"])
                            item = Item(item_type, WIDTH_SCREEN)
                            item.rect.center = enemy.rect.center
                            self.items.add(item)

        # Nhặt item
        hit3 = pygame.sprite.spritecollide(self.spaceship, self.items, True)
        for item in hit3:
            if item.type == "health":
                self.spaceship.heal()
            elif item.type == "ammo":
                self.spaceship.type_bullet_previous = self.spaceship.type_bullet
                self.spaceship.has_special_bullet = True
                self.bullet_powerup_start = pygame.time.get_ticks()

        # Va chạm giữa đạn của người chơi và đạn của enemy
        hit_by_enemy_bullets = pygame.sprite.spritecollide(self.spaceship, self.enemy_bullets_group, True)
        for bullet in hit_by_enemy_bullets:
            self.spaceship.kill()
            self.spaceship.take_hidden()


        bullet_hits = pygame.sprite.groupcollide(
            self.spaceship.bullets_group,  # Đạn người chơi
            self.enemy_bullets_group,  # Đạn enemy
            True,  # Xoá đạn người chơi khi va chạm
            True  # Xoá đạn enemy khi va chạm
        )



    def update(self,screen,dt):
        if not self.paused:
            return  # Nếu bạn muốn dừng cập nhật mọi thứ khi pause, thì OK
        else:

            self.bg_scroll += self.scroll_speed
            if self.bg_scroll >= self.background.get_height():
                self.bg_scroll = 0 # Hoặc self.bg_scroll = 0 nếu muốn cuộn vòng lặp

        if self.spaceship.lives > 0:
            keys = pygame.key.get_pressed()
            self.spaceship.move(keys)
            self.spaceship.update()
            self.spaceship.bullets_group.update()
            self.enemies.update()



            self.handle_collisions()
            if self.spaceship.lives == 1 and not self.spawn_item:
                item_type = random.choice(["health", "ammo"])
                item = Item(item_type, WIDTH_SCREEN)
                self.items.add(item)
                self.spawn_item = True



            if self.level_up:
                if time.time() - self.level_upStartTime >= self.level_up_duringTime :
                    Music.play_sound_main()
                    self.spaceship.level = game_manager.current_level
                    self.spaceship.type_bullet = "type1"
                    self.spaceship.type_bullet_previous = "type1"
                    self.enemies.empty()
                    self.background = game_manager.load_map()


                    self.level_up = False
                    self.last_formation_spawn_time = pygame.time.get_ticks()



            if self.spaceship.score >= game_manager.point :
                game_manager.next_level()
                self.level_up = True
                self.level_upStartTime = time.time()
                self.turn_change_bullet = 0
                self.spaceship.type_bullet = "type1"
                self.spaceship.has_special_bullet = False

            if self.spaceship.lives <= 0:
                self.spaceship.kill()
                self.enemies.empty()
                game_manager.current_level = 1
                game_manager.point = 120
                self.game_over = True


            if self.spaceship.score >= game_manager.point / 2 and self.turn_change_bullet == 0:
                self.turn_change_bullet = 1
                type_bullet = random.choice(["type2","type3"])
                self.spaceship.type_bullet = type_bullet

            if self.spaceship.has_special_bullet :
                if pygame.time.get_ticks() - self.bullet_powerup_start > self.bullet_powerup_duringTime :
                    self.spaceship.has_special_bullet  = False
                    self.spaceship.type_bullet = self.spaceship.type_bullet_previous

            now = pygame.time.get_ticks()
            if now - self.last_formation_spawn_time > self.formation_spawn_interval:
                self.spawn_enemy_formation(WIDTH_SCREEN, HEIGHT_SCREEN)
                self.last_formation_spawn_time = now

            for bullet in list(self.spaceship.bullets):
                if not bullet.alive() or bullet.rect.bottom < 0:
                    self.spaceship.bullets.remove(bullet)
            self.enemy_bullets_group.update(dt)
            self.items.update()

    def render(self, screen):


        if self.level_up:
            Music.music_stop()
            self.enemies.empty()

        if self.paused:
            screen.blit(self.background, (0, self.bg_scroll))
            screen.blit(self.background, (0, self.bg_scroll - self.background.get_height()))  # Vẽ phần ảnh đúng theo vị trí cuộn
            self.spaceship.draw(screen)

            for bullet in self.spaceship.bullets:
                bullet.draw(screen)

            self.enemies.draw(screen)
            self.enemy_bullets_group.draw(screen)

        else :
            notification = PopupMessage((WIDTH_SCREEN * 2/8, HEIGHT_SCREEN / 2 ), "GAME PAUSE " , submessage="Press ESC To Continue")
            notification.show()
            notification.draw(screen)
            game_manager.current_level = 1
            game_manager.update_level_env()

        if self.game_over:
            notification = PopupMessage((WIDTH_SCREEN * 2 / 8, HEIGHT_SCREEN / 2), "GAME OVER =( ",
                                        submessage="Press ESC To Menu")
            notification.show()
            notification.draw(screen)
            return


        self.items.draw(screen)





    def spawn_enemy_formation(self, screen_width, screen_height):
        formation_type = random.choice(["line", "V", "wave"])
        enemy_type = random.choice(["type1", "type2", "type3","type4"])
        enemy_count = random.randint(4, 7)
        spacing_x = 90  # Khoảng cách ngang giữa các enemy
        spacing_y = 40  # Khoảng cách dọc giữa các hàng (chữ V)
        offset_y = -100  # Vị trí y bắt đầu của đỉnh chữ V

        if formation_type == "line":
            # --- Hàng ngang ---
            total_width = spacing_x * (enemy_count - 1)
            start_x = (screen_width - total_width) // 2

            for i in range(enemy_count):
                x = start_x + i * spacing_x
                y = offset_y
                enemy = EnemyShip(screen_width, screen_height, x,y, enemy_type,self.enemy_bullets_group)
                self.enemies.add(enemy)
            print("doi hinh ngang")

        elif formation_type == "V":
            # --- Đội hình chữ V ---
            center_index = enemy_count // 2
            center_x = screen_width // 2

            for i in range(enemy_count):
                offset = i - center_index
                x = center_x + offset * spacing_x
                y = offset_y + abs(offset) * spacing_y  # càng xa trung tâm càng thấp

                enemy = EnemyShip(screen_width, screen_height, x,y, enemy_type,self.enemy_bullets_group)
                self.enemies.add(enemy)
            print("doi hinh chu v")
        elif formation_type == "wave":
            # --- Đội hình đường sóng (sin) ---
            center_x = screen_width // 2
            amplitude = 120  # biên độ sóng
            frequency = 0.5  # tần số
            spacing_wave_y = 60

            for i in range(enemy_count):
                y = offset_y - i * spacing_wave_y
                x = center_x + math.sin(i * frequency) * amplitude
                enemy = EnemyShip(screen_width, screen_height, x, y, enemy_type,self.enemy_bullets_group)
                self.enemies.add(enemy)
            print("Đội hình sóng")