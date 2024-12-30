"""
Troll monster implementation
Represents a strong monster with regenerative abilities
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Troll(Monster):
    """
    Troll monster class
    A powerful monster that can heal over time
    Special: Regenerates health each turn
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['TROLL']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 