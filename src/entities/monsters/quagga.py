"""
Quagga monster implementation
Represents a fast and aggressive beast
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Quagga(Monster):
    """
    Quagga monster class
    A swift monster with aggressive behavior
    Special: Can move twice per turn
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['QUAGGA']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 