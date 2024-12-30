"""
Medusa monster implementation
A mythical monster that can petrify the player
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Medusa(Monster):
    """
    Medusa monster class
    Can turn the player to stone with her gaze
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['MEDUSA']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 