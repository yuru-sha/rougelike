#!/usr/bin/env python3
from typing import Dict, Any, Tuple

# 近接武器の定義
MELEE_WEAPONS: Dict[str, Dict[str, Any]] = {
    'Mace': {
        'char': ')',
        'color': (192, 192, 192),
        'damage': (2, 4),  # 2d4
        'hit_bonus': 0,
        'levels': (1, 26),
        'two_handed': False
    },
    'Long Sword': {
        'char': ')',
        'color': (192, 192, 192),
        'damage': (3, 4),  # 3d4
        'hit_bonus': 0,
        'levels': (1, 26),
        'two_handed': False
    },
    'Two-Handed Sword': {
        'char': ')',
        'color': (192, 192, 192),
        'damage': (4, 4),  # 4d4
        'hit_bonus': 0,
        'levels': (1, 26),
        'two_handed': True
    },
    'Short Sword': {
        'char': ')',
        'color': (192, 192, 192),
        'damage': (2, 3),  # 2d3
        'hit_bonus': 0,
        'levels': (1, 26),
        'two_handed': False
    },
    'Dagger': {
        'char': ')',
        'color': (192, 192, 192),
        'damage': (1, 6),  # 1d6
        'hit_bonus': 0,
        'levels': (1, 26),
        'two_handed': False
    }
}

# 遠距離武器の定義
RANGED_WEAPONS: Dict[str, Dict[str, Any]] = {
    'Short Bow': {
        'char': '}',
        'color': (139, 69, 19),
        'damage': (1, 2),  # 1d2
        'hit_bonus': 1,
        'levels': (1, 26),
        'two_handed': True,
        'ranged': True,
        'ammo_type': 'arrow'
    },
    'Long Bow': {
        'char': '}',
        'color': (139, 69, 19),
        'damage': (1, 4),  # 1d4
        'hit_bonus': 1,
        'levels': (3, 26),
        'two_handed': True,
        'ranged': True,
        'ammo_type': 'arrow'
    },
    'Light Crossbow': {
        'char': '}',
        'color': (139, 69, 19),
        'damage': (2, 3),  # 2d3
        'hit_bonus': 2,
        'levels': (4, 26),
        'two_handed': True,
        'ranged': True,
        'ammo_type': 'bolt'
    },
    'Heavy Crossbow': {
        'char': '}',
        'color': (139, 69, 19),
        'damage': (2, 5),  # 2d5
        'hit_bonus': 2,
        'levels': (6, 26),
        'two_handed': True,
        'ranged': True,
        'ammo_type': 'bolt',
        'reload_time': 2
    }
}

# レア武器の定義
RARE_WEAPONS: Dict[str, Dict[str, Any]] = {
    'Vorpal Blade': {
        'char': ')',
        'color': (255, 215, 0),  # 金色
        'damage': (4, 6),  # 4d6
        'hit_bonus': 3,
        'levels': (15, 26),
        'two_handed': False,
        'special': 'vorpal'  # 一定確率で即死
    },
    'Frost Brand': {
        'char': ')',
        'color': (135, 206, 250),  # 水色
        'damage': (3, 6),  # 3d6
        'hit_bonus': 2,
        'levels': (12, 26),
        'two_handed': False,
        'special': 'frost'  # 追加の冷気ダメージ
    },
    'Flame Tongue': {
        'char': ')',
        'color': (255, 69, 0),  # オレンジ
        'damage': (3, 6),  # 3d6
        'hit_bonus': 2,
        'levels': (12, 26),
        'two_handed': False,
        'special': 'fire'  # 追加の炎ダメージ
    }
}

# 魔法武器の定義
MAGIC_WEAPONS: Dict[str, Dict[str, Any]] = {
    'Sword +1': {
        'char': ')',
        'color': (255, 255, 0),
        'damage': (2, 6),
        'hit_bonus': 1,
        'levels': (5, 26),
        'two_handed': False
    },
    'Sword +2': {
        'char': ')',
        'color': (255, 255, 0),
        'damage': (2, 8),
        'hit_bonus': 2,
        'levels': (10, 26),
        'two_handed': False
    },
    'Sword +3': {
        'char': ')',
        'color': (255, 255, 0),
        'damage': (3, 8),
        'hit_bonus': 3,
        'levels': (15, 26),
        'two_handed': False
    }
}

# 基本防具の定義
ARMORS: Dict[str, Dict[str, Any]] = {
    'Leather Armor': {
        'char': '[',
        'color': (139, 69, 19),
        'defense': 2,
        'weight': 15,
        'levels': (1, 26)
    },
    'Studded Leather': {
        'char': '[',
        'color': (139, 69, 19),
        'defense': 3,
        'weight': 20,
        'levels': (2, 26)
    },
    'Ring Mail': {
        'char': '[',
        'color': (192, 192, 192),
        'defense': 3,
        'weight': 25,
        'levels': (3, 26)
    },
    'Scale Mail': {
        'char': '[',
        'color': (192, 192, 192),
        'defense': 4,
        'weight': 30,
        'levels': (4, 26)
    },
    'Chain Mail': {
        'char': '[',
        'color': (192, 192, 192),
        'defense': 5,
        'weight': 35,
        'levels': (5, 26)
    },
    'Splint Mail': {
        'char': '[',
        'color': (192, 192, 192),
        'defense': 6,
        'weight': 40,
        'levels': (6, 26)
    },
    'Banded Mail': {
        'char': '[',
        'color': (192, 192, 192),
        'defense': 6,
        'weight': 45,
        'levels': (7, 26)
    },
    'Plate Mail': {
        'char': '[',
        'color': (192, 192, 192),
        'defense': 7,
        'weight': 50,
        'levels': (8, 26)
    }
}

# レア防具の定義
RARE_ARMORS: Dict[str, Dict[str, Any]] = {
    'Dragon Scale Mail': {
        'char': '[',
        'color': (255, 0, 0),  # 赤
        'defense': 9,
        'weight': 40,
        'levels': (20, 26),
        'special': 'fire_resist'
    },
    'Mithril Chain Mail': {
        'char': '[',
        'color': (192, 192, 192),  # 銀
        'defense': 8,
        'weight': 20,  # 通常の半分
        'levels': (15, 26),
        'special': 'light'
    },
    'Elven Chain Mail': {
        'char': '[',
        'color': (0, 255, 127),  # 緑
        'defense': 7,
        'weight': 25,
        'levels': (12, 26),
        'special': 'stealth'
    }
}

# 魔法防具の定義
MAGIC_ARMORS: Dict[str, Dict[str, Any]] = {
    'Armor +1': {
        'char': '[',
        'color': (255, 255, 0),
        'defense': 8,
        'weight': 50,
        'levels': (5, 26)
    },
    'Armor +2': {
        'char': '[',
        'color': (255, 255, 0),
        'defense': 9,
        'weight': 50,
        'levels': (10, 26)
    },
    'Armor +3': {
        'char': '[',
        'color': (255, 255, 0),
        'defense': 10,
        'weight': 50,
        'levels': (15, 26)
    }
}

# 基本盾の定義
SHIELDS: Dict[str, Dict[str, Any]] = {
    'Buckler': {
        'char': '(',
        'color': (192, 192, 192),
        'defense': 1,
        'weight': 5,
        'levels': (1, 26),
        'block_chance': 10
    },
    'Small Shield': {
        'char': '(',
        'color': (192, 192, 192),
        'defense': 2,
        'weight': 8,
        'levels': (2, 26),
        'block_chance': 15
    },
    'Large Shield': {
        'char': '(',
        'color': (192, 192, 192),
        'defense': 3,
        'weight': 12,
        'levels': (4, 26),
        'block_chance': 20
    },
    'Tower Shield': {
        'char': '(',
        'color': (192, 192, 192),
        'defense': 4,
        'weight': 15,
        'levels': (6, 26),
        'block_chance': 25
    }
}

# レア盾の定義
RARE_SHIELDS: Dict[str, Dict[str, Any]] = {
    'Dragon Scale Shield': {
        'char': '(',
        'color': (255, 0, 0),
        'defense': 5,
        'weight': 12,
        'levels': (15, 26),
        'block_chance': 30,
        'special': 'fire_resist'
    },
    'Mithril Shield': {
        'char': '(',
        'color': (192, 192, 192),
        'defense': 4,
        'weight': 6,
        'levels': (12, 26),
        'block_chance': 25,
        'special': 'light'
    },
    'Reflection Shield': {
        'char': '(',
        'color': (0, 191, 255),
        'defense': 3,
        'weight': 10,
        'levels': (10, 26),
        'block_chance': 20,
        'special': 'reflect'
    }
}

# 魔法盾の定義
MAGIC_SHIELDS: Dict[str, Dict[str, Any]] = {
    'Shield +1': {
        'char': '(',
        'color': (255, 255, 0),
        'defense': 3,
        'weight': 8,
        'levels': (5, 26),
        'block_chance': 20
    },
    'Shield +2': {
        'char': '(',
        'color': (255, 255, 0),
        'defense': 4,
        'weight': 8,
        'levels': (10, 26),
        'block_chance': 25
    },
    'Shield +3': {
        'char': '(',
        'color': (255, 255, 0),
        'defense': 5,
        'weight': 8,
        'levels': (15, 26),
        'block_chance': 30
    }
}

# 基本指輪の定義
RINGS: Dict[str, Dict[str, Any]] = {
    'Ring of Protection': {
        'char': '=',
        'color': (255, 215, 0),
        'defense': 1,
        'levels': (5, 26)
    },
    'Ring of Strength': {
        'char': '=',
        'color': (255, 0, 0),
        'strength': 1,
        'levels': (5, 26)
    },
    'Ring of Sustain': {
        'char': '=',
        'color': (0, 255, 0),
        'sustain': True,
        'levels': (7, 26)
    },
    'Ring of Searching': {
        'char': '=',
        'color': (0, 0, 255),
        'search': 2,
        'levels': (7, 26)
    }
}

# レア指輪の定義
RARE_RINGS: Dict[str, Dict[str, Any]] = {
    'Ring of Teleportation': {
        'char': '=',
        'color': (148, 0, 211),  # 紫
        'levels': (15, 26),
        'special': 'teleport'
    },
    'Ring of Regeneration': {
        'char': '=',
        'color': (0, 255, 0),  # 緑
        'levels': (12, 26),
        'special': 'regeneration',
        'heal_rate': 2
    },
    'Ring of Fire Resistance': {
        'char': '=',
        'color': (255, 69, 0),  # オレンジ
        'levels': (10, 26),
        'special': 'fire_resist'
    }
}

# 魔法指輪の定義
MAGIC_RINGS: Dict[str, Dict[str, Any]] = {
    'Ring of Protection +1': {
        'char': '=',
        'color': (255, 255, 0),
        'defense': 2,
        'levels': (5, 26)
    },
    'Ring of Protection +2': {
        'char': '=',
        'color': (255, 255, 0),
        'defense': 3,
        'levels': (10, 26)
    },
    'Ring of Protection +3': {
        'char': '=',
        'color': (255, 255, 0),
        'defense': 4,
        'levels': (15, 26)
    }
}

# 巻物の定義
SCROLLS: Dict[str, Dict[str, Any]] = {
    'Scroll of Identify': {
        'char': '?',
        'color': (255, 255, 255),
        'levels': (1, 26),
        'effect': 'identify'
    },
    'Scroll of Light': {
        'char': '?',
        'color': (255, 255, 0),
        'levels': (1, 26),
        'effect': 'light'
    },
    'Scroll of Remove Curse': {
        'char': '?',
        'color': (0, 255, 255),
        'levels': (2, 26),
        'effect': 'remove_curse'
    },
    'Scroll of Enchant Weapon': {
        'char': '?',
        'color': (255, 0, 0),
        'levels': (4, 26),
        'effect': 'enchant_weapon'
    },
    'Scroll of Enchant Armor': {
        'char': '?',
        'color': (0, 255, 0),
        'levels': (4, 26),
        'effect': 'enchant_armor'
    },
    'Scroll of Teleportation': {
        'char': '?',
        'color': (148, 0, 211),
        'levels': (5, 26),
        'effect': 'teleport'
    },
    'Scroll of Scare Monster': {
        'char': '?',
        'color': (255, 69, 0),
        'levels': (3, 26),
        'effect': 'scare'
    }
}

# 薬の定義
POTIONS: Dict[str, Dict[str, Any]] = {
    'Potion of Healing': {
        'char': '!',
        'color': (255, 0, 0),
        'levels': (1, 26),
        'effect': 'heal',
        'amount': 15
    },
    'Potion of Extra Healing': {
        'char': '!',
        'color': (255, 0, 0),
        'levels': (3, 26),
        'effect': 'heal',
        'amount': 30
    },
    'Potion of Gain Strength': {
        'char': '!',
        'color': (255, 165, 0),
        'levels': (4, 26),
        'effect': 'gain_strength',
        'amount': 1
    },
    'Potion of Restore Strength': {
        'char': '!',
        'color': (255, 140, 0),
        'levels': (2, 26),
        'effect': 'restore_strength'
    },
    'Potion of Confusion': {
        'char': '!',
        'color': (148, 0, 211),
        'levels': (1, 26),
        'effect': 'confusion',
        'duration': 20
    },
    'Potion of Poison': {
        'char': '!',
        'color': (0, 100, 0),
        'levels': (1, 26),
        'effect': 'poison',
        'damage': 3
    },
    'Potion of See Invisible': {
        'char': '!',
        'color': (0, 255, 255),
        'levels': (2, 26),
        'effect': 'see_invisible',
        'duration': 100
    }
}

# 食料の定義
FOODS: Dict[str, Dict[str, Any]] = {
    'Ration': {
        'char': '%',
        'color': (139, 69, 19),
        'levels': (1, 26),
        'nutrition': 850
    },
    'Slime Mold': {
        'char': '%',
        'color': (0, 255, 0),
        'levels': (2, 26),
        'nutrition': 500
    }
}

# 矢と矢筒の定義
AMMO: Dict[str, Dict[str, Any]] = {
    'Arrow': {
        'char': ']',
        'color': (139, 69, 19),
        'damage': (1, 2),
        'levels': (1, 26),
        'ammo_type': 'arrow',
        'stack_size': 20
    },
    'Bolt': {
        'char': ']',
        'color': (139, 69, 19),
        'damage': (1, 3),
        'levels': (1, 26),
        'ammo_type': 'bolt',
        'stack_size': 20
    },
    'Silver Arrow': {
        'char': ']',
        'color': (192, 192, 192),
        'damage': (2, 3),
        'levels': (5, 26),
        'ammo_type': 'arrow',
        'stack_size': 10,
        'special': 'undead_bonus'
    }
}

# 杖の定義
WANDS: Dict[str, Dict[str, Any]] = {
    'Wand of Magic Missile': {
        'char': '/',
        'color': (255, 0, 0),
        'levels': (1, 26),
        'effect': 'magic_missile',
        'damage': (2, 5),
        'charges': (10, 15)
    },
    'Wand of Lightning': {
        'char': '/',
        'color': (255, 255, 0),
        'levels': (4, 26),
        'effect': 'lightning',
        'damage': (4, 6),
        'charges': (8, 12)
    },
    'Wand of Fire': {
        'char': '/',
        'color': (255, 69, 0),
        'levels': (6, 26),
        'effect': 'fire',
        'damage': (6, 8),
        'charges': (6, 10)
    },
    'Wand of Cold': {
        'char': '/',
        'color': (0, 191, 255),
        'levels': (5, 26),
        'effect': 'cold',
        'damage': (5, 7),
        'charges': (7, 11)
    },
    'Wand of Polymorph': {
        'char': '/',
        'color': (148, 0, 211),
        'levels': (7, 26),
        'effect': 'polymorph',
        'charges': (5, 8)
    },
    'Wand of Slow Monster': {
        'char': '/',
        'color': (0, 255, 0),
        'levels': (2, 26),
        'effect': 'slow',
        'charges': (10, 15)
    },
    'Wand of Teleportation': {
        'char': '/',
        'color': (0, 255, 255),
        'levels': (5, 26),
        'effect': 'teleport',
        'charges': (8, 12)
    }
}

# アイテム出現確率の更新
ITEM_CHANCES: Dict[str, int] = {
    'healing_potion': 20,
    'extra_healing_potion': 10,
    'gain_strength_potion': 5,
    'restore_strength_potion': 5,
    'confusion_potion': 5,
    'poison_potion': 5,
    'see_invisible_potion': 5,
    'identify_scroll': 10,
    'light_scroll': 8,
    'remove_curse_scroll': 7,
    'enchant_weapon_scroll': 5,
    'enchant_armor_scroll': 5,
    'teleportation_scroll': 5,
    'scare_monster_scroll': 5,
    'magic_missile_wand': 5,
    'lightning_wand': 3,
    'fire_wand': 2,
    'cold_wand': 2,
    'polymorph_wand': 1,
    'slow_monster_wand': 3,
    'teleportation_wand': 2,
    'food': 15,
    'arrow': 10,
    'bolt': 8,
    'silver_arrow': 2,
    'melee_weapon': 8,
    'ranged_weapon': 5,
    'armor': 8,
    'shield': 8,
    'ring': 5,
    'magic_weapon': 2,
    'magic_armor': 2,
    'magic_shield': 2,
    'magic_ring': 2,
    'rare_weapon': 1,
    'rare_armor': 1,
    'rare_shield': 1,
    'rare_ring': 1
} 