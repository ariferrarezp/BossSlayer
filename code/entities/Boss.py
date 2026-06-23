from code.entities.Entity import Entity


class Boss(Entity):
    def __init__(self, name, image_path, position):
        super().__init__(name, image_path, position, (400, 400))

        self.hp = 300
        self.max_hp = 300