"""
Hobgoblin monster implementation
Represents a common humanoid enemy with basic combat skills
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class Hobgoblin(Monster):
    """
    Hobgoblin monster class
    A basic humanoid monster with balanced stats
    Special: Has a chance to perform a double attack
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['HOBGOBLIN']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 