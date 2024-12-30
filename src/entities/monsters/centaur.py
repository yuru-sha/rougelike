"""
Centaur monster implementation
A fast and skilled warrior monster
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Centaur(Monster):
    """
    Centaur monster class
    Fast moving monster with good combat skills
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['CENTAUR']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 