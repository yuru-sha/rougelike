"""
Gold implementation
Represents gold pieces that can be collected by the player
"""
from entities.entity import Entity
import random
from utils.logger import get_logger

logger = get_logger(__name__)

class Gold(Entity):
    """Class representing gold pieces"""
    def __init__(self, x: int, y: int, amount: int = None):
        super().__init__(
            x=x,
            y=y,
            char='*',  # Same display as original Rogue
            name='Gold',
            blocks_movement=False  # Gold can be walked over
        )
        # Randomly determine amount if not specified
        self.amount = amount or random.randint(2, 50)
        logger.debug(f"Created gold pile of {self.amount} at ({x}, {y})") 