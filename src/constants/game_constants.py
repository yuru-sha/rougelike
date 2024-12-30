"""
Game constants and configuration values
"""

# Display characters
DISPLAY_CHARS = {
    'PLAYER': '@',
    'WALL': '#',
    'FLOOR': '.',
    'CORRIDOR': '#',
    'STAIRS_UP': '<',
    'STAIRS_DOWN': '>',
    'GOLD': '*',
    'AMULET': '"',
    'UNSEEN': ' ',
}

# Map generation
MAP_CONFIG = {
    'MIN_WIDTH': 80,
    'MIN_HEIGHT': 24,
    'MAX_ROOMS': 9,  # 3x3グリッド
    'MIN_ROOM_SIZE': 4,  # 最小サイズを小さく
    'MAX_ROOM_SIZE': 8,  # 最大サイズも調整
}

# Game rules
GAME_RULES = {
    'MAX_LEVEL': 26,
    'VIEW_RADIUS': 7,
    'MAX_INVENTORY': 23,
    'MAX_GOLD': 999999,
}

# Player stats
PLAYER_STATS = {
    'BASE_HP': 12,
    'BASE_STRENGTH': 16,
    'BASE_ARMOR': 0,
    'MAX_LEVEL': 21,
}

# Experience points needed for each level
XP_REQUIREMENTS = {
    level: level * 10000
    for level in range(1, 22)
}

# Colors using blessed/terminal
COLORS = {
    'STATUS': 'white_on_blue',
    'MESSAGE': 'yellow',
    'PLAYER': 'bright_white',
    'GOLD': 'yellow',
    'AMULET': 'bright_magenta',
    'STAIRS': 'bright_cyan',
}

# Gold generation
GOLD_CONFIG = {
    'MIN_AMOUNT': 2,      # Minimum gold per pile
    'MAX_AMOUNT': 250,    # Maximum gold per pile
    'MIN_PILES': 2,       # Minimum piles per level
    'MAX_PILES': 4        # Maximum piles per level
}

# Level up bonuses
LEVEL_UP_CONFIG = {
    'HP_INCREASE': 2,
    'STRENGTH_INCREASE': 1,
    'XP_MULTIPLIER': 10
}

# Scoring system
SCORE_CONFIG = {
    'LEVEL_MULTIPLIER': 1000,
    'DEPTH_MULTIPLIER': 500,
    'AMULET_BONUS': 20000
}

# Logging configuration
LOG_CONFIG = {
    'MAX_FILE_SIZE': 1024 * 1024,  # 1MB
    'BACKUP_COUNT': 2
}

# Combat system
COMBAT_CONFIG = {
    'BASE_HIT_CHANCE': 0.7,  # 基本命中率
    'LEVEL_HIT_BONUS': 0.05,  # レベルごとの命中ボーナス
    'STRENGTH_DAMAGE_BONUS': 0.5,  # 力の値による追加ダメージ係数
    'MIN_DAMAGE': 1,  # 最小ダメージ
    'ARMOR_REDUCTION': 0.1,  # 防具による軽減係数
}

# Monster definitions
MONSTER_CONFIG = {
    'BAT': {
        'char': 'B',
        'name': 'bat',
        'level': 1,
        'hp': 3,
        'strength': 3,
        'exp_value': 1
    },
    'SNAKE': {
        'char': 'S',
        'name': 'snake',
        'level': 2,
        'hp': 4,
        'strength': 5,  # 毒による追加ダメージ
        'exp_value': 2
    },
    'HOBGOBLIN': {
        'char': 'H',
        'name': 'hobgoblin',
        'level': 3,
        'hp': 6,
        'strength': 6,
        'exp_value': 3
    },
    'CENTAUR': {
        'char': 'C',
        'name': 'centaur',
        'level': 4,
        'hp': 8,
        'strength': 8,
        'exp_value': 5
    },
    'ICE_MONSTER': {
        'char': 'I',
        'name': 'ice monster',
        'level': 5,
        'hp': 7,
        'strength': 7,
        'exp_value': 5
    },
    'NYMPH': {
        'char': 'N',
        'name': 'nymph',
        'level': 6,
        'hp': 6,
        'strength': 6,
        'exp_value': 8  # アイテムを盗むため高い
    },
    'RUST_MONSTER': {
        'char': 'R',
        'name': 'rust monster',
        'level': 7,
        'hp': 10,
        'strength': 8,
        'exp_value': 10
    },
    'ZOMBIE': {
        'char': 'Z',
        'name': 'zombie',
        'level': 8,
        'hp': 15,
        'strength': 10,
        'exp_value': 12
    },
    'TROLL': {
        'char': 'T',
        'name': 'troll',
        'level': 12,
        'hp': 20,
        'strength': 15,
        'exp_value': 15
    },
    'YETI': {
        'char': 'Y',
        'name': 'yeti',
        'level': 13,
        'hp': 18,
        'strength': 14,
        'exp_value': 18
    },
    'WRAITH': {
        'char': 'W',
        'name': 'wraith',
        'level': 14,
        'hp': 25,
        'strength': 17,
        'exp_value': 25
    },
    'VAMPIRE': {
        'char': 'V',
        'name': 'vampire',
        'level': 15,
        'hp': 30,
        'strength': 20,
        'exp_value': 35
    },
    'DRAGON': {
        'char': 'D',
        'name': 'dragon',
        'level': 16,
        'hp': 40,
        'strength': 30,  # 一撃死の可能性
        'exp_value': 50
    },
    'AQUATOR': {
        'char': 'A',
        'name': 'aquator',
        'level': 5,
        'hp': 8,
        'strength': 6,
        'exp_value': 9
    },
    'LEPRECHAUN': {
        'char': 'L',
        'name': 'leprechaun',
        'level': 7,
        'hp': 6,
        'strength': 5,
        'exp_value': 10
    },
    'PHANTOM': {
        'char': 'P',
        'name': 'phantom',
        'level': 8,
        'hp': 12,
        'strength': 8,
        'exp_value': 13
    },
    'GRIFFIN': {
        'char': 'G',
        'name': 'griffin',
        'level': 9,
        'hp': 16,
        'strength': 13,
        'exp_value': 15
    },
    'MEDUSA': {
        'char': 'M',
        'name': 'medusa',
        'level': 10,
        'hp': 18,
        'strength': 14,
        'exp_value': 18
    },
    'UMBER_HULK': {
        'char': 'U',
        'name': 'umber hulk',
        'level': 11,
        'hp': 20,
        'strength': 16,
        'exp_value': 20
    },
    'XORN': {
        'char': 'X',
        'name': 'xorn',
        'level': 12,
        'hp': 22,
        'strength': 18,
        'exp_value': 22
    },
    'QUAGGA': {
        'char': 'Q',
        'name': 'quagga',
        'level': 6,
        'hp': 10,
        'strength': 9,
        'exp_value': 8
    },
    'ORC': {
        'char': 'O',
        'name': 'orc',
        'level': 4,
        'hp': 7,
        'strength': 7,
        'exp_value': 5
    },
    'DEMON': {
        'char': 'D',
        'name': 'demon',
        'level': 15,
        'hp': 35,
        'strength': 25,
        'exp_value': 45
    },
    'EMU': {
        'char': 'E',
        'name': 'emu',
        'level': 3,
        'hp': 5,
        'strength': 4,
        'exp_value': 2
    },
    'JABBERWOCK': {
        'char': 'J',
        'name': 'jabberwock',
        'level': 14,
        'hp': 32,
        'strength': 22,
        'exp_value': 40
    },
    'KESTREL': {
        'char': 'K',
        'name': 'kestrel',
        'level': 2,
        'hp': 4,
        'strength': 3,
        'exp_value': 2
    }
}

# Monster spawn configuration by dungeon level
MONSTER_SPAWN_CONFIG = {
    # 浅い階層 (1-5)
    1: [('BAT', 70), ('SNAKE', 30)],
    2: [('BAT', 50), ('SNAKE', 40), ('HOBGOBLIN', 10)],
    3: [('SNAKE', 40), ('HOBGOBLIN', 40), ('CENTAUR', 20)],
    4: [('HOBGOBLIN', 35), ('CENTAUR', 35), ('ICE_MONSTER', 30)],
    5: [('CENTAUR', 30), ('ICE_MONSTER', 40), ('NYMPH', 30)],
    
    # 中層 (6-15)
    6: [('ICE_MONSTER', 30), ('NYMPH', 30), ('RUST_MONSTER', 40)],
    7: [('NYMPH', 25), ('RUST_MONSTER', 45), ('ZOMBIE', 30)],
    8: [('RUST_MONSTER', 30), ('ZOMBIE', 50), ('TROLL', 20)],
    9: [('ZOMBIE', 40), ('TROLL', 40), ('YETI', 20)],
    10: [('TROLL', 45), ('YETI', 35), ('WRAITH', 20)],
    
    # 深層 (16-26)
    16: [('TROLL', 30), ('WRAITH', 40), ('VAMPIRE', 30)],
    20: [('WRAITH', 35), ('VAMPIRE', 45), ('DRAGON', 20)],
    24: [('VAMPIRE', 40), ('DRAGON', 40), ('WRAITH', 20)],
    26: [('DRAGON', 60), ('VAMPIRE', 40)]  # 最深層
}

# デフォルト設定（未定義のレベル用）
for i in range(11, 15):
    MONSTER_SPAWN_CONFIG[i] = MONSTER_SPAWN_CONFIG[10]
for i in range(17, 19):
    MONSTER_SPAWN_CONFIG[i] = MONSTER_SPAWN_CONFIG[16]
for i in range(21, 23):
    MONSTER_SPAWN_CONFIG[i] = MONSTER_SPAWN_CONFIG[20]
for i in range(25, 26):
    MONSTER_SPAWN_CONFIG[i] = MONSTER_SPAWN_CONFIG[24]

# Number of monsters per room
MONSTERS_PER_ROOM = {
    'MIN': 0,
    'MAX': 3,  # 深い階層ではより多くのモンスター
    'CHANCE': 0.8  # オリジナルに近い出現率
} 