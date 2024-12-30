"""
Phantom monster implementation
An ethereal monster that can become invisible
"""

from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG


class Phantom(Monster):
    """
    Phantom monster class
    Can turn invisible and surprise the player
    """

    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG["PHANTOM"]
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
