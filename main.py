import pygame
from settings import *
from map import Map
from player import Player
from raycaster import Raycaster

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map()
player = Player()

clock = pygame.time.Clock()

raycaster = Raycaster(player, map)

sky = pygame.image.load("./Assets/360_F_99890228_xRXJFnENLpAHdl82Y5LrRg11RwWMb5KO.jpg").convert()
floor = pygame.image.load("./Assets/1.-evergreen-prato-ampio-474467063.jpg").convert()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
   
    player.update()
    raycaster.castAllRays()

    screen.fill((0, 0, 0))

    half_height = WINDOW_HEIGHT // 2

    # cielo (parte sopra)
    screen.blit(pygame.transform.scale(sky, (WINDOW_WIDTH, half_height)), (0, 0))

    # terreno (parte sotto)
    pygame.draw.rect(
        screen,
        (50, 150, 50),  # verde prato, cambialo come vuoi
        (0, half_height, WINDOW_WIDTH, half_height)
    )

    # map.render(screen)
    # player.render(screen)
    
    raycaster.render(screen)

    pygame.display.update()
