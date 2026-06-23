from code.entities.Entity import Entity


class Player(Entity):
    def __init__(self, name, image_path, position):
        super().__init__(name, image_path, position, (180, 180))

        self.hp = 100
        self.max_hp = 100