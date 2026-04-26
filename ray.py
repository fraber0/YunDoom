import math, pygame
from settings import *

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if (angle < 0):
        angle = (2 * math.pi) + angle
    return angle

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

class Ray:
    def __init__(self, angle, player, map):
        self.rayAngle = normalizeAngle(angle)
        self.player = player
        self.map = map
        # le coordinate y sono invertite quindi da 0° a 180° stiamo guardando in basso
        self.is_facing_down = self.rayAngle > 0 and self.rayAngle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.rayAngle < 0.5 * math.pi or self.rayAngle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

        self.distance = 0

        self.color = 255

    def cast(self):
        # =========================
        # HORIZONTAL COLLISION
        # =========================
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        # evita problemi con raggi orizzontali
        is_horizontal_ray = abs(math.sin(self.rayAngle)) < 0.0001

        if not is_horizontal_ray:
            if self.is_facing_up:
                first_intersection_y = (self.player.y // TILESIZE) * TILESIZE - 0.01
            else:
                first_intersection_y = (self.player.y // TILESIZE) * TILESIZE + TILESIZE

            first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(self.rayAngle)

            next_horizontal_x = first_intersection_x
            next_horizontal_y = first_intersection_y

            ya = -TILESIZE if self.is_facing_up else TILESIZE
            xa = ya / math.tan(self.rayAngle)

            while (0 <= next_horizontal_x <= WINDOW_WIDTH and
                   0 <= next_horizontal_y <= WINDOW_HEIGHT):

                if self.map.has_wall_at(next_horizontal_x, next_horizontal_y):
                    found_horizontal_wall = True
                    horizontal_hit_x = next_horizontal_x
                    horizontal_hit_y = next_horizontal_y
                    break

                next_horizontal_x += xa
                next_horizontal_y += ya

        # =========================
        # VERTICAL COLLISION
        # =========================
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        # evita problemi con raggi verticali
        is_vertical_ray = abs(math.cos(self.rayAngle)) < 0.0001

        if not is_vertical_ray:
            if self.is_facing_right:
                first_intersection_x = (self.player.x // TILESIZE) * TILESIZE + TILESIZE
            else:
                first_intersection_x = (self.player.x // TILESIZE) * TILESIZE - 0.01

            first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(self.rayAngle)

            next_vertical_x = first_intersection_x
            next_vertical_y = first_intersection_y

            xa = TILESIZE if self.is_facing_right else -TILESIZE
            ya = xa * math.tan(self.rayAngle)

            while (0 <= next_vertical_x <= WINDOW_WIDTH and
                   0 <= next_vertical_y <= WINDOW_HEIGHT):

                if self.map.has_wall_at(next_vertical_x, next_vertical_y):
                    found_vertical_wall = True
                    vertical_hit_x = next_vertical_x
                    vertical_hit_y = next_vertical_y
                    break

                next_vertical_x += xa
                next_vertical_y += ya

        # =========================
        # DISTANCE
        # =========================
        horizontal_distance = float('inf')
        vertical_distance = float('inf')

        if found_horizontal_wall:
            horizontal_distance = distance_between(
                self.player.x, self.player.y,
                horizontal_hit_x, horizontal_hit_y
            )

        if found_vertical_wall:
            vertical_distance = distance_between(
                self.player.x, self.player.y,
                vertical_hit_x, vertical_hit_y
            )

        # =========================
        # CHOOSE CLOSEST HIT
        # =========================
        if horizontal_distance < vertical_distance:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_distance
            self.color = 160
        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y
            self.distance = vertical_distance
            self.color = 255
            
        self.distance *= math.cos(self.player.rotationAngle - self.rayAngle)

        self.color *= (60 / self.distance)
        if self.color > 255:
            self.color = 255
        elif self.color < 0:
            self.color = 0

    def render(self, screen):
        #pygame.draw.line(screen, (255, 0, 0), (self.player.x, self.player.y), (self.player.x + math.cos(self.rayAngle) * 50, self.player.y + math.sin(self.rayAngle) * 50)) 
        pygame.draw.line(screen, (255, 0, 0), (self.player.x, self.player.y), (self.wall_hit_x, self.wall_hit_y))
