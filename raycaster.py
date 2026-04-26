import pygame
from settings import *
from ray import Ray

class Raycaster:
    def __init__(self, player, map):
        self.rays = []
        self.player = player
        self.map = map

    def castAllRays(self):
        self.rays = []
        rayAngle = (self.player.rotationAngle - FOV/2)
        for i in range(NUM_RAYS):
            ray = Ray(rayAngle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)

            rayAngle += FOV / NUM_RAYS

    def render(self, screen):

        i = 0
        for ray in self.rays:
            # ray.render(screen)

            line_height = (32 / ray.distance) * 415

            draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
            draw_end = (WINDOW_HEIGHT / 2) + (line_height / 2)

            pygame.draw.rect(screen, (ray.color, ray.color,ray.color), (i*RES, draw_begin, RES, draw_end - draw_begin))

            i += 1
