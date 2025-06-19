import pygame

ENEMY_IMAGES = {}
EXPLOSION_IMAGE = None
EXPLOSION_SOUND = None

def init_enemy_assets():
    global ENEMY_IMAGES, EXPLOSION_IMAGE, EXPLOSION_SOUND

    ENEMY_IMAGES = {
        "type1": pygame.transform.scale(
            pygame.image.load("Asset/enemy/enemyship_level2.png").convert_alpha(), (70, 70)),
        "type2": pygame.transform.scale(
            pygame.image.load("Asset/enemy/enemyship_level3.png").convert_alpha(), (70, 70)),
        "type3": pygame.transform.scale(
            pygame.image.load("Asset/enemy/enemyship_level4.png").convert_alpha(), (70, 70)),
        "type4": pygame.transform.scale(
            pygame.image.load("Asset/enemy/enemyship_level5.png").convert_alpha(), (70, 70)),
    }

    EXPLOSION_IMAGE = pygame.transform.scale(
        pygame.image.load("Asset/enemy/explosion.png").convert_alpha(), (50, 50))

    EXPLOSION_SOUND = pygame.mixer.Sound("Asset/sound/reward.mp3")
