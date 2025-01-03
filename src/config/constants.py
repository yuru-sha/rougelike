#!/usr/bin/env python3
from typing import Dict, Tuple

# Game Constants
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 46  # マップ表示領域
STATUS_HEIGHT = 1  # ステータスバー（上部）
MESSAGE_HEIGHT = 3  # メッセージ領域（下部）
ROOM_MAX_SIZE = 8  # Rogueの部屋サイズ
ROOM_MIN_SIZE = 4  # Rogueの部屋サイズ
MAX_ROOMS = 9  # Rogueの部屋数
MAX_DUNGEON_LEVEL = 26
INVENTORY_CAPACITY = 26

# Entity Generation Settings
MAX_MONSTERS_PER_ROOM = 4  # Rogueに準拠
MAX_ITEMS_PER_ROOM = 4    # Rogueに準拠
MAX_GOLD_PER_ROOM = 2
GOLD_MIN_AMOUNT = 10
GOLD_MAX_AMOUNT = 50

# Player Stats
PLAYER_START_HP = 12
PLAYER_START_STRENGTH = 16
PLAYER_START_DAMAGE = (1, 4)  # 1d4

# Starting Equipment Settings
STARTING_WEAPON_POWER = 1  # 短剣の基本ダメージ
STARTING_WEAPON_DICE = 6   # 短剣は1d6
STARTING_WEAPON_BONUS = 1  # 短剣は+1
STARTING_BOW_POWER = 1     # 弓の基本ダメージ
STARTING_BOW_DICE = 2      # 弓は1d2
STARTING_ARROWS = 25       # 初期矢の数
STARTING_FOOD = 5          # 初期食料の数

# Display Characters
CHARS: Dict[str, str] = {
    'player': '@',
    'wall': '#',
    'floor': '.',
    'orc': 'o',
    'troll': 'T',
    'stairs_down': '>',
    'stairs_up': '<',
    'potion': '!',
    'scroll': '?',
    'gold': '$',
    'amulet': '"',
    'weapon': ')',
    'bow': '}',
    'arrow': ']',
    'food': '%'
}

# Colors
COLORS: Dict[str, Tuple[int, int, int]] = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (255, 0, 255),
    'cyan': (0, 255, 255),
    'brown': (139, 69, 19),
    'gray': (128, 128, 128),
    'light_gray': (192, 192, 192),
    'dark_gray': (64, 64, 64),
    'orange': (255, 165, 0),
    'gold': (255, 215, 0)
}

# Game Settings
TITLE = "Roguelike Game"
AMULET_GENERATED = False 