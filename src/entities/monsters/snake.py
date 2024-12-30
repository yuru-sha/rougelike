"""
Snake monster implementation
Represents a poisonous early-game monster
"""

from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG


class Snake(Monster):
    """
    Snake monster class
    A quick monster with venomous attacks
    Special: Can poison the player, causing damage over time
    """

    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG["SNAKE"]
        super().__init__(
            x=x,
            y=y,
            char=config["char"],
            name=config["name"],
            level=config["level"],
            hp=config["hp"],
            strength=config["strength"],
            exp_value=config["exp_value"],
        )
