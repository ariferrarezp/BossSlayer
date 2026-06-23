#import pygame

from code.Const import *
from code.Background import Background
from code.factory.EntityFactory import get_entity

pygame.init()

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Boss Slayer")

clock = pygame.time.Clock()

background = Background("asset/fundo.png")

player = get_entity("Player")
boss = get_entity("Boss")

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    background.draw(window)
    player.draw(window)
    boss.draw(window)

    pygame.display.update()

pygame.quit()