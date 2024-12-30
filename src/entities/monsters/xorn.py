"""
Xorn monster implementation
Represents a creature that can phase through walls
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Xorn(Monster):
    """
    Xorn monster class
    A monster that can move through solid walls
    Special: Can pass through walls to surprise the player
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['XORN']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 