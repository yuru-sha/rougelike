"""
Base entity class for all game objects
"""
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from core.map import GameMap  # 型チェック時のみインポート

class Entity:
    def __init__(self, x: int, y: int, char: str, name: str, blocks_movement: bool = True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.blocks_movement = blocks_movement
    
    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def move(self, dx: int, dy: int, game_map: 'GameMap') -> bool:  # 型ヒントを文字列で指定
        """エンティティの移動を試みる"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def distance_to(self, other: 'Entity') -> float:
        """他のエンティティまでの距離を計算"""
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx ** 2 + dy ** 2) ** 0.5 