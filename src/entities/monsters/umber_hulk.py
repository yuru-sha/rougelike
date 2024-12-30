"""
Umber Hulk monster implementation
Represents a powerful monster that causes confusion
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class UmberHulk(Monster):
    """
    Umber Hulk monster class
    A fearsome monster with a confusing gaze
    Special: Can confuse the player with its gaze attack
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['UMBER_HULK']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 