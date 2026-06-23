import pygame


class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert()

    def draw(self, window):
        window.blit(self.image, (0, 0))