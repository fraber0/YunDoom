import pygame
import math
from settings import *
from player import Player

sprite_img = pygame.image.load("./Assets/Francesco Berra - Screenshot 2025-11-23 161922.png").convert_alpha()

class Giulio:
    def __init__(self, x, y):
        self.x = x
        self.y = y