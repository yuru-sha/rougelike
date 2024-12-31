"""
Aquator monster implementation
Represents a water-based monster that corrodes equipment
"""

from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG


class Aquator(Monster):
    """
    Aquator monster class
    A water elemental that damages equipment
    Special: Can rust player's armor on contact
    """

    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG["AQUATOR"]
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
