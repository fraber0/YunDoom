import pygame
import sys
from settings import *

# ──────────────────────────────────────────────────────────────────────────────
# MAPPE DISPONIBILI
# ──────────────────────────────────────────────────────────────────────────────
MAPS = {
    "Corridoio": [
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
    ],
    "Labirinto": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "Arena": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
# DIFFICOLTÀ
# ──────────────────────────────────────────────────────────────────────────────
DIFFICULTIES = {
    "Facile":   {"move_speed": 3.5, "rot_speed": 3.0, "fov_mult": 1.0, "color": (80, 200, 120)},
    "Normale":  {"move_speed": 2.5, "rot_speed": 2.0, "fov_mult": 1.0, "color": (220, 180, 50)},
    "Difficile":{"move_speed": 1.8, "rot_speed": 1.5, "fov_mult": 0.8, "color": (220, 80,  60)},
}

# ──────────────────────────────────────────────────────────────────────────────
# MINIMAP PREVIEW
# ──────────────────────────────────────────────────────────────────────────────
def _draw_minimap(surface, rect, grid):
    rows = len(grid)
    cols = len(grid[0])
    cell_w = rect.width  / cols
    cell_h = rect.height / rows
    pygame.draw.rect(surface, (10, 10, 20), rect)
    for r in range(rows):
        for c in range(cols):
            color = (40, 40, 60) if grid[r][c] == 1 else (160, 160, 200)
            x = rect.x + int(c * cell_w)
            y = rect.y + int(r * cell_h)
            pygame.draw.rect(surface, color, (x + 1, y + 1, int(cell_w) - 1, int(cell_h) - 1))
    pygame.draw.rect(surface, (100, 100, 160), rect, 1)


# ──────────────────────────────────────────────────────────────────────────────
# SCHERMATA DI LOBBY
# ──────────────────────────────────────────────────────────────────────────────
def run_lobby(screen):
    """
    Mostra il menu di selezione difficoltà + mappa.
    Ritorna (difficulty_key, map_key) oppure None se si torna indietro.
    """
    clock = pygame.time.Clock()

    # palette
    C_BG       = (15, 15, 25)
    C_TITLE    = (220, 180, 50)
    C_BORDER   = (100, 100, 160)
    C_BTN      = (40, 40, 60)
    C_BTN_HOV  = (70, 70, 110)
    C_SEL      = (80, 100, 180)
    C_WHITE    = (255, 255, 255)
    C_GREY     = (160, 160, 160)
    C_HINT     = (80, 80, 100)

    font_title  = pygame.font.SysFont("consolas", 46, bold=True)
    font_sec    = pygame.font.SysFont("consolas", 22, bold=True)
    font_btn    = pygame.font.SysFont("consolas", 24, bold=True)
    font_small  = pygame.font.SysFont("consolas", 18)

    cx = WINDOW_WIDTH  // 2
    cy = WINDOW_HEIGHT // 2

    diff_keys = list(DIFFICULTIES.keys())
    map_keys  = list(MAPS.keys())

    sel_diff = 1   # indice default → "Normale"
    sel_map  = 0   # indice default → prima mappa

    # layout colonne
    LEFT_X  = 60
    RIGHT_X = WINDOW_WIDTH // 2 + 30
    ROW_Y   = 130
    BTN_H   = 46
    BTN_GAP = 14
    BTN_W   = WINDOW_WIDTH // 2 - 90

    # bottone AVVIA
    start_w, start_h = 260, 52
    btn_start = pygame.Rect(cx - start_w // 2, WINDOW_HEIGHT - 95, start_w, start_h)
    # bottone INDIETRO
    back_w, back_h = 160, 40
    btn_back  = pygame.Rect(20, WINDOW_HEIGHT - 60, back_w, back_h)

    # minimap area
    mini_size = 150
    mini_rect = pygame.Rect(RIGHT_X, ROW_Y + 3 * (BTN_H + BTN_GAP) + 40, mini_size, mini_size)

    scanline_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for y in range(0, WINDOW_HEIGHT, 4):
        pygame.draw.line(scanline_surf, (0, 0, 0, 40), (0, y), (WINDOW_WIDTH, y))

    tick = 0

    while True:
        clock.tick(60)
        tick += 1
        mouse = pygame.mouse.get_pos()

        # ── eventi ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_RETURN:
                    return diff_keys[sel_diff], map_keys[sel_map]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # difficoltà
                for i in range(len(diff_keys)):
                    r = _diff_rect(i, LEFT_X, ROW_Y, BTN_W, BTN_H, BTN_GAP)
                    if r.collidepoint(mouse):
                        sel_diff = i
                # mappe
                for i in range(len(map_keys)):
                    r = _map_rect(i, RIGHT_X, ROW_Y, BTN_W, BTN_H, BTN_GAP)
                    if r.collidepoint(mouse):
                        sel_map = i
                # bottoni
                if btn_start.collidepoint(mouse):
                    return diff_keys[sel_diff], map_keys[sel_map]
                if btn_back.collidepoint(mouse):
                    return None

        # ── disegno ─────────────────────────────────────────────────────────
        screen.fill(C_BG)
        _draw_perspective_grid(screen, tick)
        screen.blit(scanline_surf, (0, 0))

        # titolo
        t = font_title.render("NUOVA PARTITA", True, C_TITLE)
        screen.blit(t, t.get_rect(center=(cx, 60)))
        pygame.draw.line(screen, C_BORDER, (40, 90), (WINDOW_WIDTH - 40, 90), 1)

        # ── sezione DIFFICOLTÀ ───────────────────────────────────────────────
        sec = font_sec.render("DIFFICOLTÀ", True, C_GREY)
        screen.blit(sec, (LEFT_X, ROW_Y - 28))

        for i, key in enumerate(diff_keys):
            r     = _diff_rect(i, LEFT_X, ROW_Y, BTN_W, BTN_H, BTN_GAP)
            hover = r.collidepoint(mouse)
            is_sel = (i == sel_diff)
            diff_color = DIFFICULTIES[key]["color"]

            bg = C_SEL if is_sel else (C_BTN_HOV if hover else C_BTN)
            pygame.draw.rect(screen, bg, r, border_radius=7)
            border_col = diff_color if is_sel else C_BORDER
            pygame.draw.rect(screen, border_col, r, 2, border_radius=7)

            # pallino colore difficoltà
            pygame.draw.circle(screen, diff_color, (r.x + 22, r.centery), 7)

            label = font_btn.render(key, True, C_WHITE if is_sel else C_GREY)
            screen.blit(label, label.get_rect(midleft=(r.x + 40, r.centery)))

            if is_sel:
                d = DIFFICULTIES[key]
                info = font_small.render(
                    f"vel {d['move_speed']}  rot {d['rot_speed']}  fov ×{d['fov_mult']}",
                    True, diff_color)
                screen.blit(info, info.get_rect(midright=(r.right - 10, r.centery)))

        # ── sezione MAPPA ────────────────────────────────────────────────────
        sec2 = font_sec.render("MAPPA", True, C_GREY)
        screen.blit(sec2, (RIGHT_X, ROW_Y - 28))

        for i, key in enumerate(map_keys):
            r     = _map_rect(i, RIGHT_X, ROW_Y, BTN_W, BTN_H, BTN_GAP)
            hover = r.collidepoint(mouse)
            is_sel = (i == sel_map)

            bg = C_SEL if is_sel else (C_BTN_HOV if hover else C_BTN)
            pygame.draw.rect(screen, bg, r, border_radius=7)
            border_col = C_TITLE if is_sel else C_BORDER
            pygame.draw.rect(screen, border_col, r, 2, border_radius=7)

            label = font_btn.render(key, True, C_WHITE if is_sel else C_GREY)
            screen.blit(label, label.get_rect(midleft=(r.x + 16, r.centery)))

        # minimap anteprima
        _draw_minimap(screen, mini_rect, MAPS[map_keys[sel_map]])
        lbl = font_small.render("Anteprima", True, C_GREY)
        screen.blit(lbl, lbl.get_rect(centerx=mini_rect.centerx, top=mini_rect.bottom + 6))

        # ── bottone AVVIA ────────────────────────────────────────────────────
        s_hov = btn_start.collidepoint(mouse)
        pygame.draw.rect(screen, (60, 110, 60) if s_hov else (35, 75, 35), btn_start, border_radius=8)
        pygame.draw.rect(screen, (80, 200, 80), btn_start, 2, border_radius=8)
        st = font_btn.render("▶  AVVIA", True, C_WHITE)
        screen.blit(st, st.get_rect(center=btn_start.center))

        # ── bottone INDIETRO ─────────────────────────────────────────────────
        b_hov = btn_back.collidepoint(mouse)
        pygame.draw.rect(screen, C_BTN_HOV if b_hov else C_BTN, btn_back, border_radius=7)
        pygame.draw.rect(screen, C_BORDER, btn_back, 2, border_radius=7)
        bt = font_btn.render("← MENU", True, C_GREY)
        screen.blit(bt, bt.get_rect(center=btn_back.center))

        hint = font_small.render("[INVIO] avvia  •  [ESC] indietro", True, C_HINT)
        screen.blit(hint, hint.get_rect(center=(cx, WINDOW_HEIGHT - 18)))

        pygame.display.update()


# ── helpers rect ──────────────────────────────────────────────────────────────
def _diff_rect(i, left_x, row_y, btn_w, btn_h, gap):
    return pygame.Rect(left_x, row_y + i * (btn_h + gap), btn_w, btn_h)

def _map_rect(i, right_x, row_y, btn_w, btn_h, gap):
    return pygame.Rect(right_x, row_y + i * (btn_h + gap), btn_w, btn_h)


# ──────────────────────────────────────────────────────────────────────────────
# griglia decorativa (copiata da menu.py per essere autonomo)
# ──────────────────────────────────────────────────────────────────────────────
def _draw_perspective_grid(screen, tick):
    color = (30, 30, 50)
    cx = WINDOW_WIDTH  // 2
    cy = WINDOW_HEIGHT // 2
    for i in range(1, 9):
        y_top  = cy - (cy * i // 9)
        y_bot  = cy + (cy * i // 9)
        spread = WINDOW_WIDTH * i // 9
        pygame.draw.line(screen, color, (cx - spread // 2, y_top), (cx + spread // 2, y_top))
        pygame.draw.line(screen, color, (cx - spread // 2, y_bot), (cx + spread // 2, y_bot))
    for i in range(11):
        x = int(WINDOW_WIDTH * i / 10)
        pygame.draw.line(screen, color, (x, 0),             (cx, cy))
        pygame.draw.line(screen, color, (x, WINDOW_HEIGHT), (cx, cy))