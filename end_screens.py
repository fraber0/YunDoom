import pygame
import sys
import math
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _load_image_safe(path: str | None) -> pygame.Surface | None:
    if not path:
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except (pygame.error, FileNotFoundError, TypeError):
        print(f"[end_screens] immagine non trovata: {path!r}")
        return None


def _load_sound_safe(path: str | None) -> pygame.mixer.Sound | None:
    if not path:
        return None
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError, TypeError):
        print(f"[end_screens] suono non trovato: {path!r}")
        return None


def _stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def _draw_scanlines(surface: pygame.Surface, alpha: int = 35):
    for y in range(0, surface.get_height(), 3):
        pygame.draw.line(surface, (0, 0, 0, alpha),
                         (0, y), (surface.get_width(), y))


def _draw_particles(screen, particles: list, color: tuple):
    for p in particles:
        pygame.draw.circle(screen, color,
                           (int(p["x"]), int(p["y"])), p["r"])

        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] -= 0.03
        p["r"] = max(0, p["r"] - 0.02)

        if p["y"] < -10 or p["r"] <= 0:
            p["y"] = WINDOW_HEIGHT + 10
            p["x"] = __import__("random").randint(0, WINDOW_WIDTH)
            p["r"] = __import__("random").uniform(1.5, 4.0)
            p["vy"] = __import__("random").uniform(-0.8, -0.3)
            p["vx"] = __import__("random").uniform(-0.4, 0.4)


def _make_particles(n: int) -> list:
    import random
    return [
        {
            "x": random.randint(0, WINDOW_WIDTH),
            "y": random.randint(0, WINDOW_HEIGHT),
            "vx": random.uniform(-0.4, 0.4),
            "vy": random.uniform(-1.2, -0.3),
            "r": random.uniform(1.5, 4.5),
        }
        for _ in range(n)
    ]


def _draw_btn(screen, rect: pygame.Rect, label: str,
              font: pygame.font.Font,
              hovered: bool,
              base_col, hover_col, border_col, text_col):

    pygame.draw.rect(
        screen,
        hover_col if hovered else base_col,
        rect,
        border_radius=8
    )
    pygame.draw.rect(screen, border_col, rect, 2, border_radius=8)

    surf = font.render(label, True, text_col)
    screen.blit(surf, surf.get_rect(center=rect.center))


# ─────────────────────────────────────────────────────────────
# VITTORIA
# ─────────────────────────────────────────────────────────────

def run_victory(
    screen: pygame.Surface,
    image_path: str | None = None,
    sound_path: str | None = None,
    sound_volume: float = 0.7,
) -> str:

    _stop_music()

    bg_image = _load_image_safe(image_path)
    sound = _load_sound_safe(sound_path)

    if sound:
        sound.set_volume(sound_volume)
        sound.play(loops=-1)

    C_BG = (10, 18, 10)
    C_GOLD = (255, 210, 50)
    C_GOLD2 = (200, 160, 20)
    C_GREEN = (60, 200, 80)
    C_WHITE = (255, 255, 255)
    C_BTN = (30, 50, 30)
    C_BTN_HOV = (55, 90, 55)
    C_BTN_RED = (60, 20, 20)
    C_BTN_RHOV = (100, 35, 35)
    C_BORDER = (80, 160, 80)

    font_big = pygame.font.SysFont("consolas", 72, bold=True)
    font_sub = pygame.font.SysFont("consolas", 26)
    font_btn = pygame.font.SysFont("consolas", 28, bold=True)
    font_small = pygame.font.SysFont("consolas", 18)

    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2

    btn_w, btn_h = 240, 52
    btn_menu = pygame.Rect(cx - btn_w - 20, cy + 140, btn_w, btn_h)
    btn_quit = pygame.Rect(cx + 20, cy + 140, btn_w, btn_h)

    particles = _make_particles(80)

    scanline_surf = pygame.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.SRCALPHA
    )
    _draw_scanlines(scanline_surf, alpha=28)

    clock = pygame.time.Clock()
    tick = 0

    while True:
        clock.tick(60)
        tick += 1
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if sound: sound.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    if sound: sound.stop()
                    return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_menu.collidepoint(mouse):
                    if sound: sound.stop()
                    return "menu"
                if btn_quit.collidepoint(mouse):
                    if sound: sound.stop()
                    pygame.quit()
                    sys.exit()

        screen.fill(C_BG)

        if bg_image:
            scaled = pygame.transform.scale(
                bg_image,
                (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            scaled.set_alpha(120)
            screen.blit(scaled, (0, 0))

        else:
            for i in range(24):
                angle = (i / 24) * 2 * math.pi + tick * 0.003
                ex = cx + math.cos(angle) * WINDOW_WIDTH
                ey = cy + math.sin(angle) * WINDOW_HEIGHT
                col_v = max(0, 40 - i)
                pygame.draw.line(
                    screen,
                    (col_v, col_v // 2, 0),
                    (cx, cy),
                    (int(ex), int(ey)),
                    1
                )

        screen.blit(scanline_surf, (0, 0))

        _draw_particles(screen, particles, C_GOLD2)

        overlay = pygame.Surface((620, 320), pygame.SRCALPHA)
        overlay.fill((10, 25, 10, 180))
        pygame.draw.rect(
            overlay,
            (*C_BORDER, 200),
            overlay.get_rect(),
            2,
            border_radius=12
        )
        screen.blit(overlay, overlay.get_rect(center=(cx, cy)))

        pulse = 1.0 + 0.04 * math.sin(tick * 0.07)
        title_surf = font_big.render("VITTORIA!", True, C_GOLD)
        tw = int(title_surf.get_width() * pulse)
        th = int(title_surf.get_height() * pulse)
        title_scaled = pygame.transform.scale(title_surf, (tw, th))
        screen.blit(title_scaled, title_scaled.get_rect(center=(cx, cy - 70)))

        sub = font_sub.render("Hai eliminato tutti i nemici!", True, C_GREEN)
        screen.blit(sub, sub.get_rect(center=(cx, cy - 5)))

        _draw_btn(screen, btn_menu, "MENU PRINCIPALE", font_btn,
                  btn_menu.collidepoint(mouse),
                  C_BTN, C_BTN_HOV, C_BORDER, C_WHITE)

        _draw_btn(screen, btn_quit, "ESCI DAL GIOCO", font_btn,
                  btn_quit.collidepoint(mouse),
                  C_BTN_RED, C_BTN_RHOV, (180, 60, 60), (255, 160, 160))

        hint = font_small.render("[INVIO / ESC] torna al menu", True, (70, 100, 70))
        screen.blit(hint, hint.get_rect(center=(cx, WINDOW_HEIGHT - 20)))

        pygame.display.update()


# ─────────────────────────────────────────────────────────────
# SCONFITTA
# ─────────────────────────────────────────────────────────────

def run_defeat(
    screen: pygame.Surface,
    image_path: str | None = None,
    sound_path: str | None = None,
    sound_volume: float = 0.6,
) -> str:

    _stop_music()

    bg_image = _load_image_safe(image_path)
    sound = _load_sound_safe(sound_path)

    if sound:
        sound.set_volume(sound_volume)
        sound.play(loops=-1)

    C_BG = (12, 5, 5)
    C_RED = (220, 40, 40)
    C_RED2 = (160, 20, 20)
    C_ORANGE = (220, 120, 40)
    C_BTN = (50, 20, 20)
    C_BTN_HOV = (90, 35, 35)
    C_BTN_GRN = (20, 50, 20)
    C_BTN_GHOV = (35, 90, 35)
    C_BORDER = (140, 40, 40)

    font_big = pygame.font.SysFont("consolas", 72, bold=True)
    font_sub = pygame.font.SysFont("consolas", 26)
    font_btn = pygame.font.SysFont("consolas", 28, bold=True)
    font_small = pygame.font.SysFont("consolas", 18)

    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2

    btn_w, btn_h = 240, 52
    btn_menu = pygame.Rect(cx - btn_w - 20, cy + 140, btn_w, btn_h)
    btn_quit = pygame.Rect(cx + 20, cy + 140, btn_w, btn_h)

    particles = _make_particles(60)
    for p in particles:
        p["vy"] = abs(p["vy"]) * 1.5
        p["r"] *= 1.2

    scanline_surf = pygame.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.SRCALPHA
    )
    _draw_scanlines(scanline_surf, alpha=45)

    clock = pygame.time.Clock()
    tick = 0

    fade_frames = 40
    fade_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surf.fill((180, 0, 0))

    while True:
        clock.tick(60)
        tick += 1
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if sound: sound.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    if sound: sound.stop()
                    return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_menu.collidepoint(mouse):
                    if sound: sound.stop()
                    return "menu"
                if btn_quit.collidepoint(mouse):
                    if sound: sound.stop()
                    pygame.quit()
                    sys.exit()

        screen.fill(C_BG)

        if bg_image:
            scaled = pygame.transform.scale(
                bg_image,
                (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            scaled.set_alpha(110)
            screen.blit(scaled, (0, 0))

        screen.blit(scanline_surf, (0, 0))

        for p in particles:
            pygame.draw.circle(
                screen,
                C_RED2,
                (int(p["x"]), int(p["y"])),
                max(1, int(p["r"]))
            )
            p["x"] += p["vx"]
            p["y"] += abs(p["vy"])

            if p["y"] > WINDOW_HEIGHT + 10:
                import random
                p["y"] = -5
                p["x"] = random.randint(0, WINDOW_WIDTH)
                p["r"] = random.uniform(1.5, 4.5)

        if tick <= fade_frames:
            alpha = int(180 * (1 - tick / fade_frames))
            fade_surf.set_alpha(alpha)
            screen.blit(fade_surf, (0, 0))

        overlay = pygame.Surface((620, 320), pygame.SRCALPHA)
        overlay.fill((25, 5, 5, 190))
        pygame.draw.rect(
            overlay,
            (*C_BORDER, 200),
            overlay.get_rect(),
            2,
            border_radius=12
        )
        screen.blit(overlay, overlay.get_rect(center=(cx, cy)))

        import random as _rnd
        shake_x = _rnd.randint(-1, 1) if tick < 90 else 0
        shake_y = _rnd.randint(-1, 1) if tick < 90 else 0

        title_surf = font_big.render("SCONFITTA", True, C_RED)
        screen.blit(title_surf, title_surf.get_rect(center=(cx + shake_x, cy - 70 + shake_y)))

        sub_col = C_ORANGE if (tick // 20) % 2 == 0 else (200, 80, 30)
        sub = font_sub.render("Sei stato eliminato...", True, sub_col)
        screen.blit(sub, sub.get_rect(center=(cx, cy - 5)))

        _draw_btn(screen, btn_menu, "RIPROVA / MENU", font_btn,
                  btn_menu.collidepoint(mouse),
                  C_BTN_GRN, C_BTN_GHOV, (60, 160, 60), (255, 255, 255))

        _draw_btn(screen, btn_quit, "ESCI DAL GIOCO", font_btn,
                  btn_quit.collidepoint(mouse),
                  C_BTN, C_BTN_HOV, C_BORDER, (255, 160, 160))

        hint = font_small.render("[INVIO / ESC] torna al menu", True, (100, 40, 40))
        screen.blit(hint, hint.get_rect(center=(cx, WINDOW_HEIGHT - 20)))

        pygame.display.update()
