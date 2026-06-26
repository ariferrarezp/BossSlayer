import pygame
from code.scenes.Menu import Menu
from code.scenes.Battle import Battle
from code.scenes.History import History
from code.Const import *

pygame.init()

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Boss Slayer")

running = True

while running:
    menu = Menu(window)
    result = menu.run()

    if result == "start":
        battle = Battle(window)
        battle.run()

    elif result == "history":
        history = History(window)
        history.run()

pygame.quit()