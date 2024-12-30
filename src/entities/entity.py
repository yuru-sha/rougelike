"""
Base entity class for all game objects
"""
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from core.map import GameMap  # Import for type hints only

class Entity:
    """
    Base class for all game entities
    
    Attributes:
        x: X-coordinate position
        y: Y-coordinate position
        char: Display character
        name: Entity name
        blocks_movement: Whether entity blocks movement
    """
    def __init__(self, x: int, y: int, char: str, name: str, blocks_movement: bool = True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.blocks_movement = blocks_movement
    
    @property
    def position(self) -> Tuple[int, int]:
        """
        Get current position
        
        Returns:
            Tuple[int, int]: Current (x, y) coordinates
        """
        return (self.x, self.y)
    
    def move(self, dx: int, dy: int, game_map: 'GameMap') -> bool:
        """
        Attempt to move entity by given delta
        
        Args:
            dx: X-axis movement delta
            dy: Y-axis movement delta
            game_map: Current game map
            
        Returns:
            bool: True if movement successful, False otherwise
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def distance_to(self, other: 'Entity') -> float:
        """
        Calculate distance to another entity
        
        Args:
            other: Target entity
            
        Returns:
            float: Euclidean distance to target
        """
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx ** 2 + dy ** 2) ** 0.5 