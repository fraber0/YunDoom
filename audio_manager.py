import pygame


class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.current_music = None

        self.tracks = {
            "menu": "./Assets/sounds/menu_song.mp3",
        }

    def play(self, name):
        # evita restart stessa musica
        if self.current_music == name or pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(self.tracks[name])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.current_music = name
