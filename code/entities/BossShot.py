from code.entities.Entity import Entity


class BossShot(Entity):
    def __init__(self, image_path, position, speed, size=(50, 50), direction_y=0):
        super().__init__(
            "BossShot",
            image_path,
            position,
            size
        )

        self.speed = speed
        self.direction_y = direction_y

    def move(self):
        self.rect.x -= self.speed
        self.rect.y += self.direction_y