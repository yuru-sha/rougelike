"""
Stairs implementation
Allows movement between dungeon levels
"""
from entities.entity import Entity
from utils.logger import get_logger

logger = get_logger(__name__)

class Stairs(Entity):
    """Class representing stairs in the dungeon"""
    def __init__(self, x: int, y: int, direction: str):
        """
        Args:
            direction: 'up' or 'down'
        """
        char = '<' if direction == 'up' else '>'
        super().__init__(
            x=x,
            y=y,
            char=char,
            name=f'Stairs {direction}',
            blocks_movement=False
        )
        self.direction = direction 