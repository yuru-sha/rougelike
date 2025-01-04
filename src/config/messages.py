#!/usr/bin/env python3
from typing import Dict

MESSAGES: Dict[str, str] = {
    # Combat messages
    "heal": "You begin to feel better.",
    "monster_death": "dies in a fit of agony",
    "player_hit": "hits you",
    "player_miss": "miss",
    "monster_miss": "misses you",
    "player_kill": "You defeated the {}!",
    "player_attack": "You attack the {}",
    "player_damage": "You hit the {} for {} damage",
    "monster_attack": "The {} attacks you",
    "monster_damage": "The {} hits you for {} damage",
    "player_dodge": "You dodge the {}'s attack",
    "monster_dodge": "The {} dodges your attack",
    "player_block": "You block the {}'s attack with your {}",
    "monster_block": "The {} blocks your attack",
    "player_crit": "You land a critical hit on the {}!",
    "monster_crit": "The {} lands a critical hit!",
    "player_weak": "You are too weak to fight effectively",
    "monster_flees": "The {} flees in terror!",
    "monster_appears": "A {} appears!",
    "monster_wounded": "The {} appears to be wounded",
    "monster_healthy": "The {} appears to be healthy",
    "monster_enraged": "The {} becomes enraged!",
    "weapon_ineffective": "Your {} seems ineffective against the {}",
    "armor_protection": "Your {} protects you from the {}'s attack",
    
    # Inventory messages
    "inventory_empty": "Your inventory is empty.",
    "cant_carry": "You can't carry anything else.",
    "nothing_here": "There is nothing here to pick up.",
    "picked_up": "You picked up {}.",
    "dropped": "You dropped {}.",
    "wielding": "You are now wielding {}.",
    "wearing": "You are now wearing {}.",
    "already_wielding": "You are already wielding that.",
    "already_wearing": "You are already wearing that.",
    "cant_wield": "You can't wield that.",
    "cant_wear": "You can't wear that.",
    "remove_first": "You'll have to remove {} first.",
    
    # Gold messages
    "gold_found": "You found {} gold pieces.",
    "gold_picked": "You pick up {} gold pieces.",
    "gold_dropped": "You drop {} gold pieces.",
    
    # Status messages
    "level_up": "Welcome to level {}! You feel stronger!",
    "strength_up": "You feel stronger! Your strength is now {}.",
    "hungry": "You are hungry.",
    "weak": "You are feeling weak.",
    "faint": "You are about to faint from hunger!",
    "confused": "You feel confused.",
    "blind": "You can't see anything!",
    "hallucination": "Oh wow! Everything looks so cosmic!",
    "poisoned": "You feel very sick.",
    
    # Dungeon messages
    "amulet_nearby": "You feel something special nearby...",
    "amulet_power": "The Amulet of Yendor pulses with ancient power...",
    "welcome_level": "Welcome to level {} of the Dungeons of Doom!",
    "trap_door": "A trap door opens up beneath your feet!",
    "bear_trap": "You are caught in a bear trap.",
    "teleport_trap": "You feel disoriented...",
    "poison_dart": "A small dart hits you!",
    "sleeping_gas": "A cloud of gas surrounds you...",
    "hidden_passage": "You found a hidden passage!",
    
    # Magic messages
    "scroll_identify": "This is a scroll of {}.",
    "potion_effect": "You feel {}!",
    "spell_cast": "You cast {}.",
    "magic_fails": "The magic fails.",
    
    # Game state messages
    "victory": "You escaped with the Amulet of Yendor!\nCongratulations! You won the game!",
    "death": "You have died...\nPress any key to continue",
    "save": "Game saved.",
    "load": "Welcome back to the Dungeons of Doom!",
    
    # Combat status
    "critical_hit": "Critical hit!",
    "dodge": "You dodge the attack!",
    "blocked": "You blocked the attack!",
    "armor_breaks": "Your armor is damaged!",
    "weapon_breaks": "Your weapon breaks!",
    
    # Item discovery
    "cursed": "Oops... this seems to be cursed.",
    "blessed": "This item is blessed!",
    "enchanted": "Your {} glows blue for a moment.",
    "disenchanted": "Your {} glows red for a moment.",
    
    # Special events
    "shop_welcome": "Welcome to my shop! Feel free to browse.",
    "shop_thanks": "Thank you for your purchase!",
    "shop_poor": "You don't have enough gold.",
    "altar_find": "You have found an altar.",
    "fountain_find": "You have found a fountain.",
    "throne_find": "You have found a throne.",
}
