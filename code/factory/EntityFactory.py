from code.entities.Player import Player
from code.entities.Boss import Boss


def get_entity(entity_name):
    match entity_name:

        case "Player":
            return Player(
                "Mage",
                "asset/Mago f1.png",
                (100, 400)
            )

        case "Boss":
            return Boss(
                "EyeBoss",
                "asset/boss.png",
                (800, 150)
            )