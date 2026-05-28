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
        attack_rate     = 60,   
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
        self._attack_sound_PM = pygame.mixer.Sound("./Assets/sounds/PM_attacco.mp3")
        self._attack_sound_PM.set_volume(1.5)
        self._attack_sound_T = pygame.mixer.Sound("./Assets/sounds/Togni2.mp3")
        self._attack_sound_T.set_volume(1.5)


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
        r = self.radius
        new_x = self.x + nx * self.speed
        new_y = self.y + ny * self.speed

        def clear(cx, cy):
            return (not game_map.has_wall_at(cx + r, cy) and
                    not game_map.has_wall_at(cx - r, cy) and
                    not game_map.has_wall_at(cx, cy + r) and
                    not game_map.has_wall_at(cx, cy - r))

        if clear(new_x, new_y):
            self.x, self.y = new_x, new_y
        elif clear(new_x, self.y):
            self.x = new_x
        elif clear(self.x, new_y):
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
                if self.scale == 0.5:
                    self._attack_sound_PM.play()
                elif self.scale == 1.0:
                    self._attack_sound_T.play()

                self._damage_sound.play()
                player.hp      = max(0, player.hp - self.attack_damage)
                self._cooldown = self._cooldown_max
            return

        if dist == 0:
            return

        self._move(dx / dist, dy / dist, game_map)

# ══════════════════════════════════════════════════════════════════════════════
# BOSS
# ══════════════════════════════════════════════════════════════════════════════

class Boss:
    """
    Boss: molto più grande di un nemico normale.
    Insegue il player e, se lo raggiunge, lo uccide istantaneamente (game over).
    Assorbe molti più colpi prima di morire.
    """

    def __init__(
        self,
        x, y, sprite_path,
        *,
        scale           = 2.0,      
        y_offset        = -0.1,
        max_hp          = 500,
        speed           = 0.7,
        chase_distance  = 600,
        stop_distance   = 20,       
        attack_rate     = 90,
    ):
        self.x = x
        self.y = y
        self.sprite        = pygame.image.load(sprite_path).convert_alpha()
        self.scale         = scale
        self.y_offset      = y_offset
        self.radius        = 20     

        self.speed          = speed
        self.chase_distance = chase_distance
        self.stop_distance  = stop_distance

        self.max_hp = max_hp
        self.hp     = max_hp
        self.alive  = True

        self._cooldown     = 0
        self._cooldown_max = attack_rate

    # ── bob_offset ────────────────────────────────
    @property
    def bob_offset(self):
        return 0

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
        """
        Ritorna True se il boss ha raggiunto il player (game over), False altrimenti.
        """
        if not self.alive:
            return False

        dx   = player.x - self.x
        dy   = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > self.chase_distance:
            return False

        # separazione dagli altri nemici
        sep_x, sep_y = 0.0, 0.0
        for other in all_enemies:
            if other is self or not getattr(other, "alive", True):
                continue
            odx   = self.x - other.x
            ody   = self.y - other.y
            odist = math.sqrt(odx * odx + ody * ody)
            min_d = self.radius + getattr(other, "radius", 10)
            if 0 < odist < min_d:
                push   = (min_d - odist) / odist
                sep_x += odx * push
                sep_y += ody * push

        if sep_x != 0 or sep_y != 0:
            sep_len = math.sqrt(sep_x * sep_x + sep_y * sep_y)
            self._move(sep_x / sep_len, sep_y / sep_len, game_map)

        if dist < self.stop_distance:
            self._cooldown -= 1
            if self._cooldown <= 0:
                self._cooldown = self._cooldown_max
            player.hp = 0   # uccide istantaneamente
            return True     # segnala game over al chiamante

        if dist == 0:
            return False

        self._move(dx / dist, dy / dist, game_map)
        return False

# ══════════════════════════════════════════════════════════════════════════════
# PROJECTILE
# ══════════════════════════════════════════════════════════════════════════════

class Projectile:
    """
    Proiettile sparato da un RangedEnemy.
    Si muove in linea retta, viene renderizzato come sprite 3D nel raycaster,
    esplode a contatto con un muro o con il player.
    """

    def __init__(self, x, y, angle, sprite, *, speed=4.0, damage=15,
                 scale=0.15, y_offset=0.0, max_range=500):
        self.x       = x
        self.y       = y
        self.angle   = angle          
        self.sprite  = sprite         
        self.speed   = speed
        self.damage  = damage
        self.scale   = scale
        self.y_offset = y_offset
        self.active  = True

        self._dx = math.cos(angle) * speed
        self._dy = math.sin(angle) * speed

        self._traveled   = 0.0
        self._max_range  = max_range

        self.bob_offset = 0

    def distance_to(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        return math.sqrt(dx * dx + dy * dy)

    def update(self, player, game_map):
        if not self.active:
            return

        nx = self.x + self._dx
        ny = self.y + self._dy

        # collisione con i muri
        if game_map.has_wall_at(nx, ny):
            self.active = False
            return

        self.x = nx
        self.y = ny
        self._traveled += self.speed

        # range massimo
        if self._traveled >= self._max_range:
            self.active = False
            return

        # collisione con il player
        if self.distance_to(player) < 12:
            player.hp  = max(0, player.hp - self.damage)
            self.active = False


# ══════════════════════════════════════════════════════════════════════════════
# RANGED ENEMY
# ══════════════════════════════════════════════════════════════════════════════

class RangedEnemy:
    def __init__(
        self,
        x, y,
        sprite_path,
        projectile_sprite_path,
        *,
        scale              = 1.0,
        y_offset           = 0.0,
        max_hp             = 80,
        speed              = 0.8,
        chase_distance     = 400,
        preferred_dist     = 180,   
        fire_rate          = 90,    
        projectile_speed   = 5.0,
        projectile_damage  = 15,
        projectile_scale   = 0.15,
        projectile_y_offset= 0.0,
        projectile_max_range = 500,
    ):
        self.x = x
        self.y = y
        self.sprite   = pygame.image.load(sprite_path).convert_alpha()
        self._proj_sprite = pygame.image.load(projectile_sprite_path).convert_alpha()

        self.scale    = scale
        self.y_offset = y_offset
        self.radius   = 10

        self.speed           = speed
        self.chase_distance  = chase_distance
        self.preferred_dist  = preferred_dist

        self._fire_rate      = fire_rate
        self._fire_cooldown  = fire_rate   
        self._proj_speed     = projectile_speed
        self._proj_damage    = projectile_damage
        self._proj_scale     = projectile_scale
        self._proj_y_offset  = projectile_y_offset
        self._proj_max_range = projectile_max_range

        self.max_hp = max_hp
        self.hp     = max_hp
        self.alive  = True

        self.projectiles: list[Projectile] = []

        try:
            self._shoot_sound = pygame.mixer.Sound("./Assets/sounds/Freccia_Scagliata.mp3")
            self._shoot_sound.set_volume(0.4)
        except Exception:
            self._shoot_sound = None

        try:
            self._damage_sound = pygame.mixer.Sound("./Assets/sounds/Freccia_Colpito.mp3")
            self._damage_sound.set_volume(1.0)
        except Exception:
            self._damage_sound = None

    # ── helpers ──────────────────────────────────────────────────────────────

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self._damage_sound:
            self._damage_sound.play()
        if self.hp == 0:
            self.alive = False

    def distance_to(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        return math.sqrt(dx * dx + dy * dy)

    # bob_offset
    @property
    def bob_offset(self):
        return 0

    def _move(self, nx, ny, game_map):
        new_x = self.x + nx * self.speed
        new_y = self.y + ny * self.speed
        if not game_map.has_wall_at(new_x, new_y):
            self.x, self.y = new_x, new_y
        elif not game_map.has_wall_at(new_x, self.y):
            self.x = new_x
        elif not game_map.has_wall_at(self.x, new_y):
            self.y = new_y

    def _fire(self, player):
        """Crea un proiettile puntato verso il player con leggero spread."""
        dx = player.x - self.x
        dy = player.y - self.y
        base_angle = math.atan2(dy, dx)
        spread = random.uniform(-0.05, 0.05)  
        angle  = base_angle + spread
        self.projectiles.append(Projectile(
            self.x, self.y, angle,
            self._proj_sprite,
            speed      = self._proj_speed,
            damage     = self._proj_damage,
            scale      = self._proj_scale,
            y_offset   = self._proj_y_offset,
            max_range  = self._proj_max_range,
        ))
        if self._shoot_sound:
            self._shoot_sound.play()

    # ── update ───────────────────────────────────────────────────────────────

    def update(self, player, game_map, all_enemies):
        if not self.alive:
            return

        # aggiorna i proiettili vivi
        for proj in self.projectiles:
            proj.update(player, game_map)
        self.projectiles = [p for p in self.projectiles if p.active]

        dx   = player.x - self.x
        dy   = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > self.chase_distance:
            return

        # ── separazione tra nemici ──────────────────────────────────────────
        sep_x, sep_y = 0.0, 0.0
        for other in all_enemies:
            if other is self or not getattr(other, "alive", True):
                continue
            odx   = self.x - other.x
            ody   = self.y - other.y
            odist = math.sqrt(odx * odx + ody * ody)
            min_d = self.radius + getattr(other, "radius", 10)
            if 0 < odist < min_d:
                push   = (min_d - odist) / odist
                sep_x += odx * push
                sep_y += ody * push

        if sep_x != 0 or sep_y != 0:
            sep_len = math.sqrt(sep_x * sep_x + sep_y * sep_y)
            self._move(sep_x / sep_len, sep_y / sep_len, game_map)

        if dist == 0:
            return

        if dist > self.preferred_dist:
            self._move(dx / dist, dy / dist, game_map)
        elif dist < self.preferred_dist * 0.7:
            self._move(-dx / dist, -dy / dist, game_map)

        # ── fuoco ──────────────────────────────────────────────────────────
        self._fire_cooldown -= 1
        if self._fire_cooldown <= 0:
            self._fire(player)
            self._fire_cooldown = self._fire_rate


# ══════════════════════════════════════════════════════════════════════════════
# AMMO BOX
# ══════════════════════════════════════════════════════════════════════════════

class AmmoBox:
    PICKUP_DISTANCE = 20   
    AMMO_AMOUNT     = 10   

    def __init__(self, x, y, sprite_path, scale=0.25, y_offset=0.5, bob_speed=0.05, bob_amount=6):
        self.x = x
        self.y = y
        raw = pygame.image.load(sprite_path).convert_alpha()
        self.sprite  = raw
        self.active  = True
        self.scale   = scale        
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



# ══════════════════════════════════════════════════════════════════════════════
# HEAL
# ══════════════════════════════════════════════════════════════════════════════

class Heal:
    PICKUP_DISTANCE = 20   
    HEAL_AMOUNT     = 25   

    def __init__(self, x, y, sprite_path, scale=0.25, y_offset=0.5, bob_speed=0.05, bob_amount=6):
        self.x = x
        self.y = y
        raw = pygame.image.load(sprite_path).convert_alpha()
        self.sprite  = raw
        self.active  = True
        self.scale   = scale        
        self.y_offset = y_offset

        self._bob_speed  = bob_speed
        self._bob_amount = bob_amount
        self._bob_tick   = random.uniform(0, math.pi * 2)

        self.heal_sound = pygame.mixer.Sound(
            "./Assets/sounds/Coconut.mp3"
        )
        self.heal_sound.set_volume(1.5)

    @property
    def bob_offset(self):
        return int(math.sin(self._bob_tick) * self._bob_amount)

    def update_bob(self):
        self._bob_tick += self._bob_speed

    def distance_to(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        return math.sqrt(dx * dx + dy * dy)

    def try_pickup(self, player) -> bool:
        """Restituisce True se il player l'ha raccolta in questo frame."""
        if not self.active:
            return False
        if self.distance_to(player) <= self.PICKUP_DISTANCE:
            self.heal_sound.play()
            self.heal_to_add = 100 - player.hp
            if self.heal_to_add <= 25:
                player.hp = 100
            else:
                player.hp += 25
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
        self.ranged_enemies: list[RangedEnemy] = []
        self.ammo_boxes: list[AmmoBox] = []
        self.heal_boxes: list[Heal] = []
        self.bosses: list[Boss] = []

    def add_boss(
        self,
        x, y, sprite_path,
        *,
        scale          = 2.2,
        y_offset       = -0.3,
        max_hp         = 5000,
        speed          = 0.7,
        chase_distance = 600,
        stop_distance  = 20,
        attack_rate    = 90,
    ):
        self.bosses.append(Boss(
            x, y, sprite_path,
            scale          = scale,
            y_offset       = y_offset,
            max_hp         = max_hp,
            speed          = speed,
            chase_distance = chase_distance,
            stop_distance  = stop_distance,
            attack_rate    = attack_rate,
        ))

    def add_ranged_enemy(
        self,
        x, y,
        sprite_path,
        projectile_sprite_path,
        *,
        scale               = 1.0,
        y_offset            = 0.0,
        max_hp              = 80,
        speed               = 0.8,
        chase_distance      = 400,
        preferred_dist      = 180,
        fire_rate           = 90,
        projectile_speed    = 5.0,
        projectile_damage   = 15,
        projectile_scale    = 0.15,
        projectile_y_offset = 0.0,
        projectile_max_range = 500,
    ):
        self.ranged_enemies.append(RangedEnemy(
            x, y,
            sprite_path,
            projectile_sprite_path,
            scale               = scale,
            y_offset            = y_offset,
            max_hp              = max_hp,
            speed               = speed,
            chase_distance      = chase_distance,
            preferred_dist      = preferred_dist,
            fire_rate           = fire_rate,
            projectile_speed    = projectile_speed,
            projectile_damage   = projectile_damage,
            projectile_scale    = projectile_scale,
            projectile_y_offset = projectile_y_offset,
            projectile_max_range= projectile_max_range,
        ))

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

    def spawn_heal_boxes(self, sprite_path: str, count: int = 3):

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
            self.heal_boxes.append(Heal(cx + 50, cy, sprite_path, y_offset=0.0))

    def random_spawn_pos(
        self,
        min_dist_from_player: float = 150.0,
        min_dist_from_others: float = 60.0,
        occupied_positions: list[tuple[float, float]] | None = None,
    ) -> tuple[float, float]:
        if self.game_map is None:
            return self.player.x + 200, self.player.y

        occupied_positions = occupied_positions or []
        grid = self.game_map.grid

        MIN_TILE_DIST = 2 * TILESIZE

        free_centers = [
            (float(col_idx * TILESIZE + TILESIZE // 2),
             float(row_idx * TILESIZE + TILESIZE // 2))
            for row_idx, row in enumerate(grid)
            for col_idx, cell in enumerate(row)
            if cell == 0
            and math.sqrt(
                (col_idx * TILESIZE + TILESIZE // 2 - self.player.x) ** 2 +
                (row_idx * TILESIZE + TILESIZE // 2 - self.player.y) ** 2
            ) >= MIN_TILE_DIST
        ]

        random.shuffle(free_centers)
        return free_centers[0] if free_centers else (self.player.x + 200, self.player.y)


    def update(self):
        all_enemies = self.enemies + self.ranged_enemies

        for enemy in self.enemies:
            enemy.update(self.player, self.game_map, all_enemies)

        for enemy in self.ranged_enemies:
            enemy.update(self.player, self.game_map, all_enemies)
        
        all_enemies_full = self.enemies + self.ranged_enemies + self.bosses
        for boss in self.bosses:
            boss.update(self.player, self.game_map, all_enemies_full)

        if self.weapon is not None:
            for box in self.ammo_boxes:
                box.try_pickup(self.player, self.weapon)

        for box in self.ammo_boxes:
            if box.active:
                box.update_bob()

        for box in self.heal_boxes:
            box.try_pickup(self.player)
            if box.active:
                box.update_bob()


    def render(self, screen):
        sprites = []
        for e in self.enemies:
            if e.alive:
                sprites.append(("enemy", e))
        for e in self.ranged_enemies:
            if e.alive:
                sprites.append(("ranged", e))
                # i proiettili di questo nemico
                for p in e.projectiles:
                    if p.active:
                        sprites.append(("projectile", p))
        for b in self.ammo_boxes:
            if b.active:
                sprites.append(("ammo", b))
        for b in self.bosses:
            if b.alive:
                sprites.append(("boss", b))
        for b in self.heal_boxes:
            if b.active:
                sprites.append(("heal", b))


        sprites.sort(key=lambda s: s[1].distance_to(self.player), reverse=True)

        for _, obj in sprites:
            self.render_sprite(screen, obj)

    def render_sprite(self, screen, obj):
        player = self.player

        obj_scale      = getattr(obj, "scale",      1.0)
        obj_y_offset   = getattr(obj, "y_offset",   0.0)
        obj_bob_offset = getattr(obj, "bob_offset",   0)   

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
            int((TILESIZE / corrected_dist) * 415 * obj_scale),   
            MAX_SPRITE_SIZE
        )
        sprite_width = sprite_height

        if sprite_width <= 0 or sprite_height <= 0:
            return

        draw_top  = (WINDOW_HEIGHT // 2 - sprite_height // 2
                   + int(sprite_height * (1 - obj_scale) / 2)
                   + int(sprite_height * obj_y_offset)
                   + obj_bob_offset)                              
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
        Colpisce sia MeleeEnemy che RangedEnemy. Ritorna True se colpisce."""
        best = None
        best_dist = float('inf')
        for enemy in self.enemies + self.ranged_enemies + self.bosses:
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
