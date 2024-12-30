"""
Bat monster implementation
Represents a weak but agile early-game monster
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Bat(Monster):
    """
    Bat monster class
    A fast but weak monster found in early levels
    Special: High evasion chance against attacks
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['BAT']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 