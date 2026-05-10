import pygame
from settings import *
from map import Map
from player import Player
from raycaster import Raycaster
from menu import run_menu
from lobby import run_lobby, MAPS, DIFFICULTIES
 
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Raycaster")
 
while True:   # loop: permette di tornare al menu dopo una partita
 
    # ── MENU PRINCIPALE ────────────────────────────────────────────────────────
    run_menu(screen)
 
    # ── LOBBY (difficoltà + mappa) ─────────────────────────────────────────────
    result = run_lobby(screen)
    if result is None:
        continue   # il giocatore è tornato indietro → rimostro il menu
 
    diff_key, map_key = result
    diff_cfg = DIFFICULTIES[diff_key]
    map_grid = MAPS[map_key]
 
    # ── SETUP GIOCO ────────────────────────────────────────────────────────────
    game_map   = Map(grid=map_grid)
    player     = Player(
        move_speed = diff_cfg["move_speed"],
        rot_speed  = diff_cfg["rot_speed"] * (__import__("math").pi / 180),
        game_map   = game_map,
    )
    raycaster  = Raycaster(player, game_map)
    clock      = pygame.time.Clock()
 
    sky   = pygame.image.load("./Assets/360_F_99890228_xRXJFnENLpAHdl82Y5LrRg11RwWMb5KO.jpg").convert()
    floor_color = (50, 150, 50)
 
    # ── GAME LOOP ──────────────────────────────────────────────────────────────
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   # torna al menu principale
 
        player.update()
        raycaster.castAllRays()
 
        screen.fill((0, 0, 0))
        half = WINDOW_HEIGHT // 2
        screen.blit(pygame.transform.scale(sky, (WINDOW_WIDTH, half)), (0, 0))
        pygame.draw.rect(screen, floor_color, (0, half, WINDOW_WIDTH, half))
        raycaster.render(screen)
 
        # HUD: difficoltà + mappa in alto a sinistra
        fnt = pygame.font.SysFont("consolas", 16)
        hud = fnt.render(f"{map_key}  |  {diff_key}  |  [ESC] menu", True, (200, 200, 200))
        screen.blit(hud, (8, 6))
 
        pygame.display.update()