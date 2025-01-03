#!/usr/bin/env python3
from typing import List, Optional, Dict, Any, Tuple
import random
from .tile import Tile, Rectangle
from config.constants import (
    ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAX_ROOMS,
    MAX_MONSTERS_PER_ROOM, MAX_ITEMS_PER_ROOM, MAX_GOLD_PER_ROOM,
    GOLD_MIN_AMOUNT, GOLD_MAX_AMOUNT
)
from config.monsters import MONSTERS
from config.items import (
    MELEE_WEAPONS, RANGED_WEAPONS, RARE_WEAPONS, MAGIC_WEAPONS,
    ARMORS, RARE_ARMORS, MAGIC_ARMORS,
    RINGS, RARE_RINGS, MAGIC_RINGS,
    ITEM_CHANCES
)
from entity.entity import Entity, EntityType

class GameMap:
    def __init__(self, width: int, height: int, dungeon_level: int):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level
        self.tiles = self._initialize_tiles()
    
    def _initialize_tiles(self) -> List[List[Tile]]:
        return [[Tile(walkable=False, transparent=False)
                 for y in range(self.height)]
                for x in range(self.width)]
    
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _create_room(self, room: Rectangle) -> None:
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].walkable = True
                self.tiles[x][y].transparent = True
    
    def _create_h_tunnel(self, x1: int, x2: int, y: int) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True
    
    def _create_v_tunnel(self, y1: int, y2: int, x: int) -> None:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True

    def _place_entities(self, room: Rectangle, entities: List[Entity]) -> None:
        self._place_monsters(room, entities)
        self._place_items(room, entities)
        self._place_gold(room, entities)

    def _place_monsters(self, room: Rectangle, entities: List[Entity]) -> None:
        # このフロアに出現可能なモンスターをフィルタリング
        possible_monsters = {
            name: data for name, data in MONSTERS.items()
            if self.dungeon_level >= data['min_level'] and
            self.dungeon_level <= data['max_level']
        }

        if not possible_monsters:
            return

        # モンスターの数を決定
        number_of_monsters = random.randint(0, MAX_MONSTERS_PER_ROOM)

        for _ in range(number_of_monsters):
            # モンスターの位置をランダムに決定
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            # 他のエンティティと重ならないかチェック
            if not any(entity.x == x and entity.y == y for entity in entities):
                # モンスターをランダムに選択
                monster_name = random.choice(list(possible_monsters.keys()))
                monster_data = possible_monsters[monster_name]

                monster = Entity(
                    x=x,
                    y=y,
                    char=monster_data['char'],
                    color=monster_data['color'],
                    name=monster_name,
                    entity_type=EntityType.MONSTER,
                    blocks=True,
                    hp=self._roll_hp(monster_data['hp']),
                    max_hp=self._roll_hp(monster_data['hp']),
                    power=monster_data['damage'],
                    xp_given=monster_data['xp'],
                    speed=monster_data.get('speed', 1.0),
                    special=monster_data.get('special'),
                    regeneration=monster_data.get('regeneration', False),
                    sight_radius=monster_data.get('sight_radius', 8)
                )

                entities.append(monster)

    def _roll_hp(self, hp_dice: Tuple[int, int]) -> int:
        """
        HPをロールする
        hp_dice: (基本HP, ダイス数)のタプル
        """
        base_hp, dice = hp_dice
        return base_hp + random.randint(1, dice)

    def _place_items(self, room: Rectangle, entities: List[Entity]) -> None:
        number_of_items = random.randint(0, MAX_ITEMS_PER_ROOM)

        for _ in range(number_of_items):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                item = self._create_item(x, y)
                if item:
                    entities.append(item)

    def _create_item(self, x: int, y: int) -> Optional[Entity]:
        roll = random.randint(1, 100)
        total = 0

        for item_name, chance in ITEM_CHANCES.items():
            total += chance
            if roll <= total:
                if item_name == 'healing_potion':
                    return Entity(
                        x, y, '!', (127, 0, 0), 'Healing Potion',
                        EntityType.ITEM, blocks=False,
                        effect='heal', effect_amount=4
                    )
                elif item_name == 'lightning_scroll':
                    return Entity(
                        x, y, '?', (0, 127, 127), 'Lightning Scroll',
                        EntityType.ITEM, blocks=False,
                        effect='lightning', effect_amount=5
                    )
                elif item_name == 'fireball_scroll':
                    return Entity(
                        x, y, '?', (127, 127, 0), 'Fireball Scroll',
                        EntityType.ITEM, blocks=False,
                        effect='fireball', effect_amount=3
                    )
                elif item_name == 'confusion_scroll':
                    return Entity(
                        x, y, '?', (127, 0, 127), 'Confusion Scroll',
                        EntityType.ITEM, blocks=False,
                        effect='confusion', effect_amount=4
                    )
                elif item_name == 'teleport_scroll':
                    return Entity(
                        x, y, '?', (0, 255, 255), 'Teleport Scroll',
                        EntityType.ITEM, blocks=False,
                        effect='teleport', effect_amount=0
                    )
                elif item_name == 'weapon':
                    weapon_name = random.choice(list(WEAPONS.keys()))
                    return self._create_weapon(x, y, weapon_name)
                elif item_name == 'armor':
                    armor_name = random.choice(list(ARMORS.keys()))
                    return self._create_armor(x, y, armor_name)
                elif item_name == 'ring':
                    ring_name = random.choice(list(RINGS.keys()))
                    return self._create_ring(x, y, ring_name)
        return None

    def _create_weapon(self, x: int, y: int, weapon_name: str) -> Entity:
        weapon_data = WEAPONS[weapon_name]
        return Entity(
            x, y,
            weapon_data['char'],
            weapon_data['color'],
            weapon_name,
            EntityType.WEAPON,
            blocks=False,
            damage_dice=weapon_data['damage'],
            hit_bonus=weapon_data['hit_bonus'],
            two_handed=weapon_data['two_handed'],
            ranged=weapon_data.get('ranged', False)
        )

    def _create_armor(self, x: int, y: int, armor_name: str) -> Entity:
        armor_data = ARMORS[armor_name]
        return Entity(
            x, y,
            armor_data['char'],
            armor_data['color'],
            armor_name,
            EntityType.ARMOR,
            blocks=False,
            defense=armor_data['defense'],
            weight=armor_data['weight']
        )

    def _create_ring(self, x: int, y: int, ring_name: str) -> Entity:
        ring_data = RINGS[ring_name]
        return Entity(
            x, y,
            ring_data['char'],
            ring_data['color'],
            ring_name,
            EntityType.RING,
            blocks=False,
            defense=ring_data.get('defense', 0),
            strength=ring_data.get('strength', 0),
            sustain=ring_data.get('sustain', False),
            search=ring_data.get('search', 0)
        )

    def _place_gold(self, room: Rectangle, entities: List[Entity]) -> None:
        number_of_gold = random.randint(0, MAX_GOLD_PER_ROOM)

        for _ in range(number_of_gold):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                gold_amount = random.randint(GOLD_MIN_AMOUNT, GOLD_MAX_AMOUNT)
                gold = Entity(
                    x, y, '$', (255, 215, 0), f'{gold_amount} Gold',
                    EntityType.GOLD, blocks=False, gold_amount=gold_amount
                )
                entities.append(gold)

    def make_map(self, player: Entity, entities: List[Entity]) -> None:
        rooms: List[Rectangle] = []

        for _ in range(MAX_ROOMS):
            room = self._create_random_room()
            
            if not any(room.intersects(other_room) for other_room in rooms):
                self._create_room(room)
                new_x, new_y = room.center
                
                if not rooms:
                    player.x, player.y = new_x, new_y
                else:
                    prev_x, prev_y = rooms[-1].center
                    self._connect_rooms(prev_x, prev_y, new_x, new_y)
                
                self._place_entities(room, entities)
                rooms.append(room)

        self._place_special_entities(rooms, player, entities)

    def _create_random_room(self) -> Rectangle:
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(0, self.width - w - 1)
        y = random.randint(0, self.height - h - 1)
        return Rectangle(x, y, w, h)

    def _connect_rooms(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if random.random() < 0.5:
            self._create_h_tunnel(x1, x2, y1)
            self._create_v_tunnel(y1, y2, x2)
        else:
            self._create_v_tunnel(y1, y2, x1)
            self._create_h_tunnel(x1, x2, y2)

    def _place_special_entities(self, rooms: List[Rectangle], player: Entity, entities: List[Entity]) -> None:
        if self.dungeon_level == 26:
            self._try_place_amulet(rooms, entities)
        self._place_stairs(rooms, entities)

    def _try_place_amulet(self, rooms: List[Rectangle], entities: List[Entity]) -> None:
        if len(rooms) > 0:
            room = random.choice(rooms)
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                amulet = Entity(
                    x, y, '"', (255, 255, 0), 'The Amulet of Yendor',
                    EntityType.AMULET, blocks=False
                )
                entities.append(amulet)

    def _place_stairs(self, rooms: List[Rectangle], entities: List[Entity]) -> None:
        if len(rooms) > 0:
            room = random.choice(rooms)
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                stairs = Entity(
                    x, y, '>', (255, 255, 255), 'Stairs',
                    EntityType.STAIRS_DOWN, blocks=False
                )
                entities.append(stairs) 