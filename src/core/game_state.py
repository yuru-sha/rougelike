"""
Game state management
"""
from dataclasses import dataclass
from typing import List, Set
from entities.player import Player
from core.map import GameMap
from entities.entity import Entity
from constants.game_constants import SCORE_CONFIG

@dataclass
class GameState:
    """Game state container"""
    player: Player
    current_map: GameMap
    entities: List[Entity]
    game_level: int = 1
    explored_levels: Set[int] = None
    has_amulet: bool = False

    def __post_init__(self):
        if self.explored_levels is None:
            self.explored_levels = set()

    def calculate_score(self) -> int:
        """Calculate final score"""
        score = (
            self.player.gold +
            self.player.level * SCORE_CONFIG['LEVEL_MULTIPLIER'] +
            len(self.explored_levels) * SCORE_CONFIG['DEPTH_MULTIPLIER']
        )
        if self.has_amulet:
            score += SCORE_CONFIG['AMULET_BONUS']
        return score

    def check_victory(self) -> bool:
        """Check if victory conditions are met"""
        return self.has_amulet and self.game_level == 1

    def add_explored_level(self, level: int) -> None:
        """Add level to explored levels set"""
        self.explored_levels.add(level) 