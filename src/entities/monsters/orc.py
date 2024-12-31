"""
Orc monster implementation
A common humanoid enemy with balanced stats
"""

from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG


class Orc(Monster):
    """
    Orc monster class
    Basic humanoid monster with moderate strength
    """

    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG["ORC"]
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
