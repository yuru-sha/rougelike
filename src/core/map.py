"""
Map generation and management for Rogue
Implements traditional dungeon generation algorithms
"""
from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
import random
from utils.logger import get_logger
from entities.entity import Entity
from entities.stairs import Stairs

logger = get_logger(__name__)

@dataclass
class Room:
    """Data class representing a room in the dungeon"""
    x: int
    y: int
    width: int
    height: int

    @property
    def center(self) -> Tuple[int, int]:
        """Returns the center coordinates of the room"""
        return (
            self.x + self.width // 2,
            self.y + self.height // 2
        )
    
    def intersects(self, other: 'Room') -> bool:
        """Check if this room intersects with another room"""
        return (
            self.x <= other.x + other.width and
            self.x + self.width >= other.x and
            self.y <= other.y + other.height and
            self.y + self.height >= other.y
        )

class GameMap:
    """Class managing the dungeon map"""
    def __init__(self, width: int = 80, height: int = 21, level: int = 1):
        self.width = width
        self.height = height
        self.level = level  # Current dungeon level
        self.tiles = self._initialize_tiles()
        self.rooms: List[Room] = []
        self.visible: Set[Tuple[int, int]] = set()
        
        # Map generation parameters
        self.params = {
            'grid_width': 3,
            'grid_height': 3,
            'min_room_width': 6,
            'max_room_width': 9,
            'min_room_height': 4,
            'max_room_height': 7,
            'corridor_width': 1
        }

    def generate(self) -> List[Entity]:
        """Generate dungeon level"""
        logger.info(f"Generating dungeon level {self.level}")
        self.rooms.clear()
        
        # Calculate grid cell size
        cell_width = (self.width - 2) // self.params['grid_width']
        cell_height = (self.height - 3) // self.params['grid_height']
        
        # Place rooms
        self._place_rooms(cell_width, cell_height)
        
        # Connect rooms with corridors
        self._connect_rooms()
        
        # Place entities
        entities = []
        
        # Place stairs
        stairs = self._place_stairs()
        entities.extend(stairs)
        
        # Place gold
        gold_piles = self._place_gold()
        entities.extend(gold_piles)
        
        # Place Amulet in deep levels
        if self.level == 26:
            from entities.amulet import AmuletOfYendor
            room = random.choice(self.rooms)
            x = random.randint(room.x + 1, room.x + room.width - 2)
            y = random.randint(room.y + 1, room.y + room.height - 2)
            amulet = AmuletOfYendor(x, y)
            entities.append(amulet)
            logger.info("Placed Amulet of Yendor")
        
        logger.info("Dungeon generation complete")
        return entities

    def _place_rooms(self, cell_width: int, cell_height: int) -> None:
        """Place rooms in the grid cells"""
        for i in range(self.params['grid_height']):
            for j in range(self.params['grid_width']):
                self._place_room_in_cell(i, j, cell_width, cell_height)

    def _place_room_in_cell(self, i: int, j: int, cell_width: int, cell_height: int) -> None:
        """Place a room within a grid cell"""
        # Determine room size
        room_width = random.randint(
            self.params['min_room_width'],
            min(self.params['max_room_width'], cell_width - 2)
        )
        room_height = random.randint(
            self.params['min_room_height'],
            min(self.params['max_room_height'], cell_height - 2)
        )
        
        # Determine room position within cell
        cell_x = j * cell_width + 1
        cell_y = i * cell_height + 1
        x = cell_x + random.randint(0, max(0, cell_width - room_width - 2))
        y = cell_y + random.randint(0, max(0, cell_height - room_height - 2))
        
        # Create and carve room
        new_room = Room(x, y, room_width, room_height)
        self._carve_room(new_room)
        self.rooms.append(new_room)
        
        logger.debug(f"Room placed at ({x}, {y}) of size {room_width}x{room_height}")

    def _connect_rooms(self) -> None:
        """Connect rooms with corridors"""
        for i in range(len(self.rooms) - 1):
            self._connect_room_pair(self.rooms[i], self.rooms[i + 1])

    def _connect_room_pair(self, room1: Room, room2: Room) -> None:
        """Connect two rooms with a corridor"""
        x1, y1 = room1.center
        x2, y2 = room2.center
        
        # Generate L-shaped corridor
        if random.random() < 0.5:
            self._create_horizontal_tunnel(x1, x2, y1)
            self._create_vertical_tunnel(y1, y2, x2)
        else:
            self._create_vertical_tunnel(y1, y2, x1)
            self._create_horizontal_tunnel(x1, x2, y2)

    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a position is walkable"""
        return (
            self.is_in_bounds(x, y) and 
            self.tiles[y][x] in ['.', '#']
        )

    def is_in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within map bounds"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile_char(self, x: int, y: int) -> str:
        """Get the character at the specified tile position"""
        return self.tiles[y][x]

    def _carve_room(self, room: Room) -> None:
        """Carve out a room in the dungeon"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if y == room.y or y == room.y + room.height - 1:
                    self.tiles[y][x] = '-'
                elif x == room.x or x == room.x + room.width - 1:
                    self.tiles[y][x] = '|'
                else:
                    self.tiles[y][x] = '.'

    def _create_horizontal_tunnel(self, x1: int, x2: int, y: int) -> None:
        """水平方向の通路を生成"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y][x] = '.'
            # 通路の上下に壁を配置
            if self.tiles[y-1][x] == ' ':
                self.tiles[y-1][x] = '-'
            if self.tiles[y+1][x] == ' ':
                self.tiles[y+1][x] = '-'

    def _create_vertical_tunnel(self, y1: int, y2: int, x: int) -> None:
        """垂直方向の通路を生成"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y][x] = '.'
            # 通路の左右に壁を配置
            if self.tiles[y][x-1] == ' ':
                self.tiles[y][x-1] = '|'
            if self.tiles[y][x+1] == ' ':
                self.tiles[y][x+1] = '|'

    def _initialize_tiles(self) -> List[List[str]]:
        """マップを壁で初期化"""
        return [[' ' for x in range(self.width)] for y in range(self.height)]

    def _create_horizontal_passage(self, room1: Room, room2: Room) -> None:
        """水平方向の通路を生成"""
        x1 = room1.x + room1.width - 1
        x2 = room2.x
        
        # 部屋の重なりがある場合の処理
        y_min = max(room1.y + 1, room2.y + 1)
        y_max = min(room1.y + room1.height - 2, room2.y + room2.height - 2)
        
        if y_min > y_max:
            # 部屋が上下に離れている場合は中間点を使用
            y = (room1.y + room1.height // 2 + room2.y + room2.height // 2) // 2
        else:
            y = random.randint(y_min, y_max)
        
        # 通路を生成
        for x in range(x1, x2 + 1):
            self.tiles[y][x] = '.'
            # 通路の上下に壁を配置
            if self.tiles[y-1][x] == ' ':
                self.tiles[y-1][x] = '-'
            if self.tiles[y+1][x] == ' ':
                self.tiles[y+1][x] = '-'

    def _create_vertical_passage(self, room1: Room, room2: Room) -> None:
        """垂直方向の通路を生成"""
        y1 = room1.y + room1.height - 1
        y2 = room2.y
        
        # 部屋の重なりがある場合の処理
        x_min = max(room1.x + 1, room2.x + 1)
        x_max = min(room1.x + room1.width - 2, room2.x + room2.width - 2)
        
        if x_min > x_max:
            # 部屋が左右に離れている場合は中間点を使用
            x = (room1.x + room1.width // 2 + room2.x + room2.width // 2) // 2
        else:
            x = random.randint(x_min, x_max)
        
        # 通路を生成
        for y in range(y1, y2 + 1):
            self.tiles[y][x] = '.'
            # 通路の左右に壁を配置
            if self.tiles[y][x-1] == ' ':
                self.tiles[y][x-1] = '|'
            if self.tiles[y][x+1] == ' ':
                self.tiles[y][x+1] = '|'

    def _create_horizontal_passage(self, room1: Room, room2: Room) -> None:
        """水平方向の通路を生成"""
        x1 = room1.x + room1.width - 1
        x2 = room2.x
        
        # 部屋の重なりがある場合の処理
        y_min = max(room1.y + 1, room2.y + 1)
        y_max = min(room1.y + room1.height - 2, room2.y + room2.height - 2)
        
        if y_min > y_max:
            # 部屋が上下に離れている場合は中間点を使用
            y = (room1.y + room1.height // 2 + room2.y + room2.height // 2) // 2
        else:
            y = random.randint(y_min, y_max)
        
        # 通路を生成
        for x in range(x1, x2 + 1):
            self.tiles[y][x] = '.'
            # 通路の上下に壁を配置
            if self.tiles[y-1][x] == ' ':
                self.tiles[y-1][x] = '-'
            if self.tiles[y+1][x] == ' ':
                self.tiles[y+1][x] = '-'

    def _create_vertical_passage(self, room1: Room, room2: Room) -> None:
        """垂直方向の通路を生成"""
        y1 = room1.y + room1.height - 1
        y2 = room2.y
        
        # 部屋の重なりがある場合の処理
        x_min = max(room1.x + 1, room2.x + 1)
        x_max = min(room1.x + room1.width - 2, room2.x + room2.width - 2)
        
        if x_min > x_max:
            # 部屋が左右に離れている場合は中間点を使用
            x = (room1.x + room1.width // 2 + room2.x + room2.width // 2) // 2
        else:
            x = random.randint(x_min, x_max)
        
        # 通路を生成
        for y in range(y1, y2 + 1):
            self.tiles[y][x] = '.'
            # 通路の左右に壁を配置
            if self.tiles[y][x-1] == ' ':
                self.tiles[y][x-1] = '|'
            if self.tiles[y][x+1] == ' ':
                self.tiles[y][x+1] = '|'

    def _carve_room(self, room: Room) -> None:
        """部屋を掘る"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if y == room.y or y == room.y + room.height - 1:
                    self.tiles[y][x] = '-'
                elif x == room.x or x == room.x + room.width - 1:
                    self.tiles[y][x] = '|'
                else:
                    self.tiles[y][x] = '.'

    def get_tile_char(self, x: int, y: int) -> str:
        """指定位置のタイル文字を取得"""
        return self.tiles[y][x]

    def is_walkable(self, x: int, y: int) -> bool:
        """指定位置が歩行可能か判定"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x] in '.#'
        return False 

    def _place_entity_in_room(self, room: Room) -> Tuple[int, int]:
        """Get random position in room for entity placement"""
        return (
            random.randint(room.x + 1, room.x + room.width - 2),
            random.randint(room.y + 1, room.y + room.height - 2)
        )

    def _place_gold(self) -> List['Gold']:
        """Place gold piles in rooms"""
        from entities.gold import Gold
        
        gold_count = random.randint(2, 4)
        available_rooms = random.sample(self.rooms, gold_count)
        
        return [
            Gold(*self._place_entity_in_room(room))
            for room in available_rooms
        ]

    def _place_stairs(self) -> List[Stairs]:
        """Place stairs in the dungeon"""
        stairs = []
        
        if self.level > 1:
            x, y = self._place_entity_in_room(self.rooms[0])
            stairs.append(Stairs(x, y, 'up'))
        
        if self.level < 26:
            x, y = self._place_entity_in_room(self.rooms[-1])
            stairs.append(Stairs(x, y, 'down'))
        
        return stairs 