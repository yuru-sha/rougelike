"""
Emu monster implementation
A fast bird-like creature
"""

from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG


class Emu(Monster):
    """
    Emu monster class
    Quick monster that can flee from combat
    """

    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG["EMU"]
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
