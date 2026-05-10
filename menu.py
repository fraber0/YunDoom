import pygame
import sys
from settings import *
 
def run_menu(screen):
    """
    Mostra il menu di avvio. Ritorna True se il giocatore vuole iniziare,
    False se vuole uscire.
    """
    clock = pygame.time.Clock()
 
    # Colori
    COLOR_BG        = (15, 15, 25)
    COLOR_TITLE     = (220, 180, 50)
    COLOR_SUBTITLE  = (180, 180, 180)
    COLOR_BTN       = (40, 40, 60)
    COLOR_BTN_HOVER = (70, 70, 110)
    COLOR_BTN_TEXT  = (255, 255, 255)
    COLOR_QUIT_TEXT = (180, 80, 80)
    COLOR_BORDER    = (100, 100, 160)
 
    font_title    = pygame.font.SysFont("consolas", 64, bold=True)
    font_subtitle = pygame.font.SysFont("consolas", 22)
    font_btn      = pygame.font.SysFont("consolas", 30, bold=True)
 
    # Bottoni
    btn_w, btn_h = 260, 55
    center_x = WINDOW_WIDTH // 2
    btn_play  = pygame.Rect(center_x - btn_w // 2, WINDOW_HEIGHT // 2 + 20,  btn_w, btn_h)
    btn_info  = pygame.Rect(center_x - btn_w // 2, WINDOW_HEIGHT // 2 + 100, btn_w, btn_h)
    btn_quit  = pygame.Rect(center_x - btn_w // 2, WINDOW_HEIGHT // 2 + 180, btn_w, btn_h)
 
    # Effetto "scanlines"
    scanline_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for y in range(0, WINDOW_HEIGHT, 4):
        pygame.draw.line(scanline_surf, (0, 0, 0, 40), (0, y), (WINDOW_WIDTH, y))
 
    tick = 0
 
    while True:
        clock.tick(60)
        tick += 1
        mouse_pos = pygame.mouse.get_pos()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.collidepoint(mouse_pos):
                    return True
                if btn_info.collidepoint(mouse_pos):
                    run_instructions(screen)
                if btn_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
 
        # --- SFONDO ---
        screen.fill(COLOR_BG)
        _draw_perspective_grid(screen, tick)
        screen.blit(scanline_surf, (0, 0))
 
        # --- TITOLO ---
        title_surf = font_title.render("RAYCASTER", True, COLOR_TITLE)
        alpha = 200 + int(55 * abs(pygame.math.Vector2(1, 0).rotate(tick * 2).x))
        title_surf.set_alpha(min(alpha, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(center_x, WINDOW_HEIGHT // 2 - 90)))
 
        subtitle_surf = font_subtitle.render("usa le frecce per muoverti", True, COLOR_SUBTITLE)
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(center_x, WINDOW_HEIGHT // 2 - 30)))
 
        # --- BOTTONE PLAY ---
        play_hover = btn_play.collidepoint(mouse_pos)
        pygame.draw.rect(screen, COLOR_BTN_HOVER if play_hover else COLOR_BTN, btn_play, border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDER, btn_play, 2, border_radius=8)
        play_txt = font_btn.render("▶  GIOCA", True, COLOR_BTN_TEXT)
        screen.blit(play_txt, play_txt.get_rect(center=btn_play.center))
 
        # --- BOTTONE ISTRUZIONI ---
        info_hover = btn_info.collidepoint(mouse_pos)
        pygame.draw.rect(screen, COLOR_BTN_HOVER if info_hover else COLOR_BTN, btn_info, border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDER, btn_info, 2, border_radius=8)
        info_txt = font_btn.render("?  ISTRUZIONI", True, COLOR_BTN_TEXT)
        screen.blit(info_txt, info_txt.get_rect(center=btn_info.center))
 
        # --- BOTTONE QUIT ---
        quit_hover = btn_quit.collidepoint(mouse_pos)
        pygame.draw.rect(screen, COLOR_BTN_HOVER if quit_hover else COLOR_BTN, btn_quit, border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDER, btn_quit, 2, border_radius=8)
        quit_txt = font_btn.render("✕  ESCI", True, COLOR_QUIT_TEXT)
        screen.blit(quit_txt, quit_txt.get_rect(center=btn_quit.center))
 
        # --- HINT TASTIERA ---
        hint = font_subtitle.render("[INVIO] per iniziare  •  [ESC] per uscire", True, (80, 80, 100))
        screen.blit(hint, hint.get_rect(center=(center_x, WINDOW_HEIGHT - 30)))
 
        pygame.display.update()
 
 
def run_instructions(screen):
    """Schermata con i comandi di gioco. Torna al menu premendo ESC o il bottone."""
    clock = pygame.time.Clock()
 
    COLOR_BG      = (15, 15, 25)
    COLOR_TITLE   = (220, 180, 50)
    COLOR_BORDER  = (100, 100, 160)
    COLOR_BTN     = (40, 40, 60)
    COLOR_BTN_HOV = (70, 70, 110)
    COLOR_KEY     = (220, 180, 50)
    COLOR_DESC    = (200, 200, 200)
 
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_cmd   = pygame.font.SysFont("consolas", 24, bold=True)
    font_desc  = pygame.font.SysFont("consolas", 24)
    font_hint  = pygame.font.SysFont("consolas", 20)
    font_btn   = pygame.font.SysFont("consolas", 28, bold=True)
 
    commands = [
        ("↑",       "Avanza"),
        ("↓",       "Indietreggia"),
        ("←",       "Ruota a sinistra"),
        ("→",       "Ruota a destra"),
        ("ESC",     "Esci dal gioco"),
        ("[INVIO]", "Avvia la partita dal menu"),
    ]
 
    center_x = WINDOW_WIDTH // 2
 
    btn_w, btn_h = 220, 48
    btn_back = pygame.Rect(center_x - btn_w // 2, WINDOW_HEIGHT - 80, btn_w, btn_h)
 
    scanline_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for y in range(0, WINDOW_HEIGHT, 4):
        pygame.draw.line(scanline_surf, (0, 0, 0, 40), (0, y), (WINDOW_WIDTH, y))
 
    box_w = 500
    box_h = 30 + len(commands) * 44 + 10
    box_x = center_x - box_w // 2
    box_y = WINDOW_HEIGHT // 2 - box_h // 2 + 20
 
    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.collidepoint(mouse_pos):
                    return
 
        # --- SFONDO ---
        screen.fill(COLOR_BG)
        _draw_perspective_grid(screen, 0)
        screen.blit(scanline_surf, (0, 0))
 
        # --- TITOLO ---
        title_surf = font_title.render("ISTRUZIONI", True, COLOR_TITLE)
        screen.blit(title_surf, title_surf.get_rect(center=(center_x, 70)))
 
        # --- BOX COMANDI ---
        pygame.draw.rect(screen, (22, 22, 38), (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(screen, COLOR_BORDER,  (box_x, box_y, box_w, box_h), 1, border_radius=10)
 
        for idx, (key, desc) in enumerate(commands):
            row_y = box_y + 18 + idx * 44
 
            key_surf = font_cmd.render(key, True, COLOR_KEY)
            screen.blit(key_surf, key_surf.get_rect(midleft=(box_x + 30, row_y + 12)))
 
            sep_x = box_x + 170
            pygame.draw.line(screen, COLOR_BORDER, (sep_x, row_y + 4), (sep_x, row_y + 36))
 
            desc_surf = font_desc.render(desc, True, COLOR_DESC)
            screen.blit(desc_surf, desc_surf.get_rect(midleft=(sep_x + 20, row_y + 12)))
 
            if idx < len(commands) - 1:
                pygame.draw.line(screen, (40, 40, 60),
                                 (box_x + 10, row_y + 40), (box_x + box_w - 10, row_y + 40))
 
        # --- BOTTONE INDIETRO ---
        back_hover = btn_back.collidepoint(mouse_pos)
        pygame.draw.rect(screen, COLOR_BTN_HOV if back_hover else COLOR_BTN, btn_back, border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDER, btn_back, 2, border_radius=8)
        back_txt = font_btn.render("← INDIETRO", True, (255, 255, 255))
        screen.blit(back_txt, back_txt.get_rect(center=btn_back.center))
 
        hint = font_hint.render("[ESC] per tornare al menu", True, (80, 80, 100))
        screen.blit(hint, hint.get_rect(center=(center_x, WINDOW_HEIGHT - 20)))
 
        pygame.display.update()
 
 
def _draw_perspective_grid(screen, tick):
    """Griglia decorativa che simula un corridoio in prospettiva."""
    color = (30, 30, 50)
    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2
 
    for i in range(1, 9):
        y_top = cy - (cy * i // 9)
        y_bot = cy + (cy * i // 9)
        spread = WINDOW_WIDTH * i // 9
        pygame.draw.line(screen, color, (cx - spread // 2, y_top), (cx + spread // 2, y_top))
        pygame.draw.line(screen, color, (cx - spread // 2, y_bot), (cx + spread // 2, y_bot))
 
    num_v = 10
    for i in range(num_v + 1):
        x_edge = int(WINDOW_WIDTH * i / num_v)
        pygame.draw.line(screen, color, (x_edge, 0),    (cx, cy))
        pygame.draw.line(screen, color, (x_edge, WINDOW_HEIGHT), (cx, cy))