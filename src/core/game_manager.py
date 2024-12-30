from dataclasses import dataclass
from typing import Set, List, Optional
from enum import Enum, auto
from src.entities.player import Player
from src.core.map import GameMap
from src.entities.base_entity import Entity


class GameState(Enum):
    TITLE = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


@dataclass
class GameProgress:
    """Immutable game progress container"""

    player: Player
    current_map: GameMap
    entities: List[Entity]
    game_level: int
    explored_levels: Set[int]
    has_amulet: bool = False


class GameManager:
    def __init__(self) -> None:
        self._progress: Optional[GameProgress] = None
        self._state: GameState = GameState.TITLE

    def new_game(self) -> None:
        """Initialize new game state"""
        self._state = GameState.PLAYING
        self._progress = GameProgress(
            player=Player(),
            current_map=GameMap(),
            entities=[],
            game_level=1,
            explored_levels=set(),
        )

    def update_progress(self, new_progress: GameProgress) -> None:
        """Update game progress immutably"""
        self._progress = new_progress

    @property
    def progress(self) -> GameProgress:
        """Get current game progress"""
        if not self._progress:
            raise RuntimeError("Game not initialized")
        return self._progress

    def update_state(self, new_state: GameState) -> None:
        """Update game state (TITLE, PLAYING, etc)"""
        self._state = new_state

    @property
    def state(self) -> GameState:
        """Get current game state"""
        return self._state
