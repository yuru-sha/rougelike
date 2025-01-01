"""
Player class implementation
Handles player specific attributes and actions
"""
from typing import Optional
from entities.entity import Entity
from core.map import GameMap, Room
from utils.logger import get_logger

logger = get_logger(__name__)

class Player(Entity):
    """Class representing the player character"""
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char='@',
            name='Player'
        )
        self.is_dead = False
        # Initialize stats
        self.stats = {
            'level': 1,
            'exp': 0,
            'hp': 12,
            'max_hp': 12,
            'strength': 16,
            'max_strength': 16,
            'gold': 0,
            'armor_class': 0
        }
        
        # Equipment slots
        self.equipment = {
            'weapon': None,
            'armor': None
        }

    @property
    def level(self) -> int:
        return self.stats['level']
    
    @property
    def exp(self) -> int:
        return self.stats['exp']
    
    @property
    def hp(self) -> int:
        return self.stats['hp']
    
    @property
    def max_hp(self) -> int:
        return self.stats['max_hp']
    
    @property
    def strength(self) -> int:
        return self.stats['strength']
    
    @property
    def gold(self) -> int:
        return self.stats['gold']

    def move(self, dx: int, dy: int, game_map: GameMap) -> bool:
        """Handle player movement"""
        new_x = self.x + dx
        new_y = self.y + dy
        logger.debug(f"Attempting to move from ({self.x}, {self.y}) to ({new_x}, {new_y})")
        
        success = super().move(dx, dy, game_map)
        if success:
            logger.debug(f"Move successful, updating FOV")
            self._update_fov(game_map)
        else:
            logger.debug(f"Move failed - destination not walkable")
        return success

    def _update_fov(self, game_map: GameMap) -> None:
        """Update player's field of view (Rogue-style)"""
        game_map.visible.clear()
        
        # Find current room
        current_room = self._get_current_room(game_map)
        
        if current_room:
            self._make_room_visible(current_room, game_map)
        else:
            self._make_corridor_visible(game_map)

    def _get_current_room(self, game_map: GameMap) -> Optional[Room]:
        """プレイヤーがいる部屋を取得"""
        for room in game_map.rooms:
            if (room.x <= self.x < room.x + room.width and 
                room.y <= self.y < room.y + room.height):
                return room
        return None

    def _make_room_visible(self, room: Room, game_map: GameMap) -> None:
        """部屋全体を視界に入れる"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                game_map.visible.add((x, y))

    def _make_corridor_visible(self, game_map: GameMap) -> None:
        """通路の視界を更新"""
        # プレイヤーの位置
        game_map.visible.add((self.x, self.y))
        
        # 隣接タイル
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_x, new_y = self.x + dx, self.y + dy
            if game_map.is_in_bounds(new_x, new_y):
                game_map.visible.add((new_x, new_y))

    def _cast_light(self, game_map: GameMap, octant: int) -> None:
        """影を投影（影投影法によるFOV計算）"""
        VIEW_RADIUS = 7
        
        def transform(row: int, col: int) -> tuple[int, int]:
            """座標変換（8方向対応）"""
            if octant == 0:    return self.x + col, self.y - row
            elif octant == 1:  return self.x + row, self.y - col
            elif octant == 2:  return self.x + row, self.y + col
            elif octant == 3:  return self.x + col, self.y + row
            elif octant == 4:  return self.x - col, self.y + row
            elif octant == 5:  return self.x - row, self.y + col
            elif octant == 6:  return self.x - row, self.y - col
            else:             return self.x - col, self.y - row
        
        def is_wall(x: int, y: int) -> bool:
            """壁かどうかを判定"""
            if 0 <= x < game_map.width and 0 <= y < game_map.height:
                return game_map.get_tile_char(x, y) in ['|', '-']
            return True
        
        def is_in_bounds(x: int, y: int) -> bool:
            """マップ範囲内かどうかを判定"""
            return 0 <= x < game_map.width and 0 <= y < game_map.height
        
        # 視界範囲を計算
        for row in range(VIEW_RADIUS + 1):
            for col in range(row + 1):
                x, y = transform(row, col)
                
                if is_in_bounds(x, y):
                    # 視線が通るかチェック
                    if self._has_line_of_sight(game_map, x, y):
                        game_map.visible.add((x, y))
                    
                    # 壁に当たったら、その方向の探索を終了
                    if is_wall(x, y):
                        break

    def _has_line_of_sight(self, game_map: GameMap, target_x: int, target_y: int) -> bool:
        """視線が通るかチェック（ブレゼンハムのライン算法）"""
        x0, y0 = self.x, self.y
        x1, y1 = target_x, target_y
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x = x0
        y = y0
        n = 1 + dx + dy
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        error = dx - dy
        dx *= 2
        dy *= 2

        while n > 0:
            # 壁があれば視線が通らない
            if game_map.get_tile_char(x, y) in ['|', '-']:
                return False
            
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
            n -= 1

        return True

    def take_damage(self, amount: int) -> None:
        """ダメージを受ける"""
        self.hp = max(0, self.hp - amount)
        logger.info(f"Player took {amount} damage. HP: {self.hp}/{self.max_hp}")
        if self.hp == 0:
            self.die()

    def heal(self, amount: int) -> None:
        """HPを回復"""
        self.hp = min(self.max_hp, self.hp + amount)
        logger.info(f"Player healed {amount} HP. HP: {self.hp}/{self.max_hp}")

    def die(self) -> None:
        """Handle player death"""
        logger.info("Player died!")
        self.char = '%'  # Represent corpse
        self.is_dead = True

    def add_gold(self, amount: int) -> None:
        """Add gold to player's inventory"""
        self.stats['gold'] += amount
        logger.info(f"Added {amount} gold. Total: {self.gold}")

    def gain_exp(self, amount: int) -> None:
        """Gain experience points"""
        self.exp += amount
        logger.info(f"Gained {amount} exp. Total: {self.exp}")
        
        # Check for level up
        while self.exp >= self._exp_to_next_level():
            self._level_up()

    def _exp_to_next_level(self) -> int:
        """Calculate experience needed for next level"""
        return self.level * 10

    def _level_up(self) -> None:
        """Handle level up"""
        self.level += 1
        self.max_hp += 2
        self.hp = self.max_hp
        self.strength += 1
        logger.info(f"Level up! Now level {self.level}") 