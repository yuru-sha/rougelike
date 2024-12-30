"""
Jabberwock monster implementation
A fearsome legendary creature
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Jabberwock(Monster):
    """
    Jabberwock monster class
    Powerful monster with multiple attacks
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['JABBERWOCK']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 