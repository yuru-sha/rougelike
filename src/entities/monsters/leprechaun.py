"""
Leprechaun monster implementation
A tricky monster that steals gold
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Leprechaun(Monster):
    """
    Leprechaun monster class
    Can steal gold from the player and teleport away
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['LEPRECHAUN']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 