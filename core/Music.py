import pygame

sounds = [
    "Asset/sound/theme.mp3",
    "Asset/sound/sound_play.mp3",
    "Asset/sound/click.mp3",
    "Asset/sound/sound_bullet.mp3",
    "Asset/sound/sound_play_1.mp3"
]

class Music:
    @staticmethod
    def music_load(path):
        pygame.mixer.music.load(path)

    @staticmethod
    def music_stop():
        pygame.mixer.music.stop()

    @staticmethod
    def music_play(loop=-1):
        pygame.mixer.music.play(loop)

    @staticmethod
    def play_sound_intro():
        Music.music_load(sounds[0])
        Music.music_play()

    @staticmethod
    def play_sound_main():
        Music.music_load(sounds[4])
        pygame.mixer.music.set_volume(0.3)
        Music.music_play()

