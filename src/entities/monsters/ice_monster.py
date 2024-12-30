"""
Ice Monster implementation
A monster that can freeze the player
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class IceMonster(Monster):
    """
    Ice Monster class
    Can temporarily freeze the player in place
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['ICE_MONSTER']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 