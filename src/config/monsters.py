#!/usr/bin/env python3
from typing import Dict, Tuple, Any

MONSTERS: Dict[str, Dict[str, Any]] = {
    'Bat': {
        'char': 'B',
        'color': (139, 69, 19),  # 茶色
        'hp': (1, 8),  # 1d8
        'damage': (1, 2),  # 1d2
        'xp': 2,
        'min_level': 1,
        'max_level': 8,
        'speed': 2.0,  # 移動速度（通常の2倍）
        'sight_radius': 6
    },
    'Snake': {
        'char': 'S',
        'color': (0, 255, 0),  # 緑
        'hp': (2, 6),  # 2d6
        'damage': (1, 3),  # 1d3
        'xp': 3,
        'min_level': 2,
        'max_level': 9,
        'speed': 1.0,
        'sight_radius': 5
    },
    'Hobgoblin': {
        'char': 'H',
        'color': (139, 69, 19),
        'hp': (1, 8),
        'damage': (1, 8),
        'xp': 3,
        'min_level': 1,
        'max_level': 10,
        'speed': 1.0,
        'sight_radius': 7
    },
    'Kestrel': {
        'char': 'K',
        'color': (165, 42, 42),  # 茶色
        'hp': (1, 6),
        'damage': (1, 4),
        'xp': 2,
        'min_level': 1,
        'max_level': 7,
        'speed': 1.5,
        'sight_radius': 8
    },
    'Aquator': {
        'char': 'A',
        'color': (0, 191, 255),  # 水色
        'hp': (5, 10),
        'damage': (0, 0),  # 武器を錆びさせる特殊能力
        'xp': 15,
        'min_level': 7,
        'max_level': 16,
        'speed': 1.0,
        'sight_radius': 7,
        'special': 'rust'
    },
    'Zombie': {
        'char': 'Z',
        'color': (169, 169, 169),  # 灰色
        'hp': (6, 12),
        'damage': (1, 8),
        'xp': 7,
        'min_level': 4,
        'max_level': 14,
        'speed': 0.5,  # 遅い
        'sight_radius': 6,
        'special': 'undead'
    },
    'Troll': {
        'char': 'T',
        'color': (0, 100, 0),  # 濃い緑
        'hp': (6, 16),
        'damage': (2, 8),
        'xp': 120,
        'min_level': 13,
        'max_level': 26,
        'speed': 1.0,
        'sight_radius': 7,
        'regeneration': True
    },
    'Dragon': {
        'char': 'D',
        'color': (255, 0, 0),  # 赤
        'hp': (10, 20),
        'damage': (3, 10),
        'xp': 5000,
        'min_level': 21,
        'max_level': 26,
        'speed': 1.0,
        'sight_radius': 8,
        'special': 'fire'
    },
    'Ice Monster': {
        'char': 'I',
        'color': (0, 191, 255),  # 水色
        'hp': (1, 8),
        'damage': (0, 0),
        'xp': 5,
        'min_level': 2,
        'max_level': 11,
        'speed': 1.0,
        'sight_radius': 6,
        'special': 'freeze'  # 一時的に動けなくする
    },
    'Centaur': {
        'char': 'C',
        'color': (139, 69, 19),  # 茶色
        'hp': (4, 8),
        'damage': (1, 6),
        'xp': 15,
        'min_level': 4,
        'max_level': 12,
        'speed': 1.5,  # 速い
        'sight_radius': 7
    },
    'Wraith': {
        'char': 'W',
        'color': (128, 128, 128),  # 灰色
        'hp': (3, 6),
        'damage': (1, 6),
        'xp': 25,
        'min_level': 8,
        'max_level': 15,
        'speed': 1.0,
        'sight_radius': 7,
        'special': 'level_drain'  # レベルを下げる
    },
    'Nymph': {
        'char': 'N',
        'color': (0, 255, 127),  # 緑
        'hp': (3, 6),
        'damage': (0, 0),
        'xp': 25,
        'min_level': 11,
        'max_level': 18,
        'speed': 1.2,
        'sight_radius': 6,
        'special': 'steal'  # アイテムを盗む
    },
    'Quasit': {
        'char': 'Q',
        'color': (255, 0, 255),  # マゼンタ
        'hp': (3, 7),
        'damage': (1, 5),
        'xp': 30,
        'min_level': 10,
        'max_level': 17,
        'speed': 1.7,  # とても速い
        'sight_radius': 7,
        'special': 'invisible'  # 時々透明になる
    },
    'Rattlesnake': {
        'char': 'S',
        'color': (255, 165, 0),  # オレンジ
        'hp': (2, 5),
        'damage': (1, 3),
        'xp': 10,
        'min_level': 3,
        'max_level': 10,
        'speed': 1.0,
        'sight_radius': 5,
        'special': 'poison'  # 毒を与える
    },
    'Vampire': {
        'char': 'V',
        'color': (139, 0, 0),  # 暗い赤
        'hp': (8, 16),
        'damage': (1, 10),
        'xp': 350,
        'min_level': 16,
        'max_level': 23,
        'speed': 1.2,
        'sight_radius': 8,
        'special': 'drain_life',  # 生命力を吸収
        'regeneration': True
    },
    'Xeroc': {
        'char': 'X',
        'color': (255, 255, 255),  # 白
        'hp': (7, 12),
        'damage': (2, 6),
        'xp': 90,
        'min_level': 12,
        'max_level': 19,
        'speed': 1.0,
        'sight_radius': 7,
        'special': 'mimic'  # 他のモンスターに化ける
    },
    'Yeti': {
        'char': 'Y',
        'color': (255, 250, 250),  # 雪色
        'hp': (4, 10),
        'damage': (2, 6),
        'xp': 50,
        'min_level': 11,
        'max_level': 18,
        'speed': 1.0,
        'sight_radius': 6,
        'special': 'cold'  # 冷気攻撃
    },
    'Phantom': {
        'char': 'P',
        'color': (169, 169, 169),  # 灰色
        'hp': (5, 12),
        'damage': (2, 4),
        'xp': 120,
        'min_level': 14,
        'max_level': 22,
        'speed': 1.0,
        'sight_radius': 7,
        'special': 'invisible',  # 常に透明
        'regeneration': True
    },
    'Medusa': {
        'char': 'M',
        'color': (0, 255, 0),  # 緑
        'hp': (8, 16),
        'damage': (3, 7),
        'xp': 200,
        'min_level': 18,
        'max_level': 25,
        'speed': 1.0,
        'sight_radius': 8,
        'special': 'petrify'  # 石化
    },
    'Griffin': {
        'char': 'G',
        'color': (218, 165, 32),  # ゴールド
        'hp': (7, 14),
        'damage': (2, 8),
        'xp': 150,
        'min_level': 15,
        'max_level': 22,
        'speed': 1.5,
        'sight_radius': 8,
        'special': 'fly'  # 飛行能力
    },
    'Leprechaun': {
        'char': 'L',
        'color': (0, 255, 0),  # 緑
        'hp': (3, 7),
        'damage': (1, 2),
        'xp': 10,
        'min_level': 6,
        'max_level': 13,
        'speed': 1.3,
        'sight_radius': 6,
        'special': 'steal_gold'  # 金を盗む
    },
    'Umber Hulk': {
        'char': 'U',
        'color': (139, 69, 19),  # 茶色
        'hp': (8, 16),
        'damage': (3, 7),
        'xp': 180,
        'min_level': 17,
        'max_level': 24,
        'speed': 1.0,
        'sight_radius': 7,
        'special': 'confuse'  # 混乱させる
    },
    'Floating Eye': {
        'char': 'E',
        'color': (0, 191, 255),  # 水色
        'hp': (1, 8),
        'damage': (0, 0),
        'xp': 2,
        'min_level': 1,
        'max_level': 7,
        'speed': 0.5,
        'sight_radius': 5,
        'special': 'paralyze'  # 一時的に麻痺させる
    },
    'Rust Monster': {
        'char': 'R',
        'color': (139, 69, 19),  # 茶色
        'hp': (2, 8),
        'damage': (0, 0),
        'xp': 20,
        'min_level': 8,
        'max_level': 17,
        'speed': 1.0,
        'sight_radius': 6,
        'special': 'rust'  # 武器や防具を錆びさせる
    },
    'Orc': {
        'char': 'O',
        'color': (0, 255, 0),  # 緑
        'hp': (1, 8),
        'damage': (1, 6),
        'xp': 5,
        'min_level': 1,
        'max_level': 10,
        'speed': 1.0,
        'sight_radius': 7
    },
    'Mimic': {
        'char': 'm',
        'color': (139, 69, 19),  # 茶色
        'hp': (7, 12),
        'damage': (3, 7),
        'xp': 140,
        'min_level': 15,
        'max_level': 24,
        'speed': 1.0,
        'sight_radius': 7,
        'special': 'mimic'  # アイテムに化ける
    },
    'Invisible Stalker': {
        'char': 'I',
        'color': (255, 255, 255),  # 白（実際には見えない）
        'hp': (8, 16),
        'damage': (2, 8),
        'xp': 120,
        'min_level': 13,
        'max_level': 22,
        'speed': 1.2,
        'sight_radius': 8,
        'special': 'invisible'  # 常に透明
    },
    'Giant Ant': {
        'char': 'A',
        'color': (139, 69, 19),  # 茶色
        'hp': (2, 6),
        'damage': (1, 4),
        'xp': 5,
        'min_level': 2,
        'max_level': 9,
        'speed': 1.5,
        'sight_radius': 6
    }
} 