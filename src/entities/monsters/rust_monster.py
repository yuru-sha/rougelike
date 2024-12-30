"""
Rust Monster implementation
Represents a monster that corrodes metal equipment
"""
from entities.monster import Monster
from constants.game_constants import MONSTER_CONFIG

class RustMonster(Monster):
    """
    Rust Monster class
    A monster that destroys metal equipment
    Special: Can permanently damage player's armor
    """
    def __init__(self, x: int, y: int):
        config = MONSTER_CONFIG['RUST_MONSTER']
        super().__init__(
            x=x, y=y,
            char=config['char'],
            name=config['name'],
            level=config['level'],
            hp=config['hp'],
            strength=config['strength'],
            exp_value=config['exp_value']
        ) 