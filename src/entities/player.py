"""
Player class implementation
Handles player specific attributes and actions
"""
from typing import Optional
from entities.entity import Entity
from core.map import GameMap, Room
from utils.logger import get_logger
from constants.game_constants import LEVEL_UP_CONFIG, COMBAT_CONFIG
import random

logger = get_logger(__name__)

class Player(Entity):
    """
    Class representing the player character
    
    Attributes:
        is_dead: Whether player is dead
        stats: Dictionary containing player stats
        equipment: Dictionary containing equipped items
    """
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char='@',
            name='Player'
        )
        self.is_dead = False
        # Initialize base stats
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
    
    @level.setter
    def level(self, value: int) -> None:
        self.stats['level'] = value
    
    @property
    def exp(self) -> int:
        return self.stats['exp']
    
    @exp.setter
    def exp(self, value: int) -> None:
        self.stats['exp'] = value
    
    @property
    def hp(self) -> int:
        return self.stats['hp']
    
    @hp.setter
    def hp(self, value: int) -> None:
        self.stats['hp'] = value
    
    @property
    def max_hp(self) -> int:
        return self.stats['max_hp']
    
    @max_hp.setter
    def max_hp(self, value: int) -> None:
        self.stats['max_hp'] = value
    
    @property
    def strength(self) -> int:
        return self.stats['strength']
    
    @strength.setter
    def strength(self, value: int) -> None:
        self.stats['strength'] = value
    
    @property
    def gold(self) -> int:
        return self.stats['gold']
    
    @property
    def armor_class(self) -> int:
        return self.stats['armor_class']
    
    @armor_class.setter
    def armor_class(self, value: int) -> None:
        self.stats['armor_class'] = value

    def move(self, dx: int, dy: int, game_map: GameMap) -> bool:
        """
        Handle player movement and update FOV
        
        Args:
            dx: X-axis movement delta
            dy: Y-axis movement delta
            game_map: Current game map
            
        Returns:
            bool: True if movement successful
        """
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
        # Clear current FOV
        game_map.visible.clear()
        
        # Find current room
        current_room = self._get_current_room(game_map)
        
        if current_room:
            self._make_room_visible(current_room, game_map)
        else:
            self._make_corridor_visible(game_map)

    def _get_current_room(self, game_map: GameMap) -> Optional[Room]:
        # Check if player is in any room
        for room in game_map.rooms:
            if (room.x <= self.x < room.x + room.width and 
                room.y <= self.y < room.y + room.height):
                return room
        return None

    def _make_room_visible(self, room: Room, game_map: GameMap) -> None:
        # Make entire room visible
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                game_map.visible.add((x, y))

    def _make_corridor_visible(self, game_map: GameMap) -> None:
        # Add current position to visible tiles
        game_map.visible.add((self.x, self.y))
        
        # Add adjacent tiles to visible
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_x, new_y = self.x + dx, self.y + dy
            if game_map.is_in_bounds(new_x, new_y):
                game_map.visible.add((new_x, new_y))

    def _cast_light(self, game_map: GameMap, octant: int) -> None:
        VIEW_RADIUS = 7
        
        def transform(row: int, col: int) -> tuple[int, int]:
            # Transform coordinates based on octant
            if octant == 0:    return self.x + col, self.y - row
            elif octant == 1:  return self.x + row, self.y - col
            elif octant == 2:  return self.x + row, self.y + col
            elif octant == 3:  return self.x + col, self.y + row
            elif octant == 4:  return self.x - col, self.y + row
            elif octant == 5:  return self.x - row, self.y + col
            elif octant == 6:  return self.x - row, self.y - col
            else:             return self.x - col, self.y - row
        
        def is_wall(x: int, y: int) -> bool:
            # Check if position contains a wall
            if 0 <= x < game_map.width and 0 <= y < game_map.height:
                return game_map.get_tile_char(x, y) in ['|', '-']
            return True
        
        def is_in_bounds(x: int, y: int) -> bool:
            # Check if position is within map bounds
            return 0 <= x < game_map.width and 0 <= y < game_map.height
        
        # Calculate visible area
        for row in range(VIEW_RADIUS + 1):
            for col in range(row + 1):
                x, y = transform(row, col)
                
                if is_in_bounds(x, y):
                    # Check line of sight
                    if self._has_line_of_sight(game_map, x, y):
                        game_map.visible.add((x, y))
                    
                    # Stop if wall is hit
                    if is_wall(x, y):
                        break

    def _has_line_of_sight(self, game_map: GameMap, target_x: int, target_y: int) -> bool:
        # Bresenham's line algorithm for line of sight
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
            # Check for walls blocking sight
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
        """
        Apply damage to player
        
        Args:
            amount: Amount of damage to take
        """
        self.hp = max(0, self.hp - amount)
        logger.info(f"Player took {amount} damage. HP: {self.hp}/{self.max_hp}")
        if self.hp == 0:
            self.die()

    def heal(self, amount: int) -> None:
        """
        Heal player HP
        
        Args:
            amount: Amount of HP to heal
        """
        self.hp = min(self.max_hp, self.hp + amount)
        logger.info(f"Player healed {amount} HP. HP: {self.hp}/{self.max_hp}")

    def die(self) -> None:
        """Handle player death"""
        logger.info("Player died!")
        self.char = '%'  # Change to corpse symbol
        self.is_dead = True

    def add_gold(self, amount: int) -> None:
        """
        Add gold to player's inventory
        
        Args:
            amount: Amount of gold to add
        """
        self.stats['gold'] += amount
        logger.info(f"Added {amount} gold. Total: {self.gold}")

    def gain_exp(self, amount: int) -> None:
        """
        Add experience points and check for level up
        
        Args:
            amount: Amount of experience to gain
        """
        self.stats['exp'] += amount
        logger.info(f"Gained {amount} exp. Total: {self.exp}")
        
        # Check for level up
        while self.exp >= self._exp_to_next_level():
            self._level_up()

    def _exp_to_next_level(self) -> int:
        return self.level * LEVEL_UP_CONFIG['XP_MULTIPLIER']

    def _level_up(self) -> None:
        """Handle level up"""
        self.level += 1
        self.max_hp += LEVEL_UP_CONFIG['HP_INCREASE']
        self.hp = self.max_hp
        self.strength += LEVEL_UP_CONFIG['STRENGTH_INCREASE']
        logger.info(f"Level up! Now level {self.level}")

    def attack(self, target: 'Monster') -> tuple[bool, int]:
        """
        Attack a monster
        
        Args:
            target: Monster to attack
            
        Returns:
            tuple[bool, int]: (hit success, damage dealt)
        """
        # Calculate hit chance
        hit_chance = COMBAT_CONFIG['BASE_HIT_CHANCE'] + (
            self.level * COMBAT_CONFIG['LEVEL_HIT_BONUS']
        )
        
        # Check if attack hits
        if random.random() > hit_chance:
            return False, 0
            
        # Calculate damage
        base_damage = random.randint(1, self.strength)
        bonus_damage = int(self.strength * COMBAT_CONFIG['STRENGTH_DAMAGE_BONUS'])
        total_damage = max(COMBAT_CONFIG['MIN_DAMAGE'], base_damage + bonus_damage)
        
        # Apply damage to target
        target.take_damage(total_damage)
        
        # Grant experience if monster dies
        if target.is_dead:
            self.gain_exp(target.exp_value)
        
        return True, total_damage 