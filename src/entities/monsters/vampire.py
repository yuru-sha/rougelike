"""
Vampire monster implementation
Represents a powerful undead that drains life force
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Vampire(Monster):
    """
    Vampire monster class
    A deadly undead that can heal itself by draining health
    Special: Heals itself when dealing damage to the player
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['VAMPIRE']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 