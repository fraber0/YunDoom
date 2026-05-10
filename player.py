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
        self.rotationAngle = 0 * (math.pi / 180)
        self.moveSpeed = move_speed
        self.rotationSpeed = rot_speed if rot_speed is not None else 2 * (math.pi / 180)
 
        # se viene passata una mappa la usa, altrimenti crea quella default
        self.map = game_map if game_map is not None else Map()
 
    def update(self):
        keys = pygame.key.get_pressed()
 
        self.turnDirection = 0
        self.walkDirection = 0
 
        if keys[pygame.K_RIGHT]:
            self.turnDirection = 1
        if keys[pygame.K_LEFT]:
            self.turnDirection = -1
        if keys[pygame.K_UP]:
            self.walkDirection = 1
        if keys[pygame.K_DOWN]:
            self.walkDirection = -1
 
        moveStep = self.walkDirection * self.moveSpeed
        self.rotationAngle += self.turnDirection * self.rotationSpeed
        dx = math.cos(self.rotationAngle) * moveStep
        dy = math.sin(self.rotationAngle) * moveStep
 
        if not self.map.has_wall_at(self.x + dx, self.y):
            self.x += dx
        if not self.map.has_wall_at(self.x, self.y + dy):
            self.y += dy
 
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(screen, (255, 0, 0),
                         (self.x, self.y),
                         (self.x + math.cos(self.rotationAngle) * 50,
                          self.y + math.sin(self.rotationAngle) * 50))