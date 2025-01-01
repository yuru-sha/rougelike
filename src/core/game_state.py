"""
Manages the current state of the game
Including map, player, entities and game progress
"""
from dataclasses import dataclass, field
from typing import List, Dict, Set
from entities.entity import Entity
from entities.player import Player
from core.map import GameMap

@dataclass
class GameState:
    player: Player
    current_map: GameMap
    entities: List[Entity]
    game_level: int = 1
    explored_levels: Set[int] = field(default_factory=set)  # Use default_factory for mutable defaults
    has_amulet: bool = False  # Whether player has the Amulet of Yendor
        
    def calculate_score(self) -> int:
        """Calculate score (using original Rogue scoring system)"""
        gold_score = self.player.gold
        level_score = self.player.level * 1000
        depth_score = len(self.explored_levels) * 500
        amulet_bonus = 20000 if self.has_amulet else 0  # Bonus for having the Amulet
        
        total_score = gold_score + level_score + depth_score + amulet_bonus
        return total_score

    def add_explored_level(self, level: int) -> None:
        """Record an explored dungeon level"""
        self.explored_levels.add(level)

    def check_victory(self) -> bool:
        """Check victory condition
        Player wins by returning to level 1 with the Amulet"""
        return self.has_amulet and self.game_level == 1 