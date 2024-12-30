"""
Yeti monster implementation
Represents a powerful beast with ice-based abilities
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Yeti(Monster):
    """
    Yeti monster class
    A strong monster that can freeze opponents
    Special: Can freeze the player, preventing movement
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['YETI']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 