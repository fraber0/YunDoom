import pygame
from settings import *
 
_DEFAULT_GRID = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
 
class Map:
    def __init__(self, grid=None):
        self.grid = grid if grid is not None else _DEFAULT_GRID
 
    def has_wall_at(self, x, y):
        if x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
            return True
        grid_x = int(x // TILESIZE)
        grid_y = int(y // TILESIZE)
        return self.grid[grid_y][grid_x] == 1
 
    def render(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                tile_x = j * TILESIZE
                tile_y = i * TILESIZE
                if self.grid[i][j] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (tile_x, tile_y, TILESIZE - 1, TILESIZE - 1))
                elif self.grid[i][j] == 1:
                    pygame.draw.rect(screen, (40, 40, 40), (tile_x, tile_y, TILESIZE - 1, TILESIZE - 1))