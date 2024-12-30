"""
Demon monster implementation
A powerful demon from the netherworld
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Demon(Monster):
    """
    Demon monster class
    Can cast spells and summon other monsters
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['DEMON']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 