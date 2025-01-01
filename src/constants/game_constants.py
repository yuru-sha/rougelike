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
    'MAX_ROOMS': 30,
    'MIN_ROOM_SIZE': 6,
    'MAX_ROOM_SIZE': 10,
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
    'MAX_LEVEL': 20,
}

# Experience points needed for each level
XP_REQUIREMENTS = {
    level: level * 1000
    for level in range(1, 21)
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