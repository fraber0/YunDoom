import math
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Weapon:
    SHOOT_FRAME_DURATION = 5

    @property
    def is_shooting(self) -> bool:
        return self._shooting

    def __init__(
        self,
        sprite_dir: str,
        scale: float = 0.45,
        bob_speed: float = 0.15,
        bob_amount: int = 8,
        shoot_frames: int = 5,
        max_ammo: int = 30,
        start_ammo: int = 10,
    ):
        self.frames = []
        for i in range(shoot_frames + 1):
            raw = pygame.image.load(f"{sprite_dir}/{i}.png").convert_alpha()
            target_h = int(WINDOW_HEIGHT * scale)
            target_w = int(target_h * (raw.get_width() / raw.get_height()))
            self.frames.append(pygame.transform.scale(raw, (target_w, target_h)))

        self.base_x = (WINDOW_WIDTH  - self.frames[0].get_width())  // 2
        self.base_y =  WINDOW_HEIGHT - self.frames[0].get_height() + 8 

        self.bob_speed  = bob_speed
        self.bob_amount = bob_amount
        self._bob_tick  = 0.0
        self._bob_y     = 0

        self._shoot_frames    = shoot_frames
        self._shooting        = False
        self._shoot_frame_idx = 0
        self._shoot_tick      = 0
        self._recoil_y        = 0
        self._current_frame   = 0

        # ── MUNIZIONI ──────────────────────────────────────────────────────────
        self.max_ammo  = max_ammo
        self.ammo      = start_ammo

        self._hud_font = pygame.font.SysFont("consolas", 22, bold=True)

        self.shoot_sound = pygame.mixer.Sound(
            "./Assets/sounds/shoot.mp3"
        )
        self.shoot_sound.set_volume(0.2)

    def shoot(self):
        if not self._shooting and self.ammo > 0:
            self.ammo -= 1
            self._shooting        = True
            self._shoot_frame_idx = 0
            self._shoot_tick      = 0
            self._current_frame   = 1
            self.shoot_sound.play()

    def update(self):
        self._update_bob()
        self._update_shoot()

    def render(self, screen: pygame.Surface):
        x = self.base_x
        y = self.base_y + self._bob_y + self._recoil_y
        screen.blit(self.frames[self._current_frame], (x, y))
        self._render_ammo_hud(screen)

    def _render_ammo_hud(self, screen: pygame.Surface):
        """Disegna le munizioni in basso a destra."""
        color = (220, 180, 50) if self.ammo > 0 else (220, 60, 60)
        text  = self._hud_font.render(f"AMMO  {self.ammo:02d} / {self.max_ammo:02d}", True, color)
        x = WINDOW_WIDTH  - text.get_width()  - 12
        y = WINDOW_HEIGHT - text.get_height() - 10
        screen.blit(text, (x, y))

    def reload(self, amount: int):
        """Aggiunge `amount` munizioni senza superare il massimo."""
        self.ammo = min(self.ammo + amount, self.max_ammo)

    def _update_bob(self):
        keys = pygame.key.get_pressed()
        is_moving = (
            keys[pygame.K_w] or keys[pygame.K_s]
            or keys[pygame.K_a] or keys[pygame.K_d]
            or keys[pygame.K_UP] or keys[pygame.K_DOWN]
        )
        if is_moving:
            self._bob_tick += self.bob_speed
        else:
            self._bob_tick *= 0.85

        self._bob_y = int(math.sin(self._bob_tick) * self.bob_amount)

    def _update_shoot(self):
        if not self._shooting:
            self._current_frame = 0
            self._recoil_y = 0
            return

        self._shoot_tick += 1
        if self._shoot_tick >= self.SHOOT_FRAME_DURATION:
            self._shoot_tick       = 0
            self._shoot_frame_idx += 1
            self._current_frame = min(self._shoot_frame_idx, len(self.frames) - 1)

        total = self._shoot_frames * self.SHOOT_FRAME_DURATION
        half  = total // 2
        tick  = self._shoot_frame_idx * self.SHOOT_FRAME_DURATION + self._shoot_tick

        if tick <= half:
            self._recoil_y = int((tick / half) * 40)
        else:
            self._recoil_y = int(((total - tick) / half) * 40)

        if self._shoot_frame_idx >= self._shoot_frames:
            self._shooting      = False
            self._recoil_y      = 0
            self._current_frame = 0
