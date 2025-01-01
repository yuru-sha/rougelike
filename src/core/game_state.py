"""
Manages the current state of the game
Including map, player, entities and game progress
"""
from dataclasses import dataclass, field
from typing import List, Dict, Set
from entities.entity import Entity
from entities.player import Player
from core.map import GameMap
from constants.game_constants import SCORE_CONFIG

@dataclass
class GameState:
    """
    Represents the current state of the game
    
    Attributes:
        player: Current player instance
        current_map: Current level map
        entities: List of all entities in current level
        game_level: Current dungeon level (1-26)
        explored_levels: Set of explored level numbers
        has_amulet: Whether player has obtained the Amulet
    """
    player: Player
    current_map: GameMap
    entities: List[Entity]
    game_level: int = 1
    explored_levels: Set[int] = field(default_factory=set)  # Track explored levels
    has_amulet: bool = False  # Amulet of Yendor possession flag
        
    def calculate_score(self) -> int:
        """
        Calculate final score using original Rogue scoring system
        
        Returns:
            int: Total score based on gold, level, depth and amulet
        """
        gold_score = self.player.gold
        level_score = self.player.level * SCORE_CONFIG['LEVEL_MULTIPLIER']
        depth_score = len(self.explored_levels) * SCORE_CONFIG['DEPTH_MULTIPLIER']
        amulet_bonus = SCORE_CONFIG['AMULET_BONUS'] if self.has_amulet else 0
        
        total_score = gold_score + level_score + depth_score + amulet_bonus
        return total_score

    def add_explored_level(self, level: int) -> None:
        """
        Record an explored dungeon level
        
        Args:
            level: Level number to mark as explored
        """
        self.explored_levels.add(level)

    def check_victory(self) -> bool:
        """
        Check if victory conditions are met
        Player wins by returning to level 1 with the Amulet
        
        Returns:
            bool: True if victory conditions are met
        """
        return self.has_amulet and self.game_level == 1 