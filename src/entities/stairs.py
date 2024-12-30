"""
Stairs implementation
Allows movement between dungeon levels
"""
from entities.entity import Entity
from utils.logger import get_logger

logger = get_logger(__name__)

class Stairs(Entity):
    """
    Class representing stairs in the dungeon
    
    Attributes:
        direction: Direction of stairs ('up' or 'down')
        char: Display character ('<' for up, '>' for down)
    """
    def __init__(self, x: int, y: int, direction: str):
        """
        Initialize stairs entity
        
        Args:
            x: X-coordinate position
            y: Y-coordinate position
            direction: Direction of stairs ('up' or 'down')
        """
        char = '<' if direction == 'up' else '>'
        super().__init__(
            x=x,
            y=y,
            char=char,
            name=f'Stairs {direction}',
            blocks_movement=False  # Stairs can be walked over
        )
        self.direction = direction
        logger.debug(f"Created {direction} stairs at ({x}, {y})") 