"""
Griffin monster implementation
A powerful flying beast
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Griffin(Monster):
    """
    Griffin monster class
    Can fly and attack from a distance
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['GRIFFIN']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 