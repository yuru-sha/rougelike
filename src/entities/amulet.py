"""
Amulet of Yendor implementation
The ultimate goal of the game
"""
from entities.entity import Entity
from utils.logger import get_logger

logger = get_logger(__name__)

class AmuletOfYendor(Entity):
    """The Amulet of Yendor - the ultimate goal"""
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char='*',  # Special display character
            name='Amulet of Yendor',
            blocks_movement=False
        ) 