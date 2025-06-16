import pygame
import os



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
        self.background = pygame.transform.scale(game_manager.load_map(),
                                                 (WIDTH_SCREEN, HEIGHT_SCREEN))  # bị co kéo

        self.font = pygame.font.SysFont("Arial", 30)
        self.spaceship = Spaceship( (WIDTH_SCREEN / 2, HEIGHT_SCREEN * 3/4 ))
        self.spaceship.level = game_manager.current_level
        self.enemies = pygame.sprite.Group()
        self.level_up = False
        self.level_upStartTime =  0
        self.level_up_duringTime = 6
        self.items = pygame.sprite.Group()
        self.spawn_enemies()
        self.turn_change_bullet = 0
        self.has_specical_bullet = False
        self.bullet_powerup_start = None
        self.bullet_powerup_duringTime = 5000

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
        hits = pygame.sprite.spritecollide(self.spaceship, self.enemies, True)
        if hits:
            self.spaceship.kill()
            self.spaceship.kill_score(10)
            self.spaceship.take_hidden()
        hits2 = pygame.sprite.groupcollide(self.spaceship.bullets_group, self.enemies, True, True)
        if hits2:
            print("tieu diet duoc dich")
            self.spaceship.kill_score(10)
            for bullet in hits2.keys():
                if bullet in self.spaceship.bullets:
                    self.spaceship.bullets.remove(bullet)
            for enemies in hits2.values():
                for enemy in enemies:  # enemies là danh sách các enemy bị bắn bởi 1 viên đạn
                    if random.random() < 0.2:  # 20% cơ hội rơi item
                        item_type = random.choice(["health", "ammo"])
                        item = Item(item_type, WIDTH_SCREEN)
                        item.rect.center = enemy.rect.center  # Giờ mới đúng
                        self.items.add(item)
        hit3 = pygame.sprite.spritecollide(self.spaceship, self.items, True)
        for item in hit3:

            if item.type == "health":
                self.spaceship.heal()
                item.kill()
            elif item.type ==  "ammo":
                self.spaceship.type_bullet_previous = self.spaceship.type_bullet
                print("Loai dan cu " + str(self.spaceship.type_bullet_previous))
                self.spaceship.has_special_bullet = True
                self.bullet_powerup_start = pygame.time.get_ticks()
                item.kill()


    def update(self,screen):
        if self.spaceship.lives > 0:
            keys = pygame.key.get_pressed()
            self.spaceship.move(keys)
            self.spaceship.update()
            self.spaceship.bullets_group.update()

            for bullet in self.spaceship.bullets:
                bullet.update()

            self.enemies.update()
            self.handle_collisions()
            if self.spaceship.lives == 1 and not self.spawn_item:
                item_type = random.choice(["health", "ammo"])
                item = Item(item_type, WIDTH_SCREEN)
                self.items.add(item)
                self.spawn_item = True

            self.items.update()

            if self.level_up:
                if time.time() - self.level_upStartTime >= self.level_up_duringTime :
                    Music.play_sound_main()
                    self.spaceship.level = game_manager.current_level
                    self.spaceship.type_bullet = "type1"
                    self.spaceship.type_bullet_previous = "type1"
                    self.enemies.empty()
                    self.background = game_manager.load_map()
                    self.spawn_enemies()

                    self.level_up = False
                    return


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


                self.game_over = True


            if self.spaceship.score >= game_manager.point / 2 and self.turn_change_bullet == 0:
                self.turn_change_bullet = 1
                type_bullet = random.choice(["type2","type3"])
                print("da chuyen doi dan " + str(type_bullet))
                self.spaceship.type_bullet = type_bullet

            if self.spaceship.has_special_bullet :
                if pygame.time.get_ticks() - self.bullet_powerup_start > self.bullet_powerup_duringTime :
                    self.spaceship.has_special_bullet  = False


    def render(self, screen):
        if self.game_over:
            notification = PopupMessage((WIDTH_SCREEN * 2 / 8, HEIGHT_SCREEN / 2), "GAME OVER =( ",
                                        submessage="Press ESC To Menu")
            notification.show()
            notification.draw(screen)
            return

        if self.level_up:
            Music.music_stop()
            self.enemies.empty()

        if self.paused:
            screen.blit(self.background, (0,0))
            screen.fill((0, 0, 50))
            screen.blit(self.background, (0, 0))
            self.spaceship.draw(screen)

            for bullet in self.spaceship.bullets:
                bullet.draw(screen)
            self.enemies.draw(screen)

        else :
            notification = PopupMessage((WIDTH_SCREEN * 2/8, HEIGHT_SCREEN / 2 ), "GAME PAUSE " , submessage="Press ESC To Continue")
            notification.show()
            notification.draw(screen)
            game_manager.current_level = 1
            game_manager.update_level_env()

        self.items.draw(screen)

    def spawn_enemies(self):
        rows = 2
        columns = 9
        spacing_x = 80
        spacing_y = 60
        offset_x = 100
        offset_y = 30

        for row in range(rows):
            for col in range(columns):

                enemy_type = (col % 3) + 1
                enemy = EnemyShip(WIDTH_SCREEN, HEIGHT_SCREEN, enemy_type=enemy_type ,custom_position=True)
                enemy.rect.x = offset_x + col * spacing_x
                enemy.rect.y = offset_y + row * spacing_y
                self.enemies.add(enemy)

