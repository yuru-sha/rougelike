"""
Base monster class implementation
"""
from typing import Optional
from entities.entity import Entity
from utils.logger import get_logger
import random
from constants.game_constants import COMBAT_CONFIG

logger = get_logger(__name__)

class Monster(Entity):
    """
    Base class for all monsters in the game
    Handles common monster behavior like combat and death
    """
    def __init__(
        self, 
        x: int, 
        y: int,
        char: str,
        name: str,
        level: int,
        hp: int,
        strength: int,
        exp_value: int
    ):
        super().__init__(x, y, char, name, blocks_movement=True)
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.strength = strength
        self.exp_value = exp_value
        self.is_dead = False

    def take_damage(self, amount: int) -> None:
        """Apply damage to monster and check for death"""
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.die()

    def die(self) -> None:
        """Handle monster death state changes"""
        self.is_dead = True
        self.char = '%'  # Change to corpse
        self.blocks_movement = False 

    def attack(self, target: 'Player') -> tuple[bool, int]:
        """
        Attack a target and calculate damage
        
        Args:
            target: The target to attack (usually the player)
            
        Returns:
            tuple[bool, int]: (hit success, damage dealt)
        """
        # Calculate hit chance with level bonus
        hit_chance = COMBAT_CONFIG['BASE_HIT_CHANCE'] + (
            self.level * COMBAT_CONFIG['LEVEL_HIT_BONUS']
        )
        
        if random.random() > hit_chance:
            return False, 0
            
        # Calculate total damage with strength bonus
        base_damage = random.randint(1, self.strength)
        bonus_damage = int(self.strength * COMBAT_CONFIG['STRENGTH_DAMAGE_BONUS'])
        total_damage = max(COMBAT_CONFIG['MIN_DAMAGE'], base_damage + bonus_damage)
        
        # Apply armor reduction
        armor_reduction = int(target.armor_class * COMBAT_CONFIG['ARMOR_REDUCTION'])
        final_damage = max(COMBAT_CONFIG['MIN_DAMAGE'], total_damage - armor_reduction)
        
        target.take_damage(final_damage)
        
        return True, final_damage 