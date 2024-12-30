"""
Dragon monster implementation
Represents the most powerful monster in the game
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Dragon(Monster):
    """
    Dragon monster class
    The ultimate enemy with devastating attacks
    Special: Can breathe fire for massive area damage
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['DRAGON']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 