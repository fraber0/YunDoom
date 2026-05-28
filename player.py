import pygame
import math
from settings import *
from map import Map
 
class Player:
    def __init__(self, move_speed=2.5, rot_speed=None, game_map=None):
        self.x = WINDOW_WIDTH  / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = 3
        self.turnDirection = 0
        self.walkDirection = 0
        self.strafeDirection = 0
        self.rotationAngle = 0 * (math.pi / 180)
        self.moveSpeed = move_speed
        self.rotationSpeed = rot_speed if rot_speed is not None else 2 * (math.pi / 180)
 
        self.map = game_map if game_map is not None else Map()

        # ── vita ──
        self.max_hp = 100
        self.hp     = 100
 
    def update(self):
        keys = pygame.key.get_pressed()
 
        self.turnDirection = 0
        self.walkDirection = 0
        self.strafeDirection = 0
 
        # rotazione visuale: frecce destra/sinistra
        if keys[pygame.K_RIGHT]:
            self.turnDirection = 1
        if keys[pygame.K_LEFT]:
            self.turnDirection = -1
 
        # avanti/indietro: W / S
        if keys[pygame.K_w]:
            self.walkDirection = 1
        if keys[pygame.K_s]:
            self.walkDirection = -1
 
        # strafe laterale: A / D
        if keys[pygame.K_a]:
            self.strafeDirection = -1
        if keys[pygame.K_d]:
            self.strafeDirection = 1

 
        self.rotationAngle += self.turnDirection * self.rotationSpeed
 
        # vettore avanti/indietro
        moveStep = self.walkDirection * self.moveSpeed
        dx = math.cos(self.rotationAngle) * moveStep
        dy = math.sin(self.rotationAngle) * moveStep
 
        # vettore laterale (perpendicolare alla direzione di sguardo)
        strafeStep = self.strafeDirection * self.moveSpeed
        sx = math.cos(self.rotationAngle + math.pi / 2) * strafeStep
        sy = math.sin(self.rotationAngle + math.pi / 2) * strafeStep

 
        if not self.map.has_wall_at(self.x + dx + sx, self.y):
            self.x += dx + sx
        if not self.map.has_wall_at(self.x, self.y + dy + sy):
            self.y += dy + sy
 
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(screen, (255, 0, 0),
                         (self.x, self.y),
                         (self.x + math.cos(self.rotationAngle) * 50,
                          self.y + math.sin(self.rotationAngle) * 50))
