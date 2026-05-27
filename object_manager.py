import pygame
import math
from settings import *
import random



class MeleeEnemy:
    """Nemico corpo a corpo: insegue il player e lo colpisce da vicino."""

    def __init__(
        self,
        x, y, sprite_path,
        *,
        scale           = 1.0,
        y_offset        = 0.0,
        max_hp          = 100,
        speed           = 1.0,
        chase_distance  = 300,
        stop_distance   = 14,
        attack_damage   = 10,
        attack_rate     = 60,   # frame tra un attacco e l'altro (60 = 1 sec a 60fps)
    ):
        self.x = x
        self.y = y
        self.sprite        = pygame.image.load(sprite_path).convert_alpha()
        self.scale         = scale
        self.y_offset      = y_offset
        self.radius        = 10

        self.speed          = speed
        self.chase_distance = chase_distance
        self.stop_distance  = stop_distance
        self.attack_damage  = attack_damage

        self.max_hp = max_hp
        self.hp     = max_hp
        self.alive  = True

        self._cooldown     = 0
        self._cooldown_max = attack_rate

        self._damage_sound = pygame.mixer.Sound("./Assets/sounds/damage.mp3")
        self._damage_sound.set_volume(1.5)
        self._attack_sound = pygame.mixer.Sound("./Assets/sounds/PM_attacco.mp3")
        self._attack_sound.set_volume(1.5)

    # ── helpers ──────────────────────────────────────────────────────────────

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False

    def distance_to(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        return math.sqrt(dx * dx + dy * dy)

    def _move(self, nx, ny, game_map):
        """Sliding movement: prova x e y separatamente per non incastrarsi nei muri."""
        new_x = self.x + nx * self.speed
        new_y = self.y + ny * self.speed
        if not game_map.has_wall_at(new_x, new_y):
            self.x, self.y = new_x, new_y
        elif not game_map.has_wall_at(new_x, self.y):
            self.x = new_x
        elif not game_map.has_wall_at(self.x, new_y):
            self.y = new_y

    # ── update ───────────────────────────────────────────────────────────────

    def update(self, player, game_map, all_enemies):
        if not self.alive:
            return

        dx   = player.x - self.x
        dy   = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        # ── separazione tra nemici ──────────────────────────────────────────
        sep_x, sep_y = 0.0, 0.0
        for other in all_enemies:
            if other is self or not other.alive:
                continue
            odx   = self.x - other.x
            ody   = self.y - other.y
            odist = math.sqrt(odx * odx + ody * ody)
            min_d = self.radius + other.radius
            if 0 < odist < min_d:
                push   = (min_d - odist) / odist
                sep_x += odx * push
                sep_y += ody * push

        if sep_x != 0 or sep_y != 0:
            sep_len = math.sqrt(sep_x * sep_x + sep_y * sep_y)
            self._move(sep_x / sep_len, sep_y / sep_len, game_map)

        if dist > self.chase_distance:
            return

        if dist < self.stop_distance:
            self._cooldown -= 1
            if self._cooldown <= 0:
                self._attack_sound.play()
                self._damage_sound.play()
                player.hp      = max(0, player.hp - self.attack_damage)
                self._cooldown = self._cooldown_max
            return

        if dist == 0:
            return

        self._move(dx / dist, dy / dist, game_map)


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
        self.enemies: list[MeleeEnemy] = []
        self.ammo_boxes: list[AmmoBox] = []

    def add_melee_enemy(
        self,
        x, y, sprite_path,
        *,
        scale           = 1.0,
        y_offset        = 0.0,
        max_hp          = 100,
        speed           = 1.0,
        chase_distance  = 300,
        stop_distance   = 14,
        attack_damage   = 10,
        attack_rate     = 60,
    ):
        self.enemies.append(MeleeEnemy(
            x, y, sprite_path,
            scale          = scale,
            y_offset       = y_offset,
            max_hp         = max_hp,
            speed          = speed,
            chase_distance = chase_distance,
            stop_distance  = stop_distance,
            attack_damage  = attack_damage,
            attack_rate    = attack_rate,
        ))


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
            enemy.update(self.player, self.game_map, self.enemies)

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
