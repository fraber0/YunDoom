import pygame
from settings import *
from map import Map
from player import Player
from raycaster import Raycaster
from menu import run_menu
from lobby import run_lobby, MAPS, DIFFICULTIES
from object_manager import ObjectManager
from weapon import Weapon
from audio_manager import AudioManager
 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Raycaster")


def _draw_hud(screen, player):
    bar_w, bar_h = 200, 18
    bar_x, bar_y = 10, WINDOW_HEIGHT - 30
    ratio = max(0, player.hp / player.max_hp)
    pygame.draw.rect(screen, (60, 20, 20),  (bar_x, bar_y, bar_w, bar_h), border_radius=4)
    col = (60, 200, 60) if ratio > 0.5 else (220, 180, 50) if ratio > 0.25 else (220, 60, 60)
    pygame.draw.rect(screen, col, (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=4)
    pygame.draw.rect(screen, (180, 180, 180), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=4)
    fnt = pygame.font.SysFont("consolas", 15, bold=True)
    txt = fnt.render(f"HP  {player.hp} / {player.max_hp}", True, (255, 255, 255))
    screen.blit(txt, (bar_x + 4, bar_y + 2))
 
while True:   # loop: permette di tornare al menu dopo una partita

    audio = AudioManager()
    audio.play("menu")
 
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
    
    weapon = Weapon("./Assets/weapon/shotgun")
    
    obj_manager = ObjectManager(player, raycaster, game_map=game_map, weapon=weapon)
    cx = len(map_grid[0]) * TILESIZE // 2   # centro x della mappa
    cy = len(map_grid)    * TILESIZE // 2   # centro y della mappa
    obj_manager.add_enemy(cx, cy, "./Assets/enemy.png", scale=0.4, y_offset=-0.2)
    obj_manager.spawn_ammo_boxes("./Assets/ammo_box.png", count=5)
    
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
                
            # ── evento sparo ──
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not weapon.is_shooting:
                    weapon.shoot()
                    obj_manager.try_shoot()
 
        pygame.mixer.music.stop()

        player.update()
        raycaster.castAllRays()
 
        screen.fill((0, 0, 0))
        half = WINDOW_HEIGHT // 2
        screen.blit(pygame.transform.scale(sky, (WINDOW_WIDTH, half)), (0, 0))
        pygame.draw.rect(screen, floor_color, (0, half, WINDOW_WIDTH, half))
        raycaster.render(screen)
        obj_manager.render(screen)
        obj_manager.update()
        
        
        
        
        weapon.update()
        
        weapon.render(screen)
        
        # HUD: difficoltà + mappa in alto a sinistra
        fnt = pygame.font.SysFont("consolas", 16)
        hud = fnt.render(f"{map_key}  |  {diff_key}  |  [ESC] menu", True, (200, 200, 200))
        screen.blit(hud, (8, 6))
 
        # HUD vita player
        _draw_hud(screen, player)

        # Crosshair
        cx = WINDOW_WIDTH  // 2
        cy = WINDOW_HEIGHT // 2
        length, gap, thick = 12, 4, 2
        col = (255, 255, 255)
        pygame.draw.rect(screen, col, (cx - length - gap, cy - thick//2, length, thick))  # sx
        pygame.draw.rect(screen, col, (cx + gap,          cy - thick//2, length, thick))  # dx
        pygame.draw.rect(screen, col, (cx - thick//2, cy - length - gap, thick, length))  # su
        pygame.draw.rect(screen, col, (cx - thick//2, cy + gap,          thick, length))  # giù

        pygame.display.update()

        
