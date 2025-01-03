#!/usr/bin/env python3
import tcod
from typing import Optional, Set, Tuple, List, Dict, Callable
import random
from enum import Enum, auto
from tcod import libtcodpy

# Game Constants
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 37
MAP_WIDTH = 50
MAP_HEIGHT = 32
ROOM_MAX_SIZE = 8
ROOM_MIN_SIZE = 5
MAX_ROOMS = 15
MAX_DUNGEON_LEVEL = 26
INVENTORY_CAPACITY = 26

# Entity Generation Settings
MAX_MONSTERS_PER_ROOM = 3
MAX_ITEMS_PER_ROOM = 2
MAX_GOLD_PER_ROOM = 2
GOLD_MIN_AMOUNT = 10
GOLD_MAX_AMOUNT = 50

# Starting Equipment Settings
STARTING_WEAPON_POWER = 1
STARTING_WEAPON_BONUS = 1
STARTING_WEAPON_DICE = 8
STARTING_BOW_POWER = 1
STARTING_BOW_DICE = 2
STARTING_ARROWS = 25
STARTING_FOOD = 25

# Display Characters
CHARS = {
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

# Game Messages
MESSAGES = {
    'heal': "You begin to feel better.",
    'monster_death': "dies in a fit of agony",
    'player_hit': "hits you",
    'inventory_empty': "Your inventory is empty.",
    'cant_carry': "You can't carry anything else.",
    'nothing_here': "There is nothing here to pick up.",
    'level_up': "You feel stronger now!",
    'amulet_nearby': "You feel something special nearby...",
    'amulet_power': "The Amulet of Yendor glows with ancient power...",
    'welcome_level': "Welcome to level {} of the Dungeons of Doom!",
    'victory': "You escaped with the Amulet of Yendor!\nCongratulations! You won the game!",
    'death': "You have died..."
}

TITLE = "Roguelike Game"
AMULET_GENERATED = False

class EntityType(Enum):
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    GOLD = auto()
    STAIRS_DOWN = auto()
    STAIRS_UP = auto()
    AMULET = auto()
    WEAPON = auto()
    RANGED = auto()
    AMMO = auto()
    FOOD = auto()

class ItemEffect(Enum):
    HEAL = auto()
    LIGHTNING = auto()
    FIREBALL = auto()
    CONFUSION = auto()
    TELEPORT = auto()
    IDENTIFY = auto()

class Entity:
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        name: str,
        entity_type: EntityType,
        blocks: bool = True,
        gold_amount: int = 0,
        inventory: Optional[List["Entity"]] = None,
        hp: int = 30,
        max_hp: int = 30,
        effect: Optional[ItemEffect] = None,
        effect_amount: int = 0,
        confused_turns: int = 0,
        power: int = 0,
        sight_radius: int = 8,
        xp: int = 0,
        xp_given: int = 0,
        level: int = 1,
        dungeon_level: int = 1
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.entity_type = entity_type
        self.blocks = blocks
        self.gold_amount = gold_amount
        self.inventory = inventory if inventory is not None else []
        self.hp = hp
        self.max_hp = max_hp
        self.effect = effect
        self.effect_amount = effect_amount
        self.confused_turns = confused_turns
        self.power = power
        self.sight_radius = sight_radius
        self.xp = xp
        self.xp_given = xp_given
        self.level = level
        self.dungeon_level = dungeon_level

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.max_hp)
        print(MESSAGES['heal'])

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
        if self.hp <= 0:
            if self.entity_type == EntityType.MONSTER:
                print(f"The {self.name} {MESSAGES['monster_death']}.")
            else:
                print(f"The {self.name} {MESSAGES['player_hit']}.")

    def drop_item(self, item: "Entity", entities: List["Entity"]) -> None:
        if item in self.inventory:
            self.inventory.remove(item)
            item.x = self.x
            item.y = self.y
            entities.append(item)
            print(f"You drop {item.name}.")

    def use_item(self, item: "Entity", entities: List["Entity"], game_map: "GameMap") -> None:
        if item not in self.inventory:
            return

        used = False
        if item.effect == ItemEffect.HEAL:
            used = self._use_healing_item(item)
        elif item.effect == ItemEffect.LIGHTNING:
            used = self._use_lightning_scroll(item, entities)
        elif item.effect == ItemEffect.FIREBALL:
            used = self._use_fireball_scroll(item, entities)
        elif item.effect == ItemEffect.CONFUSION:
            used = self._use_confusion_scroll(item, entities)
        elif item.effect == ItemEffect.TELEPORT:
            used = self._use_teleport_scroll(game_map)
        elif item.effect == ItemEffect.IDENTIFY:
            print("This is a scroll of identify.")
            used = True

        if used:
            self.inventory.remove(item)

    def _use_healing_item(self, item: "Entity") -> bool:
        if self.hp < self.max_hp:
            self.heal(item.effect_amount)
            return True
        print("Nothing happens.")
        return False

    def _use_lightning_scroll(self, item: "Entity", entities: List["Entity"]) -> bool:
        target = self._find_closest_monster(entities, 5)
        if target:
            target.take_damage(item.effect_amount)
            print(f"Lightning strikes the {target.name} with a mighty crack!")
            return True
        print("The scroll disintegrates.")
        return False

    def _use_fireball_scroll(self, item: "Entity", entities: List["Entity"]) -> bool:
        affected_monsters = self._find_monsters_in_radius(entities, 3)
        if affected_monsters:
            for monster in affected_monsters:
                monster.take_damage(item.effect_amount)
            print("The scroll erupts in a tower of flame!")
            return True
        print("The scroll turns to dust.")
        return False

    def _use_confusion_scroll(self, item: "Entity", entities: List["Entity"]) -> bool:
        target = self._find_closest_monster(entities, 3)
        if target:
            target.confused_turns = item.effect_amount
            print(f"The {target.name} appears confused!")
            return True
        print("The scroll vanishes.")
        return False

    def _use_teleport_scroll(self, game_map: "GameMap") -> bool:
        walkable_tiles = [
            (x, y)
            for x in range(1, game_map.width - 1)
            for y in range(1, game_map.height - 1)
            if game_map.tiles[x][y].walkable
        ]
        
        if walkable_tiles:
            self.x, self.y = random.choice(walkable_tiles)
            print("You feel yourself moving...")
            return True
        print("Nothing happens.")
        return False

    def _find_closest_monster(self, entities: List["Entity"], max_distance: int) -> Optional["Entity"]:
        closest_monster = None
        closest_distance = float('inf')
        
        for entity in entities:
            if entity.entity_type == EntityType.MONSTER:
                distance = abs(self.x - entity.x) + abs(self.y - entity.y)
                if distance < closest_distance and distance <= max_distance:
                    closest_monster = entity
                    closest_distance = distance
        
        return closest_monster

    def _find_monsters_in_radius(self, entities: List["Entity"], radius: int) -> List["Entity"]:
        return [
            entity for entity in entities
            if entity.entity_type == EntityType.MONSTER
            and abs(self.x - entity.x) + abs(self.y - entity.y) <= radius
        ]

    def move(self, dx: int, dy: int, game_map: "GameMap", entities: List["Entity"]) -> None:
        new_x = self.x + dx
        new_y = self.y + dy
        
        for entity in entities:
            if entity.x == new_x and entity.y == new_y:
                if entity.entity_type == EntityType.GOLD:
                    self._collect_gold(entity, entities)
                    break
                elif entity.entity_type == EntityType.MONSTER and self.entity_type == EntityType.PLAYER:
                    self.attack(entity, entities)
                    return
                elif entity.entity_type == EntityType.PLAYER and self.entity_type == EntityType.MONSTER:
                    self.attack(entity, entities)
                    return
        
        if self._is_valid_move(new_x, new_y, game_map, entities):
            self.x = new_x
            self.y = new_y

    def _is_valid_move(self, x: int, y: int, game_map: "GameMap", entities: List["Entity"]) -> bool:
        return (game_map.tiles[x][y].walkable and
                not any(entity.blocks and entity.x == x and entity.y == y
                       for entity in entities if entity is not self))

    def _collect_gold(self, gold: "Entity", entities: List["Entity"]) -> None:
        self.gold_amount += gold.gold_amount
        entities.remove(gold)
        print(f"You found {gold.gold_amount} pieces of gold.")

    def pick_up(self, entities: List["Entity"]) -> None:
        for entity in entities:
            if entity.x == self.x and entity.y == self.y:
                if entity.entity_type == EntityType.GOLD:
                    self._collect_gold(entity, entities)
                    break
                if entity.entity_type == EntityType.ITEM or entity.entity_type == EntityType.AMULET:
                    if len(self.inventory) < INVENTORY_CAPACITY:
                        self.inventory.append(entity)
                        entities.remove(entity)
                        print(f"You now have {entity.name}.")
                        if entity.entity_type == EntityType.AMULET:
                            print("You feel a strange power in your hands!")
                    else:
                        print(MESSAGES['cant_carry'])
                    break
        else:
            print(MESSAGES['nothing_here'])

    def take_turn(self, target: "Entity", game_map: "GameMap", entities: List["Entity"]) -> None:
        if self.confused_turns > 0:
            self._handle_confusion(game_map, entities)
            return

        distance = self._distance_to(target)
        if distance < self.sight_radius:
            if distance <= 1:
                self.attack(target, entities)
            else:
                self._move_towards(target.x, target.y, game_map, entities)

    def _handle_confusion(self, game_map: "GameMap", entities: List["Entity"]) -> None:
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        self.move(dx, dy, game_map, entities)
        self.confused_turns -= 1
        if self.confused_turns == 0:
            print(f"The {self.name} is no longer confused.")

    def _distance_to(self, other: "Entity") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def _move_towards(self, target_x: int, target_y: int, game_map: "GameMap", entities: List["Entity"]) -> None:
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        dx = int(round(dx / distance)) if distance > 0 else 0
        dy = int(round(dy / distance)) if distance > 0 else 0

        self.move(dx, dy, game_map, entities)

    def attack(self, target: "Entity", entities: List["Entity"]) -> None:
        if self.entity_type == EntityType.PLAYER:
            # プレイヤーの攻撃処理
            weapon = next((item for item in self.inventory 
                         if item.entity_type == EntityType.WEAPON), None)
            if weapon:
                # 武器ダメージ: 1d(effect_amount) + power
                damage = random.randint(1, weapon.effect_amount) + weapon.power
            else:
                # 素手ダメージ: 1d4
                damage = random.randint(1, 4)
        else:
            # モンスターの攻撃処理
            damage = random.randint(1, self.power)

        target.take_damage(damage)
        if self.entity_type == EntityType.PLAYER:
            print(f"You hit the {target.name} ({damage} damage).")
        else:
            print(f"The {self.name} hits you ({damage} damage).")
        
        if target.hp <= 0 and target.entity_type == EntityType.MONSTER:
            entities.remove(target)
            if self.entity_type == EntityType.PLAYER:
                self._add_xp(target.xp_given)

    def _add_xp(self, amount: int) -> None:
        self.xp += amount
        
        # レベルアップに必要な経験値を計算 (10 * 2^(N-1))
        xp_to_next_level = 10 * (2 ** (self.level - 1))
        
        while self.xp >= xp_to_next_level:
            self.xp -= xp_to_next_level
            self._level_up()
            xp_to_next_level = 10 * (2 ** (self.level - 1))

    def _level_up(self) -> None:
        self.level += 1
        # HPの増加: 1d8 + 1
        hp_increase = random.randint(1, 8) + 1
        self.max_hp += hp_increase
        self.hp = self.max_hp
        print(f"Welcome to level {self.level}!")
        print(f"You feel much stronger! (+{hp_increase} HP)")

class Tile:
    def __init__(self, walkable: bool, transparent: bool):
        self.walkable = walkable
        self.transparent = transparent

class Rectangle:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    @property
    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
    
    def intersects(self, other: "Rectangle") -> bool:
        return (
            self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1
        )

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
        number_of_monsters = random.randint(0, MAX_MONSTERS_PER_ROOM)
        monster_chances = {'orc': 80, 'troll': 20}

        for _ in range(number_of_monsters):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                if random.randint(1, 100) <= monster_chances['orc']:
                    monster = Entity(
                        x, y, CHARS['orc'], (63, 127, 63), 'Orc',
                        EntityType.MONSTER, hp=10, max_hp=10,
                        power=3, sight_radius=8, xp_given=5
                    )
                else:
                    monster = Entity(
                        x, y, CHARS['troll'], (0, 127, 0), 'Troll',
                        EntityType.MONSTER, hp=16, max_hp=16,
                        power=4, sight_radius=8, xp_given=10
                    )
                entities.append(monster)

    def _place_items(self, room: Rectangle, entities: List[Entity]) -> None:
        number_of_items = random.randint(0, MAX_ITEMS_PER_ROOM)
        item_chances = {
            'healing_potion': 35,
            'lightning_scroll': 20,
            'fireball_scroll': 15,
            'confusion_scroll': 15,
            'teleport_scroll': 15
        }

        for _ in range(number_of_items):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                item = self._create_item(x, y, item_chances)
                if item:
                    entities.append(item)

    def _create_item(self, x: int, y: int, item_chances: Dict[str, int]) -> Optional[Entity]:
        roll = random.randint(1, 100)
        total = 0

        for item_name, chance in item_chances.items():
            total += chance
            if roll <= total:
                if item_name == 'healing_potion':
                    return Entity(
                        x, y, CHARS['potion'], (127, 0, 0), 'Healing Potion',
                        EntityType.ITEM, blocks=False,
                        effect=ItemEffect.HEAL, effect_amount=4
                    )
                elif item_name == 'lightning_scroll':
                    return Entity(
                        x, y, CHARS['scroll'], (0, 127, 127), 'Lightning Scroll',
                        EntityType.ITEM, blocks=False,
                        effect=ItemEffect.LIGHTNING, effect_amount=5
                    )
                elif item_name == 'fireball_scroll':
                    return Entity(
                        x, y, CHARS['scroll'], (127, 127, 0), 'Fireball Scroll',
                        EntityType.ITEM, blocks=False,
                        effect=ItemEffect.FIREBALL, effect_amount=3
                    )
                elif item_name == 'confusion_scroll':
                    return Entity(
                        x, y, CHARS['scroll'], (127, 0, 127), 'Confusion Scroll',
                        EntityType.ITEM, blocks=False,
                        effect=ItemEffect.CONFUSION, effect_amount=4
                    )
                else:  # teleport_scroll
                    return Entity(
                        x, y, CHARS['scroll'], (0, 255, 255), 'Teleport Scroll',
                        EntityType.ITEM, blocks=False,
                        effect=ItemEffect.TELEPORT, effect_amount=0
                    )
        return None

    def _place_gold(self, room: Rectangle, entities: List[Entity]) -> None:
        number_of_gold = random.randint(0, MAX_GOLD_PER_ROOM)

        for _ in range(number_of_gold):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                gold_amount = random.randint(GOLD_MIN_AMOUNT, GOLD_MAX_AMOUNT)
                gold = Entity(
                    x, y, CHARS['gold'], (255, 215, 0), f'{gold_amount} Gold',
                    EntityType.GOLD, blocks=False, gold_amount=gold_amount
                )
                entities.append(gold)

    def make_map(self, player: Entity, entities: List[Entity]) -> None:
        global AMULET_GENERATED
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
        self._try_place_amulet(rooms, entities)
        self._place_stairs(rooms, entities)
        
        if any(item.entity_type == EntityType.AMULET for item in player.inventory):
            print(MESSAGES['amulet_power'])
        print(MESSAGES['welcome_level'].format(self.dungeon_level))

    def _try_place_amulet(self, rooms: List[Rectangle], entities: List[Entity]) -> None:
        global AMULET_GENERATED
        if not AMULET_GENERATED and 20 <= self.dungeon_level <= 25:
            if random.random() < 0.2:
                amulet_x, amulet_y = rooms[-1].center
                amulet = Entity(
                    amulet_x, amulet_y, CHARS['amulet'], (255, 255, 0),
                    'Amulet of Yendor', EntityType.AMULET, blocks=False
                )
                entities.append(amulet)
                AMULET_GENERATED = True
                print(MESSAGES['amulet_nearby'])

    def _place_stairs(self, rooms: List[Rectangle], entities: List[Entity]) -> None:
        if self.dungeon_level < MAX_DUNGEON_LEVEL:
            stairs_x, stairs_y = rooms[-1].center
            stairs_down = Entity(
                stairs_x, stairs_y, CHARS['stairs_down'], (255, 255, 255),
                'Stairs down', EntityType.STAIRS_DOWN, blocks=False
            )
            entities.append(stairs_down)

        if self.dungeon_level > 1:
            stairs_x, stairs_y = rooms[0].center
            stairs_up = Entity(
                stairs_x, stairs_y, CHARS['stairs_up'], (255, 255, 255),
                'Stairs up', EntityType.STAIRS_UP, blocks=False
            )
            entities.append(stairs_up)

class Game:
    def __init__(self):
        self.player = self._create_player()
        self.entities = [self.player]
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, dungeon_level=1)
        self.game_map.make_map(self.player, self.entities)

    def _create_player(self) -> Entity:
        player = Entity(
            0, 0, CHARS['player'], (255, 255, 255), 'Player',
            EntityType.PLAYER, gold_amount=0, hp=12, max_hp=12,
            power=1, level=1, xp=0, dungeon_level=1
        )
        self._equip_player(player)
        return player

    def _equip_player(self, player: Entity) -> None:
        equipment = self._create_starting_equipment()
        player.inventory.extend(equipment)
        
        for item in player.inventory:
            if item.entity_type == EntityType.WEAPON:
                player.power += item.power
                break

    def _create_starting_equipment(self) -> List[Entity]:
        return [
            Entity(0, 0, CHARS['weapon'], (192, 192, 192), 'Short Sword (+1)',
                  EntityType.WEAPON, blocks=False, 
                  power=STARTING_WEAPON_POWER + STARTING_WEAPON_BONUS,
                  effect_amount=STARTING_WEAPON_DICE),
            Entity(0, 0, CHARS['bow'], (139, 69, 19), 'Bow (+1)',
                  EntityType.RANGED, blocks=False,
                  power=STARTING_BOW_POWER,
                  effect_amount=STARTING_BOW_DICE),
            Entity(0, 0, CHARS['arrow'], (139, 69, 19), f'{STARTING_ARROWS} Arrows',
                  EntityType.AMMO, blocks=False, effect_amount=STARTING_ARROWS),
            Entity(0, 0, CHARS['food'], (139, 69, 19), 'Food Ration',
                  EntityType.FOOD, blocks=False, effect_amount=STARTING_FOOD),
            Entity(0, 0, CHARS['scroll'], (255, 255, 255), 'Scroll of Identify',
                  EntityType.ITEM, blocks=False, effect=ItemEffect.IDENTIFY)
        ]

    def run(self) -> None:
        with tcod.context.new_terminal(
            SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE, vsync=True,
        ) as context:
            console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
            
            running = True
            while running:
                self._render(console)
                context.present(console)
                
                for event in tcod.event.wait():
                    result = self._handle_input(event)
                    if result:
                        running = not self._process_result(result)

    def _render(self, console: tcod.console.Console) -> None:
        console.clear()
        self._render_map(console)
        self._render_entities(console)
        self._render_ui(console)

    def _render_map(self, console: tcod.console.Console) -> None:
        for x in range(self.game_map.width):
            for y in range(self.game_map.height):
                if self.game_map.tiles[x][y].walkable:
                    console.print(x=x, y=y, string=CHARS['floor'])
                else:
                    console.print(x=x, y=y, string=CHARS['wall'])

    def _render_entities(self, console: tcod.console.Console) -> None:
        # アイテム/階段/魔除けを描画
        for entity in [e for e in self.entities if e.entity_type in {
            EntityType.ITEM, EntityType.GOLD, EntityType.STAIRS_DOWN,
            EntityType.STAIRS_UP, EntityType.AMULET
        }]:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
        
        # モンスターを描画
        for entity in [e for e in self.entities if e.entity_type == EntityType.MONSTER]:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
        
        # プレイヤーを描画
        console.print(x=self.player.x, y=self.player.y,
                     string=self.player.char, fg=self.player.color)

    def _render_ui(self, console: tcod.console.Console) -> None:
        # ダンジョンレベル
        console.print(x=0, y=34, string=f"Level: {self.game_map.dungeon_level}")
        
        # HP
        console.print(x=15, y=34, string=f"HP: {self.player.hp}/{self.player.max_hp}")
        
        # 装備情報
        console.print(x=30, y=34, string=f"Power: {self.player.power}")
        
        # 所持金
        console.print(x=0, y=35, string=f"Gold: {self.player.gold_amount}")
        
        # 装備中のアイテム
        equipped_items = []
        for item in self.player.inventory:
            if item.entity_type in {EntityType.WEAPON, EntityType.RANGED}:
                equipped_items.append(f"{item.name} [E]")
        
        if equipped_items:
            console.print(x=15, y=35, string=f"Equipped: {', '.join(equipped_items)}")

    def _handle_input(self, event: tcod.event.Event) -> Optional[str]:
        if isinstance(event, tcod.event.Quit):
            return "quit"
            
        if isinstance(event, tcod.event.KeyDown):
            return self._handle_key(event)
        
        return None

    def _handle_key(self, event: tcod.event.KeyDown) -> Optional[str]:
        key_actions = {
            tcod.event.KeySym.ESCAPE: lambda: "quit",
            tcod.event.KeySym.g: lambda: self._handle_pickup(),
            tcod.event.KeySym.i: lambda: self._show_inventory(),
            tcod.event.KeySym.u: lambda: self._use_item(),
            tcod.event.KeySym.d: lambda: self._drop_item(),
        }

        if event.sym in key_actions:
            return key_actions[event.sym]()

        if self._is_movement_key(event):
            dx, dy = self._get_movement_delta(event)
            self._move_player(dx, dy)
            return "move"

        if self._is_stairs_key(event):
            return self._handle_stairs(event)

        return None

    def _is_movement_key(self, event: tcod.event.KeyDown) -> bool:
        return event.sym in {
            tcod.event.KeySym.UP, tcod.event.KeySym.DOWN,
            tcod.event.KeySym.LEFT, tcod.event.KeySym.RIGHT,
            tcod.event.KeySym.k, tcod.event.KeySym.j,
            tcod.event.KeySym.h, tcod.event.KeySym.l,
            tcod.event.KeySym.y, tcod.event.KeySym.u,
            tcod.event.KeySym.b, tcod.event.KeySym.n
        }

    def _get_movement_delta(self, event: tcod.event.KeyDown) -> Tuple[int, int]:
        movement_keys = {
            tcod.event.KeySym.UP: (0, -1),
            tcod.event.KeySym.DOWN: (0, 1),
            tcod.event.KeySym.LEFT: (-1, 0),
            tcod.event.KeySym.RIGHT: (1, 0),
            tcod.event.KeySym.k: (0, -1),
            tcod.event.KeySym.j: (0, 1),
            tcod.event.KeySym.h: (-1, 0),
            tcod.event.KeySym.l: (1, 0),
            tcod.event.KeySym.y: (-1, -1),
            tcod.event.KeySym.u: (1, -1),
            tcod.event.KeySym.b: (-1, 1),
            tcod.event.KeySym.n: (1, 1)
        }
        return movement_keys[event.sym]

    def _move_player(self, dx: int, dy: int) -> None:
        self.player.move(dx, dy, self.game_map, self.entities)
        self._process_monster_turns()

    def _process_monster_turns(self) -> None:
        for entity in self.entities:
            if entity.entity_type == EntityType.MONSTER and entity.hp > 0:
                entity.take_turn(self.player, self.game_map, self.entities)
        
        if self.player.hp <= 0:
            print(MESSAGES['death'])

    def _is_stairs_key(self, event: tcod.event.KeyDown) -> bool:
        return (event.sym == tcod.event.KeySym.PERIOD and
                event.mod & tcod.event.KMOD_SHIFT) or \
               (event.sym == tcod.event.KeySym.COMMA and
                event.mod & tcod.event.KMOD_SHIFT)

    def _handle_stairs(self, event: tcod.event.KeyDown) -> Optional[str]:
        for entity in self.entities:
            if entity.x == self.player.x and entity.y == self.player.y:
                if (event.sym == tcod.event.KeySym.PERIOD and
                    entity.entity_type == EntityType.STAIRS_DOWN):
                    return "next_level"
                elif (event.sym == tcod.event.KeySym.COMMA and
                      entity.entity_type == EntityType.STAIRS_UP):
                    if (self.game_map.dungeon_level == 1 and
                        any(item.entity_type == EntityType.AMULET
                            for item in self.player.inventory)):
                        print(MESSAGES['victory'])
                        return "quit"
                    return "previous_level"
        return None

    def _handle_pickup(self) -> str:
        self.player.pick_up(self.entities)
        return "pickup"

    def _show_inventory(self) -> None:
        if self.player.inventory:
            print("\nInventory:")
            for i, item in enumerate(self.player.inventory):
                equipped = ""
                if item.entity_type in {EntityType.WEAPON, EntityType.RANGED}:
                    equipped = " [E]"
                print(f"{chr(97 + i)}) {item.name}{equipped}")
        else:
            print(MESSAGES['inventory_empty'])

    def _use_item(self) -> Optional[str]:
        if not self.player.inventory:
            print(MESSAGES['inventory_empty'])
            return None

        print("\nUse which item?")
        self._show_inventory()
        print("\nESC to cancel")

        while True:
            event = tcod.event.wait()
            if isinstance(event, tcod.event.KeyDown):
                if event.sym == tcod.event.KeySym.ESCAPE:
                    return None
                
                index = ord(event.sym.name) - ord('a')
                if 0 <= index < len(self.player.inventory):
                    self.player.use_item(
                        self.player.inventory[index],
                        self.entities,
                        self.game_map
                    )
                    return "use"
        
        return None

    def _drop_item(self) -> Optional[str]:
        if not self.player.inventory:
            print(MESSAGES['inventory_empty'])
            return None

        print("\nDrop which item?")
        self._show_inventory()
        print("\nESC to cancel")

        while True:
            event = tcod.event.wait()
            if isinstance(event, tcod.event.KeyDown):
                if event.sym == tcod.event.KeySym.ESCAPE:
                    return None
                
                index = ord(event.sym.name) - ord('a')
                if 0 <= index < len(self.player.inventory):
                    self.player.drop_item(
                        self.player.inventory[index],
                        self.entities
                    )
                    return "drop"
        
        return None

    def _process_result(self, result: str) -> bool:
        if result == "quit":
            return True
        elif result == "next_level" and self.game_map.dungeon_level < MAX_DUNGEON_LEVEL:
            self._change_level(self.game_map.dungeon_level + 1)
        elif result == "previous_level" and self.game_map.dungeon_level > 1:
            self._change_level(self.game_map.dungeon_level - 1)
        return False

    def _change_level(self, new_level: int) -> None:
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, new_level)
        self.player.dungeon_level = new_level
        self.entities = [self.player]
        self.game_map.make_map(self.player, self.entities)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
