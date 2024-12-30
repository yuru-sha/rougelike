"""
Wraith monster implementation
Represents an undead that drains experience levels
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Wraith(Monster):
    """
    Wraith monster class
    An undead creature that feeds on experience
    Special: Can drain player's experience levels on hit
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['WRAITH']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 