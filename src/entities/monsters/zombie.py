"""
Zombie monster implementation
Represents a tough undead monster with high HP and resilience
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Zombie(Monster):
    """
    Zombie monster class
    A resilient undead that can withstand significant damage
    Special: Takes reduced damage from physical attacks
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['ZOMBIE']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 