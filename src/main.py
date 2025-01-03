#!/usr/bin/env python3
import tcod
from typing import Optional, Set, Tuple, List, Dict, Callable
import random
from enum import Enum, auto

# ゲームの設定
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_DUNGEON_LEVEL = 26  # 最大階層数
AMULET_GENERATED = False  # イェンダーの魔除けが生成されたかどうか

# エンティティの生成設定
MAX_MONSTERS_PER_ROOM = 3
MAX_ITEMS_PER_ROOM = 2
MAX_GOLD_PER_ROOM = 2
GOLD_MIN_AMOUNT = 10
GOLD_MAX_AMOUNT = 50
INVENTORY_CAPACITY = 26

TITLE = "Roguelike Game"

class EntityType(Enum):
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    GOLD = auto()
    STAIRS_DOWN = auto()  # 下り階段
    STAIRS_UP = auto()    # 上り階段
    AMULET = auto()  # イェンダーの魔除け

class ItemEffect(Enum):
    HEAL = auto()
    LIGHTNING = auto()
    FIREBALL = auto()
    CONFUSION = auto()
    TELEPORT = auto()

class Entity:
    """プレイヤー、モンスター、アイテムなどの基本クラス"""
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
        power: int = 0,  # 攻撃力
        sight_radius: int = 8,  # 視界範囲
        xp: int = 0,  # 経験値
        xp_given: int = 0,  # 倒した時に得られる経験値
        level: int = 1,  # レベル
        dungeon_level: int = 1  # 現在の階層
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
        """HPを回復する"""
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"HPが{amount}回復しました。現在のHP: {self.hp}/{self.max_hp}")

    def take_damage(self, amount: int) -> None:
        """ダメージを受ける"""
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            if self.entity_type == EntityType.MONSTER:
                print(f"{self.name}を倒しました！")
            else:
                print(f"{amount}のダメージを受けました。現在のHP: {self.hp}/{self.max_hp}")

    def drop_item(self, item: "Entity", entities: List["Entity"]) -> None:
        """アイテムを足元にドロップする"""
        if item in self.inventory:
            self.inventory.remove(item)
            item.x = self.x
            item.y = self.y
            entities.append(item)
            print(f"{item.name}をドロップしました。")

    def use_item(self, item: "Entity", entities: List["Entity"], game_map: "GameMap") -> None:
        """アイテムを使用する"""
        if item not in self.inventory:
            return

        used = False

        if item.effect == ItemEffect.HEAL:
            if self.hp < self.max_hp:
                self.heal(item.effect_amount)
                used = True
            else:
                print("HPが満タンです！")
                return

        elif item.effect == ItemEffect.LIGHTNING:
            # 最も近いモンスターにダメージ
            closest_monster = None
            closest_distance = float('inf')
            for entity in entities:
                if entity.entity_type == EntityType.MONSTER:
                    distance = abs(self.x - entity.x) + abs(self.y - entity.y)
                    if distance < closest_distance:
                        closest_monster = entity
                        closest_distance = distance
            
            if closest_monster and closest_distance <= 5:  # 射程範囲を5マスに制限
                closest_monster.take_damage(item.effect_amount)
                used = True
            else:
                print("射程範囲内にモンスターがいません。")
                return

        elif item.effect == ItemEffect.FIREBALL:
            # 自分の周囲のモンスターにダメージ
            radius = 3
            affected_monsters = []
            for entity in entities:
                if entity.entity_type == EntityType.MONSTER:
                    distance = abs(self.x - entity.x) + abs(self.y - entity.y)
                    if distance <= radius:
                        affected_monsters.append(entity)
            
            if affected_monsters:
                for monster in affected_monsters:
                    monster.take_damage(item.effect_amount)
                used = True
                print(f"{item.name}を使用し、{len(affected_monsters)}体のモンスターに{item.effect_amount}のダメージを与えました！")
            else:
                print("範囲内にモンスターがいません。")
                return

        elif item.effect == ItemEffect.CONFUSION:
            # 最も近いモンスターを混乱させる
            closest_monster = None
            closest_distance = float('inf')
            for entity in entities:
                if entity.entity_type == EntityType.MONSTER:
                    distance = abs(self.x - entity.x) + abs(self.y - entity.y)
                    if distance < closest_distance:
                        closest_monster = entity
                        closest_distance = distance
            
            if closest_monster and closest_distance <= 3:  # 射程範囲を3マスに制限
                closest_monster.confused_turns = item.effect_amount
                used = True
                print(f"{closest_monster.name}を{item.effect_amount}ターンの間、混乱させました！")
            else:
                print("射程範囲内にモンスターがいません。")
                return

        elif item.effect == ItemEffect.TELEPORT:
            # ランダムな場所にテレポート
            for _ in range(100):  # 最大100回試行
                new_x = random.randint(1, game_map.width - 2)
                new_y = random.randint(1, game_map.height - 2)
                if (game_map.tiles[new_x][new_y].walkable and
                    not any(entity.blocks and entity.x == new_x and entity.y == new_y
                           for entity in entities)):
                    self.x = new_x
                    self.y = new_y
                    used = True
                    print(f"{item.name}を使用し、ランダムな場所にテレポートしました！")
                    break
            else:
                print("テレポートに失敗しました。")
                return

        if used:
            self.inventory.remove(item)

    def move(self, dx: int, dy: int, game_map: "GameMap", entities: List["Entity"]) -> None:
        """移動先が通行可能な場合のみ移動。モンスターがいれば攻撃。"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 移動先のエンティティを確認
        for entity in entities:
            if entity.x == new_x and entity.y == new_y:
                if entity.entity_type == EntityType.GOLD:
                    # ゴールドは自動で拾う
                    self.gold_amount += entity.gold_amount
                    entities.remove(entity)
                    print(f"{entity.gold_amount}ゴールドを拾いました。所持金: {self.gold_amount}")
                    break
                elif entity.entity_type == EntityType.MONSTER and self.entity_type == EntityType.PLAYER:
                    # プレイヤーがモンスターに移動しようとした場合は攻撃
                    self.attack(entity, entities)
                    return
                elif entity.entity_type == EntityType.PLAYER and self.entity_type == EntityType.MONSTER:
                    # モンスターがプレイヤーに移動しようとした場合は攻撃
                    self.attack(entity, entities)
                    return
        
        if (game_map.tiles[new_x][new_y].walkable and
            not any(entity.blocks and entity.x == new_x and entity.y == new_y
                   for entity in entities if entity is not self)):
            self.x += dx
            self.y += dy

    def get_item(self, entities: List["Entity"]) -> None:
        """足元のアイテムを拾う"""
        for entity in entities:
            if entity.x == self.x and entity.y == self.y:
                if entity.entity_type == EntityType.ITEM or entity.entity_type == EntityType.AMULET:
                    if len(self.inventory) < INVENTORY_CAPACITY:
                        self.inventory.append(entity)
                        entities.remove(entity)
                        print(f"{entity.name}を拾いました。")
                        if entity.entity_type == EntityType.AMULET:
                            print("You feel a powerful magic coursing through your body!")
                    else:
                        print("インベントリがいっぱいです！")
                    break
        else:
            print("ここにはアイテムがありません。")

    def distance_to(self, other: "Entity") -> float:
        """他のエンティティまでの距離を計算"""
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def move_towards(self, target_x: int, target_y: int, game_map: "GameMap", entities: List["Entity"]) -> None:
        """目標地点に向かって移動"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        dx = int(round(dx / distance)) if distance > 0 else 0
        dy = int(round(dy / distance)) if distance > 0 else 0

        self.move(dx, dy, game_map, entities)

    def move_randomly(self, game_map: "GameMap", entities: List["Entity"]) -> None:
        """ランダムな方向に移動"""
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        self.move(dx, dy, game_map, entities)

    def attack(self, target: "Entity", entities: List["Entity"]) -> None:
        """他のエンティティを攻撃"""
        damage = self.power
        target.take_damage(damage)
        print(f"{self.name}が{target.name}に{damage}のダメージを与えました！")
        
        if target.hp <= 0 and target.entity_type == EntityType.MONSTER:
            entities.remove(target)
            if self.entity_type == EntityType.PLAYER:
                self.add_xp(target.xp_given)  # 経験値を獲得

    def take_turn(self, target: "Entity", game_map: "GameMap", entities: List["Entity"]) -> None:
        """モンスターのターン処理"""
        if self.confused_turns > 0:
            # 混乱状態の場合、ランダムに移動
            self.move_randomly(game_map, entities)
            self.confused_turns -= 1
            if self.confused_turns == 0:
                print(f"{self.name}の混乱が解けました。")
            return

        distance = self.distance_to(target)
        
        if distance < self.sight_radius:
            if distance <= 1:
                # 隣接している場合は攻撃
                self.attack(target, entities)
            else:
                # プレイヤーが視界内なら追跡
                self.move_towards(target.x, target.y, game_map, entities)

    def level_up(self) -> None:
        """レベルアップ処理"""
        self.level += 1
        self.max_hp += 5
        self.hp = self.max_hp  # レベルアップ時にHP全回復
        self.power += 2
        print(f"レベルアップ！ Level {self.level}")
        print(f"最大HP +5 (現在: {self.max_hp})")
        print(f"攻撃力 +2 (現在: {self.power})")

    def add_xp(self, amount: int) -> None:
        """経験値を追加し、必要に応じてレベルアップ"""
        self.xp += amount
        print(f"{amount}の経験値を獲得！ (現在: {self.xp})")
        
        # レベルアップに必要な経験値を計算
        xp_to_next_level = self.level * 10
        
        while self.xp >= xp_to_next_level:
            self.xp -= xp_to_next_level
            self.level_up()
            xp_to_next_level = self.level * 10

class Tile:
    """マップタイル。通行可能かどうかを管理する。"""
    def __init__(self, walkable: bool, transparent: bool):
        self.walkable = walkable
        self.transparent = transparent

class Rectangle:
    """部屋を表す矩形"""
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y
    
    def intersects(self, other: "Rectangle") -> bool:
        """この部屋が他の部屋と重なっているかどうかを判定"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

class GameMap:
    def __init__(self, width: int, height: int, dungeon_level: int):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level
        self.tiles = self.initialize_tiles()
    
    def initialize_tiles(self) -> List[List[Tile]]:
        """マップを壁で初期化"""
        tiles = [[Tile(walkable=False, transparent=False)
                 for y in range(self.height)]
                for x in range(self.width)]
        return tiles
    
    def in_bounds(self, x: int, y: int) -> bool:
        """指定された座標がマップの範囲内かどうかを判定"""
        return 0 <= x < self.width and 0 <= y < self.height

    def create_room(self, room: Rectangle) -> None:
        """部屋を作成"""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].walkable = True
                self.tiles[x][y].transparent = True
    
    def create_h_tunnel(self, x1: int, x2: int, y: int) -> None:
        """水平方向の通路を作成"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True
    
    def create_v_tunnel(self, y1: int, y2: int, x: int) -> None:
        """垂直方向の通路を作成"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True

    def place_entities(self, room: Rectangle, entities: List[Entity]) -> None:
        """部屋にモンスター、アイテム、ゴールドを配置"""
        number_of_monsters = random.randint(0, MAX_MONSTERS_PER_ROOM)
        number_of_items = random.randint(0, MAX_ITEMS_PER_ROOM)
        number_of_gold = random.randint(0, MAX_GOLD_PER_ROOM)

        monster_chances: Dict[str, int] = {
            'orc': 80,
            'troll': 20
        }
        item_chances: Dict[str, int] = {
            'healing_potion': 35,
            'lightning_scroll': 20,
            'fireball_scroll': 15,
            'confusion_scroll': 15,
            'teleport_scroll': 15
        }

        # モンスターの配置
        for _ in range(number_of_monsters):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                if random.randint(1, 100) <= monster_chances['orc']:
                    monster = Entity(
                        x, y, 'o', (63, 127, 63), 'Orc',
                        EntityType.MONSTER, hp=10, max_hp=10,
                        power=3, sight_radius=8, xp_given=5
                    )
                else:
                    monster = Entity(
                        x, y, 'T', (0, 127, 0), 'Troll',
                        EntityType.MONSTER, hp=16, max_hp=16,
                        power=4, sight_radius=8, xp_given=10
                    )
                entities.append(monster)

        # アイテムの配置
        for _ in range(number_of_items):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                roll = random.randint(1, 100)
                total = 0

                for item_name, chance in item_chances.items():
                    total += chance
                    if roll <= total:
                        if item_name == 'healing_potion':
                            item = Entity(
                                x, y, '!', (127, 0, 0), 'Healing Potion',
                                EntityType.ITEM, blocks=False,
                                effect=ItemEffect.HEAL, effect_amount=4
                            )
                        elif item_name == 'lightning_scroll':
                            item = Entity(
                                x, y, '?', (0, 127, 127), 'Lightning Scroll',
                                EntityType.ITEM, blocks=False,
                                effect=ItemEffect.LIGHTNING, effect_amount=5
                            )
                        elif item_name == 'fireball_scroll':
                            item = Entity(
                                x, y, '?', (127, 127, 0), 'Fireball Scroll',
                                EntityType.ITEM, blocks=False,
                                effect=ItemEffect.FIREBALL, effect_amount=3
                            )
                        elif item_name == 'confusion_scroll':
                            item = Entity(
                                x, y, '?', (127, 0, 127), 'Confusion Scroll',
                                EntityType.ITEM, blocks=False,
                                effect=ItemEffect.CONFUSION, effect_amount=4
                            )
                        else:  # teleport_scroll
                            item = Entity(
                                x, y, '?', (0, 255, 255), 'Teleport Scroll',
                                EntityType.ITEM, blocks=False,
                                effect=ItemEffect.TELEPORT, effect_amount=0
                            )
                        entities.append(item)
                        break

        # ゴールドの配置
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
        """ダンジョンを生成し、エンティティを配置"""
        global AMULET_GENERATED
        rooms: List[Rectangle] = []

        for r in range(MAX_ROOMS):
            # ランダムな部屋のサイズと位置を決定
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)
            
            new_room = Rectangle(x, y, w, h)
            
            # 他の部屋と重なっていないか確認
            for other_room in rooms:
                if new_room.intersects(other_room):
                    break
            else:  # 重なっていない場合
                # 部屋を作成
                self.create_room(new_room)
                
                # 部屋の中心座標を取得
                new_x, new_y = new_room.center
                
                if len(rooms) == 0:
                    # 最初の部屋の場合、プレイヤーの開始位置とする
                    player.x = new_x
                    player.y = new_y
                else:
                    # 前の部屋と通路でつなぐ
                    prev_x, prev_y = rooms[-1].center
                    
                    # 50%の確率で水平→垂直か垂直→水平を選択
                    if random.random() < 0.5:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                
                # エンティティを配置
                self.place_entities(new_room, entities)
                
                rooms.append(new_room)

        # イェンダーの魔除けを20-25階のランダムな階層に配置（まだ生成されていない場合）
        if not AMULET_GENERATED and 20 <= self.dungeon_level <= 25:
            # 20%の確率で生成
            if random.random() < 0.2:
                amulet_x, amulet_y = rooms[-1].center
                amulet = Entity(
                    amulet_x, amulet_y, '"', (255, 255, 0), 'Amulet of Yendor',
                    EntityType.AMULET, blocks=False
                )
                entities.append(amulet)
                AMULET_GENERATED = True
                print("You feel a powerful magical artifact nearby...")

        # 最下層以外は下り階段を配置
        if self.dungeon_level < MAX_DUNGEON_LEVEL:
            stairs_x, stairs_y = rooms[-1].center
            stairs_down = Entity(
                stairs_x, stairs_y, '>', (255, 255, 255), 'Stairs down',
                EntityType.STAIRS_DOWN, blocks=False
            )
            entities.append(stairs_down)

        # 1階以外は上り階段を配置
        if self.dungeon_level > 1:
            stairs_x, stairs_y = rooms[0].center
            stairs_up = Entity(
                stairs_x, stairs_y, '<', (255, 255, 255), 'Stairs up',
                EntityType.STAIRS_UP, blocks=False
            )
            entities.append(stairs_up)

def handle_input(event: tcod.event.Event, player: Entity, game_map: GameMap, entities: List[Entity]) -> Optional[bool]:
    """キー入力を処理する。Trueを返すとゲームを終了する。"""
    if isinstance(event, tcod.event.Quit):
        return True
        
    if isinstance(event, tcod.event.KeyDown):
        action_taken = False
        
        # 移動キーの設定
        if event.sym in {
            # 矢印キー
            tcod.event.KeySym.UP: (0, -1),
            tcod.event.KeySym.DOWN: (0, 1),
            tcod.event.KeySym.LEFT: (-1, 0),
            tcod.event.KeySym.RIGHT: (1, 0),
            # viキーバインド
            tcod.event.KeySym.k: (0, -1),  # 上
            tcod.event.KeySym.j: (0, 1),   # 下
            tcod.event.KeySym.h: (-1, 0),  # 左
            tcod.event.KeySym.l: (1, 0),   # 右
            # 斜め移動
            tcod.event.KeySym.y: (-1, -1), # 左上
            tcod.event.KeySym.u: (1, -1),  # 右上
            tcod.event.KeySym.b: (-1, 1),  # 左下
            tcod.event.KeySym.n: (1, 1),   # 右下
        }.keys():
            dx, dy = {
                # 矢印キー
                tcod.event.KeySym.UP: (0, -1),
                tcod.event.KeySym.DOWN: (0, 1),
                tcod.event.KeySym.LEFT: (-1, 0),
                tcod.event.KeySym.RIGHT: (1, 0),
                # viキーバインド
                tcod.event.KeySym.k: (0, -1),  # 上
                tcod.event.KeySym.j: (0, 1),   # 下
                tcod.event.KeySym.h: (-1, 0),  # 左
                tcod.event.KeySym.l: (1, 0),   # 右
                # 斜め移動
                tcod.event.KeySym.y: (-1, -1), # 左上
                tcod.event.KeySym.u: (1, -1),  # 右上
                tcod.event.KeySym.b: (-1, 1),  # 左下
                tcod.event.KeySym.n: (1, 1),   # 右下
            }[event.sym]
            player.move(dx, dy, game_map, entities)
            action_taken = True
        elif event.sym == tcod.event.KeySym.g:  # アイテムを拾う
            player.get_item(entities)
            action_taken = True
        elif event.sym == tcod.event.KeySym.i:  # インベントリを表示
            if player.inventory:
                print("\nインベントリ:")
                for i, item in enumerate(player.inventory):
                    print(f"{chr(97 + i)}) {item.name}")
            else:
                print("\nインベントリは空です。")
        elif event.sym == tcod.event.KeySym.u:  # アイテムを使用
            if player.inventory:
                print("\nどのアイテムを使用しますか？")
                for i, item in enumerate(player.inventory):
                    print(f"{chr(97 + i)}) {item.name}")
                print("\nESCでキャンセル")
                while True:
                    next_event = tcod.event.wait()
                    if isinstance(next_event, tcod.event.KeyDown):
                        if next_event.sym == tcod.event.KeySym.ESCAPE:
                            break
                        index = ord(next_event.sym.name) - ord('a')
                        if 0 <= index < len(player.inventory):
                            player.use_item(player.inventory[index], entities, game_map)
                            action_taken = True
                            break
            else:
                print("\nインベントリは空です。")
        elif event.sym == tcod.event.KeySym.d:  # アイテムをドロップ
            if player.inventory:
                print("\nどのアイテムをドロップしますか？")
                for i, item in enumerate(player.inventory):
                    print(f"{chr(97 + i)}) {item.name}")
                print("\nESCでキャンセル")
                while True:
                    next_event = tcod.event.wait()
                    if isinstance(next_event, tcod.event.KeyDown):
                        if next_event.sym == tcod.event.KeySym.ESCAPE:
                            break
                        index = ord(next_event.sym.name) - ord('a')
                        if 0 <= index < len(player.inventory):
                            player.drop_item(player.inventory[index], entities)
                            action_taken = True
                            break
            else:
                print("\nインベントリは空です。")
        elif event.sym == tcod.event.KeySym.PERIOD and (
            event.mod & tcod.event.KMOD_SHIFT
        ):  # > (下り階段)
            for entity in entities:
                if (entity.x == player.x and entity.y == player.y and
                    entity.entity_type == EntityType.STAIRS_DOWN):
                    return "next_level"
        
        elif event.sym == tcod.event.KeySym.COMMA and (
            event.mod & tcod.event.KMOD_SHIFT
        ):  # < (上り階段)
            for entity in entities:
                if (entity.x == player.x and entity.y == player.y and
                    entity.entity_type == EntityType.STAIRS_UP):
                    # 1階で上り階段を使用し、イェンダーの魔除けを持っている場合は勝利
                    if game_map.dungeon_level == 1 and any(
                        item.entity_type == EntityType.AMULET for item in player.inventory
                    ):
                        print("You escaped with the Amulet of Yendor!")
                        print("Congratulations! You won the game!")
                        return True
                    return "previous_level"
        
        elif event.sym == tcod.event.KeySym.ESCAPE:
            return True

        # プレイヤーがアクションを実行した場合、モンスターのターンを処理
        if action_taken:
            for entity in entities:
                if entity.entity_type == EntityType.MONSTER and entity.hp > 0:
                    entity.take_turn(player, game_map, entities)
            
            # プレイヤーの死亡判定
            if player.hp <= 0:
                print("あなたは死亡しました...")
                return True
    
    return None

def main():
    # フォントの設定
    tileset = tcod.tileset.load_tilesheet(
        "assets/fonts/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # エンティティリストの作成（プレイヤーを含む）
    player = Entity(0, 0, '@', (255, 255, 255), 'Player', EntityType.PLAYER,
                   gold_amount=0, hp=30, max_hp=30, power=5,
                   level=1, xp=0, dungeon_level=1)
    entities = [player]

    # マップを生成
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, dungeon_level=1)
    game_map.make_map(player, entities)

    # コンソールの初期化
    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title=TITLE,
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        
        running = True
        while running:
            root_console.clear()
            
            # マップの描画
            for x in range(game_map.width):
                for y in range(game_map.height):
                    if game_map.tiles[x][y].walkable:
                        root_console.print(x=x, y=y, string=".")
                    else:
                        root_console.print(x=x, y=y, string="#")
            
            # エンティティの描画（アイテム/階段/魔除け → モンスター → プレイヤーの順）
            for entity in [e for e in entities if e.entity_type in {EntityType.ITEM, EntityType.GOLD, EntityType.STAIRS_DOWN, EntityType.STAIRS_UP, EntityType.AMULET}]:
                root_console.print(
                    x=entity.x,
                    y=entity.y,
                    string=entity.char,
                    fg=entity.color
                )
            
            for entity in [e for e in entities if e.entity_type == EntityType.MONSTER]:
                root_console.print(
                    x=entity.x,
                    y=entity.y,
                    string=entity.char,
                    fg=entity.color
                )
            
            # プレイヤーは最後に描画
            for entity in [e for e in entities if e.entity_type == EntityType.PLAYER]:
                root_console.print(
                    x=entity.x,
                    y=entity.y,
                    string=entity.char,
                    fg=entity.color
                )

            # 階層情報を表示
            root_console.print(x=0, y=47, string=f"Level: {game_map.dungeon_level}")
            
            # 画面の更新
            context.present(root_console)
            
            # イベント処理
            for event in tcod.event.wait():
                result = handle_input(event, player, game_map, entities)
                if result == "next_level" and game_map.dungeon_level < MAX_DUNGEON_LEVEL:
                    # 次の階層へ
                    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, game_map.dungeon_level + 1)
                    player.dungeon_level += 1
                    entities = [player]
                    game_map.make_map(player, entities)
                    if any(item.entity_type == EntityType.AMULET for item in player.inventory):
                        print("The Amulet of Yendor pulses with mysterious energy...")
                    print(f"You descend to level {game_map.dungeon_level}")
                elif result == "previous_level" and game_map.dungeon_level > 1:
                    # 前の階層へ
                    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, game_map.dungeon_level - 1)
                    player.dungeon_level -= 1
                    entities = [player]
                    game_map.make_map(player, entities)
                    if any(item.entity_type == EntityType.AMULET for item in player.inventory):
                        print("The Amulet of Yendor pulses with mysterious energy...")
                    print(f"You ascend to level {game_map.dungeon_level}")
                elif result is True:
                    running = False
                    break

if __name__ == "__main__":
    main()
