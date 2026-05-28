import pygame

class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.current_music = None

        self.tracks = {
            "menu": "./Assets/sounds/menu_song.mp3",
            "game": "./Assets/sounds/game.mp3",
            "info": "./Assets/sounds/info.mp3",
        }

    def play(self, name, volume=0.5):
        # cambia musica SOLO se diversa
        if self.current_music == name:
            return

        pygame.mixer.music.load(self.tracks[name])
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)   # loop infinito

        self.current_music = name

    def stop(self):
        pygame.mixer.music.stop()
        self.current_music = None
