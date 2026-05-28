import pygame
import random
from settings import *
from map import Map
from player import Player
from raycaster import Raycaster
from menu import run_menu
from lobby import run_lobby, MAPS, DIFFICULTIES
from object_manager import ObjectManager
from weapon import Weapon
from audio_manager import AudioManager
from end_screens import run_victory, run_defeat
 
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
 
audio = AudioManager()


while True:   

    audio.play("menu")
 
    # ── MENU PRINCIPALE ────────────────────────────────────────────────────────
    run_menu(screen, audio)
 
    # ── LOBBY ─────────────────────────────────────────────
    result = run_lobby(screen)
    if result is None:
        continue   
 
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
    audio.play("game", volume=0.35)
    cx = len(map_grid[0]) * TILESIZE // 2   
    cy = len(map_grid)    * TILESIZE // 2   
    

    if diff_key == "Facile":
        spawned = []

        # Padre Maronno
        for i in range(random.randint(3, 7)):
            print(i)
           

            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_melee_enemy(sx, sy, "./Assets/PM.png",
                scale=0.5, y_offset=-0.2, speed=1.0, max_hp=50, chase_distance=400, stop_distance=60, attack_damage=10, attack_rate=120)

        # Ruffini
        for i in range(random.randint(1, 2)):
            print(i) 

            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_ranged_enemy(sx, sy, "./Assets/Ruffini.png", "./Assets/projectile.png", scale=0.6, y_offset=-0.2, speed=0.8, max_hp=25, chase_distance=500, projectile_damage=8, fire_rate=180)

        # Togni
        sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
        print(sx, sy)
        spawned.append((sx, sy))
        obj_manager.add_melee_enemy(sx, sy, "./Assets/Togni.png",
                scale=1.0, y_offset=-0.2, speed=0.7, max_hp=100, chase_distance=350, stop_distance=80, attack_damage=25, attack_rate=200)
        
        

        obj_manager.spawn_ammo_boxes("./Assets/ammo_box.png", count=8)
        obj_manager.spawn_heal_boxes("./Assets/heal_box.png", count=8)


    elif diff_key == "Normale":
        spawned = []

        # Padre Maronno
        for i in range(random.randint(5, 9)):
            print(i)
           

            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_melee_enemy(sx, sy, "./Assets/PM.png",
                scale=0.5, y_offset=-0.2, speed=1.0, max_hp=50, chase_distance=400, stop_distance=60, attack_damage=10, attack_rate=120)

        # Ruffini
        for i in range(random.randint(2, 5)):
            print(i) 

            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_ranged_enemy(sx, sy, "./Assets/Ruffini.png", "./Assets/projectile.png", scale=0.6, y_offset=-0.2, speed=0.8, max_hp=25, chase_distance=500, projectile_damage=8, fire_rate=180)

        # Togni
        for i in range(random.randint(1, 3)):
            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_melee_enemy(sx, sy, "./Assets/Togni.png",
                    scale=1.0, y_offset=-0.2, speed=0.7, max_hp=100, chase_distance=350, stop_distance=80, attack_damage=25, attack_rate=200)


        # Boss
        sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
        print(sx, sy)
        spawned.append((sx, sy))
        obj_manager.add_boss(sx, sy, "./Assets/boss.png", scale=1.0, y_offset=-0.2, speed=0.7)
        
        

        obj_manager.spawn_ammo_boxes("./Assets/ammo_box.png", count=8)
        obj_manager.spawn_heal_boxes("./Assets/heal_box.png", count=4)


    elif diff_key == "Difficile":
        spawned = []

        # Padre Maronno
        for i in range(random.randint(9, 14)):
            print(i)
           

            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_melee_enemy(sx, sy, "./Assets/PM.png",
                scale=0.5, y_offset=-0.2, speed=1.0, max_hp=50, chase_distance=400, stop_distance=60, attack_damage=10, attack_rate=120)

        # Ruffini
        for i in range(random.randint(3, 7)):
            print(i) 

            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_ranged_enemy(sx, sy, "./Assets/Ruffini.png", "./Assets/projectile.png", scale=0.6, y_offset=-0.2, speed=0.8, max_hp=26, chase_distance=600, projectile_damage=8, fire_rate=180)

        # Togni
        for i in range(random.randint(5, 9)):
            sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
            print(sx, sy)
            spawned.append((sx, sy))
            obj_manager.add_melee_enemy(sx, sy, "./Assets/Togni.png",
                    scale=1.0, y_offset=-0.2, speed=0.7, max_hp=125, chase_distance=350, stop_distance=80, attack_damage=25, attack_rate=200)


        # Boss
        sx, sy = obj_manager.random_spawn_pos(min_dist_from_player=150, occupied_positions=spawned)
        print(sx, sy)
        spawned.append((sx, sy))
        obj_manager.add_boss(sx, sy, "./Assets/boss.png", scale=1.0, y_offset=-0.2, speed=0.9)
        
        

        obj_manager.spawn_ammo_boxes("./Assets/ammo_box.png", count=8)
        obj_manager.spawn_heal_boxes("./Assets/heal_box.png", count=2) 
    
    
    clock      = pygame.time.Clock()

    sky   = pygame.image.load("./Assets/360_F_99890228_xRXJFnENLpAHdl82Y5LrRg11RwWMb5KO.jpg").convert()
    floor_color = (50, 150, 50)
 
    # ── GAME LOOP ──────────────────────────────────────────────────────────────
    running    = True
    end_result = None   
    while running:


        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   # torna al menu principale
                end_result = None
                
            # ── evento sparo ──
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not weapon.is_shooting:
                    weapon.shoot()
                    obj_manager.try_shoot()
 

        player.update()
        raycaster.castAllRays()
 
        screen.fill((0, 0, 0))
        half = WINDOW_HEIGHT // 2
        screen.blit(pygame.transform.scale(sky, (WINDOW_WIDTH, half)), (0, 0))
        pygame.draw.rect(screen, floor_color, (0, half, WINDOW_WIDTH, half))
        raycaster.render(screen)
        obj_manager.render(screen)
        obj_manager.update()

        # ── condizioni di fine partita ────────────────────────────────────────
        all_enemies_dead = (
            all(not e.alive for e in obj_manager.enemies) and
            all(not e.alive for e in obj_manager.ranged_enemies)
        )

        if player.hp <= 0:
            running = False
            end_result = "defeat"
        elif all_enemies_dead:
            running = False
            end_result = "victory"
        
        
        
        
        weapon.update()
        
        weapon.render(screen)
        
        # HUD
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

    # ── FINE PARTITA: mostra la schermata appropriata ─────────────────────────
    if end_result == "victory":
        run_victory(
            screen,
            image_path=None,          
            sound_path="./Assets/sounds/victory.mp3",          
            sound_volume=0.7,
        )
    elif end_result == "defeat":
        run_defeat(
            screen,
            image_path=None,          
            sound_path="./Assets/sounds/defeat.mp3",          
            sound_volume=0.6,
        )
   
