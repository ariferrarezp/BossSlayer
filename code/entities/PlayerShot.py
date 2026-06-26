import pygame
from code.entities.Entity import Entity

class PlayerShot(Entity):
    def __init__(self, position):
        super().__init__(
            "PlayerShot",
            "asset/ataque_mago.png",
            position,
            (40, 40)
        )
        self.speed = 10

    def move(self):
        self.rect.x += self.speed