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