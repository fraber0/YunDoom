import pygame
import math
from settings import *
import random



class Enemy:
    def __init__(self, x, y, sprite_path, scale=1.0, y_offset=0.0):
        self.x = x
        self.y = y

        self.sprite = pygame.image.load(sprite_path).convert_alpha()

        self.speed = 1

        self.scale = scale
        self.y_offset = y_offset

        # Distanze AI
        self.chase_distance = 200   # inizia a inseguire
        self.stop_distance = 14     # smette di avanzare

        # ── vita ──
        self.max_hp = 100
        self.hp     = 100
        self.alive  = True

        # danno inflitto al player ogni N frame quando è vicino
        self._attack_cooldown    = 0
        self._attack_cooldown_max = 60   # 1 secondo a 60 fps

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False

    def update(self, player):
        if not self.alive:
            return

        # Differenza posizione
        dx = player.x - self.x
        dy = player.y - self.y

        # Distanza dal player
        dist = math.sqrt(dx * dx + dy * dy)

        # Player troppo lontano → fermo
        if dist > self.chase_distance:
            return

        damage_sound = pygame.mixer.Sound(
            "./Assets/sounds/damage.mp3"
        )
        damage_sound.set_volume(1.5)

        # Attacca il player se abbastanza vicino
        if dist < self.stop_distance:
            self._attack_cooldown -= 1
            if self._attack_cooldown <= 0:
                damage_sound.play()
                player.hp = max(0, player.hp - 10)
                self._attack_cooldown = self._attack_cooldown_max
            return

        # Evita divisione per 0
        if dist == 0:
            return

        # Direzione normalizzata
        nx = dx / dist
        ny = dy / dist

        # Movimento
        self.x += nx * self.speed
        self.y += ny * self.speed

    def distance_to(self, player):
        dx = self.x - player.x
        dy = self.y - player.y

        return math.sqrt(dx * dx + dy * dy)


# ══════════════════════════════════════════════════════════════════════════════
# AMMO BOX
# ══════════════════════════════════════════════════════════════════════════════

class AmmoBox:
    PICKUP_DISTANCE = 20   # pixel entro cui viene raccolta
    AMMO_AMOUNT     = 10   # munizioni che aggiunge

    def __init__(self, x, y, sprite_path, scale=0.25, y_offset=0.5, bob_speed=0.05, bob_amount=6):
        self.x = x
        self.y = y
        raw = pygame.image.load(sprite_path).convert_alpha()
        self.sprite  = raw
        self.active  = True
        self.scale   = scale        # ← dimensione relativa al nemico
        self.y_offset = y_offset

        self._bob_speed  = bob_speed
        self._bob_amount = bob_amount
        self._bob_tick   = random.uniform(0, math.pi * 2)

        self.reload_sound = pygame.mixer.Sound(
            "./Assets/sounds/reload.mp3"
        )
        self.reload_sound.set_volume(1.5)

    @property
    def bob_offset(self):
        return int(math.sin(self._bob_tick) * self._bob_amount)

    def update_bob(self):
        self._bob_tick += self._bob_speed

    def distance_to(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        return math.sqrt(dx * dx + dy * dy)

    def try_pickup(self, player, weapon) -> bool:
        """Restituisce True se il player l'ha raccolta in questo frame."""
        if not self.active:
            return False
        if self.distance_to(player) <= self.PICKUP_DISTANCE:
            self.reload_sound.play()
            weapon.reload(self.AMMO_AMOUNT)
            self.active = False
            return True
        return False







class ObjectManager:
    def __init__(self, player, raycaster, game_map=None, weapon=None):
        self.player = player
        self.raycaster = raycaster
        self.game_map  = game_map
        self.weapon = weapon
        self.enemies: list[Enemy] = []
        self.ammo_boxes: list[AmmoBox] = []

    def add_enemy(self, x, y, sprite_path, scale=1.0, y_offset=0.0):
        self.enemies.append(
            Enemy(x, y, sprite_path, scale=scale, y_offset=y_offset)
        )

    def spawn_ammo_boxes(self, sprite_path: str, count: int = 3):

        """
        Spawna `count` scatole di munizioni in celle libere della mappa,
        posizionate al centro della cella.
        """
        if self.game_map is None:
            return

        grid = self.game_map.grid
        free_cells = []
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    # coordinate mondo (centro della cella)
                    cx = col_idx * TILESIZE + TILESIZE // 2
                    cy = row_idx * TILESIZE + TILESIZE // 2
                    free_cells.append((cx, cy))

        '''
        # Evita di spawnare sopra il player (escludi celle troppo vicine)
        free_cells = [
            (cx, cy) for cx, cy in free_cells
            if math.sqrt((cx - self.player.x)**2 + (cy - self.player.y)**2) > TILESIZE * 2
        ]
        '''

        chosen = random.sample(free_cells, min(count, len(free_cells)))
        for cx, cy in chosen:
            self.ammo_boxes.append(AmmoBox(cx, cy, sprite_path, y_offset=0.0))

    def update(self):
        for enemy in self.enemies:
            enemy.update(self.player)

        if self.weapon is not None:
            for box in self.ammo_boxes:
                box.try_pickup(self.player, self.weapon)

        for box in self.ammo_boxes:      
            if box.active:
                box.update_bob()

    def render(self, screen):
        sprites = []
        for e in self.enemies:
            if e.alive:
                sprites.append(("enemy", e))
        for b in self.ammo_boxes:
            if b.active:
                sprites.append(("ammo", b))

        sprites.sort(key=lambda s: s[1].distance_to(self.player), reverse=True)

        for _, obj in sprites:
            self.render_sprite(screen, obj)

    def render_sprite(self, screen, obj):
        player = self.player

        obj_scale      = getattr(obj, "scale",      1.0)
        obj_y_offset   = getattr(obj, "y_offset",   0.0)
        obj_bob_offset = getattr(obj, "bob_offset",   0)   # ← mancava

        dx = obj.x - player.x
        dy = obj.y - player.y
        sprite_distance = math.sqrt(dx * dx + dy * dy)

        MIN_DIST = 30
        if sprite_distance < MIN_DIST:
            sprite_distance = MIN_DIST
        if sprite_distance <= 0:
            return

        sprite_angle = math.atan2(dy, dx)
        angle_diff   = sprite_angle - player.rotationAngle

        while angle_diff >  math.pi: angle_diff -= 2 * math.pi
        while angle_diff < -math.pi: angle_diff += 2 * math.pi

        if abs(angle_diff) > (FOV / 2) + 0.1:
            return

        center_col     = int((angle_diff / FOV + 0.5) * WINDOW_WIDTH)
        corrected_dist = sprite_distance * math.cos(angle_diff)

        if corrected_dist <= 0:
            return

        MAX_SPRITE_SIZE = WINDOW_HEIGHT * 2
        sprite_height   = min(
            int((TILESIZE / corrected_dist) * 415 * obj_scale),   # ← * obj_scale
            MAX_SPRITE_SIZE
        )
        sprite_width = sprite_height

        if sprite_width <= 0 or sprite_height <= 0:
            return

        draw_top  = (WINDOW_HEIGHT // 2 - sprite_height // 2
                   + int(sprite_height * (1 - obj_scale) / 2)
                   + int(sprite_height * obj_y_offset)
                   + obj_bob_offset)                              # ← bob applicato
        draw_left = center_col - sprite_width // 2

        scaled_sprite = pygame.transform.scale(obj.sprite, (sprite_width, sprite_height))

        rays      = self.raycaster.rays
        ray_width = RES
        num_rays  = len(rays)
        col_start = max(0, draw_left)
        col_end   = min(WINDOW_WIDTH, draw_left + sprite_width)

        for screen_x in range(col_start, col_end):
            ray_idx = int(screen_x / ray_width)
            if ray_idx < 0 or ray_idx >= num_rays:
                continue
            if rays[ray_idx].distance < corrected_dist:
                continue

            col         = screen_x - draw_left
            col_surface = pygame.Surface((1, sprite_height), pygame.SRCALPHA)
            col_surface.blit(scaled_sprite, (0, 0), (col, 0, 1, sprite_height))
            screen.blit(col_surface, (screen_x, draw_top))


    def try_shoot(self):
        """Spara al nemico più vicino che è nel campo visivo centrale.
        Ritorna True se colpisce."""
        
        print(self.weapon.is_shooting)

        import math
        best = None
        best_dist = float('inf')
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            dist = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx)
            diff = angle - self.player.rotationAngle
            while diff >  math.pi: diff -= 2*math.pi
            while diff < -math.pi: diff += 2*math.pi
            # mirino largo ±5°
            if abs(diff) < math.radians(5) and dist < best_dist:
                best = enemy
                best_dist = dist
        if best:
            best.take_damage(25)
            return True
        return False
