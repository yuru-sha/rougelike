#!/usr/bin/env python3
from enum import Enum, auto
from typing import Optional, List, Tuple, Dict, Any, TYPE_CHECKING
import random
from config.messages import MESSAGES
from utils.logger import setup_logger

if TYPE_CHECKING:
    from map.game_map import GameMap


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
    ARMOR = auto()
    SHIELD = auto()
    RING = auto()


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
        inventory: Optional[List["Entity"]] = None,
        hp: Optional[int] = None,
        max_hp: Optional[int] = None,
        power: Optional[Tuple[int, int]] = None,
        sight_radius: Optional[int] = None,
        damage_dice: Optional[Tuple[int, int]] = None,
        hit_bonus: Optional[int] = None,
        two_handed: bool = False,
        ranged: bool = False,
        ammo_type: Optional[str] = None,
        ammo_count: Optional[int] = None,
        nutrition: Optional[int] = None,
        food_count: Optional[int] = None,
        level: int = 1,
        xp: int = 0,
        xp_given: int = 0,
        dungeon_level: int = 1,
        strength: int = 0,
        sustain: bool = False,
        search: int = 0,
        gold_amount: int = 0,
        effect: Optional[str] = None,
        effect_amount: int = 0,
        confused_turns: int = 0,
        speed: float = 1.0,
        special: Optional[str] = None,
        regeneration: bool = False,
        defense: int = 0,
        weight: int = 0,
        gold: int = 0,
        stack_size: Optional[int] = None,  # 最大スタックサイズ
        count: Optional[int] = None,  # 現在のスタック数
    ):
        self.logger = setup_logger("entity")
        self.logger.debug(f"Creating entity: {name} ({entity_type})")

        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.entity_type = entity_type
        self.blocks = blocks
        self.inventory = inventory or []
        self.hp = hp
        self.max_hp = max_hp
        self.power = power
        self.sight_radius = sight_radius
        self.damage_dice = damage_dice
        self.hit_bonus = hit_bonus
        self.two_handed = two_handed
        self.ranged = ranged
        self.ammo_type = ammo_type
        self.ammo_count = ammo_count
        self.nutrition = nutrition
        self.food_count = food_count
        self.level = level
        self.xp = xp
        self.xp_given = xp_given
        self.dungeon_level = dungeon_level
        self.strength = strength
        self.sustain = sustain
        self.search = search
        self.gold_amount = gold_amount
        self.effect = effect
        self.effect_amount = effect_amount
        self.confused_turns = confused_turns
        self.speed = speed
        self.special = special
        self.regeneration = regeneration
        self.defense = defense
        self.weight = weight
        self.move_count = 0.0
        self.gold = gold
        self.stack_size = stack_size  # 最大スタックサイズを追加
        self.count = count or 1  # 現在のスタック数を追加

    @property
    def display_name(self) -> str:
        """アイテム名を表示用にフォーマット"""
        if self.stack_size and self.count > 1:
            return f"{self.name} ({self.count})"
        return self.name

    def can_stack_with(self, other: "Entity") -> bool:
        """別のアイテムとスタック可能かチェック"""
        if not self.stack_size or not other.stack_size:
            return False

        return (
            self.entity_type == other.entity_type
            and self.name == other.name
            and self.effect == other.effect
            and self.effect_amount == other.effect_amount
            and self.ammo_type == other.ammo_type
            and self.damage_dice == other.damage_dice
        )

    def stack_with(self, other: "Entity") -> bool:
        """別のアイテムとスタックを試みる"""
        if not self.can_stack_with(other):
            return False

        total_count = self.count + other.count
        if self.stack_size and total_count <= self.stack_size:
            self.count = total_count
            return True
        return False

    def split_stack(self, amount: int) -> Optional["Entity"]:
        """スタックを分割する"""
        if not self.stack_size or amount >= self.count or amount < 1:
            return None

        # 新しいエンティティを作成
        new_entity = Entity(
            self.x,
            self.y,
            self.char,
            self.color,
            self.name,
            self.entity_type,
            blocks=self.blocks,
            effect=self.effect,
            effect_amount=self.effect_amount,
            ammo_type=self.ammo_type,
            damage_dice=self.damage_dice,
            stack_size=self.stack_size,
            count=amount,
        )

        self.count -= amount
        return new_entity

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, amount: int) -> None:
        if self.hp is None:  # HPを持たないエンティティはダメージを受けない
            return

        # 防具による軽減
        for item in self.inventory:
            if item.entity_type == EntityType.ARMOR:
                amount = max(0, amount - (item.defense or 0))
            elif item.entity_type == EntityType.RING and item.defense:
                amount = max(0, amount - item.defense)

        self.hp = max(0, self.hp - amount)  # HPが0未満にならないようにする

        # HPが0になった場合の処理
        if self.hp <= 0:
            if self.entity_type == EntityType.PLAYER:
                from engine.game import Game
                Game.instance.add_message(MESSAGES["death"])
            elif self.entity_type == EntityType.MONSTER:
                from engine.game import Game
                Game.instance.add_message(f"{self.name} {MESSAGES['monster_death']}")

    def drop_item(self, item: "Entity", entities: List["Entity"]) -> None:
        self.inventory.remove(item)
        item.x = self.x
        item.y = self.y
        entities.append(item)

    def use_item(
        self, item: "Entity", entities: List["Entity"], game_map: "GameMap"
    ) -> None:
        if item.effect == "heal":
            if self._use_healing_item(item):
                self.inventory.remove(item)
        elif item.effect == "lightning":
            if self._use_lightning_scroll(item, entities):
                self.inventory.remove(item)
        elif item.effect == "fireball":
            if self._use_fireball_scroll(item, entities):
                self.inventory.remove(item)
        elif item.effect == "confusion":
            if self._use_confusion_scroll(item, entities):
                self.inventory.remove(item)
        elif item.effect == "teleport":
            if self._use_teleport_scroll(game_map):
                self.inventory.remove(item)

    def _use_healing_item(self, item: "Entity") -> bool:
        if self.hp == self.max_hp:
            return False
        self.heal(item.effect_amount)
        return True

    def _use_lightning_scroll(self, item: "Entity", entities: List["Entity"]) -> bool:
        monster = self._find_closest_monster(entities, item.effect_amount)
        if monster is None:
            return False
        monster.take_damage(20)
        return True

    def _use_fireball_scroll(self, item: "Entity", entities: List["Entity"]) -> bool:
        monsters = self._find_monsters_in_radius(entities, item.effect_amount)
        if not monsters:
            return False
        for monster in monsters:
            monster.take_damage(12)
        return True

    def _use_confusion_scroll(self, item: "Entity", entities: List["Entity"]) -> bool:
        monster = self._find_closest_monster(entities, 5)
        if monster is None:
            return False
        monster.confused_turns = item.effect_amount
        return True

    def _use_teleport_scroll(self, game_map: "GameMap") -> bool:
        while True:
            x = random.randint(0, game_map.width - 1)
            y = random.randint(0, game_map.height - 1)
            if game_map.tiles[x][y].walkable:
                self.x = x
                self.y = y
                return True
        return False

    def _find_closest_monster(
        self, entities: List["Entity"], max_distance: int
    ) -> Optional["Entity"]:
        closest_monster = None
        closest_distance = max_distance + 1

        for entity in entities:
            if (
                entity.entity_type == EntityType.MONSTER
                and self._distance_to(entity) < closest_distance
            ):
                closest_monster = entity
                closest_distance = self._distance_to(entity)

        return closest_monster

    def _find_monsters_in_radius(
        self, entities: List["Entity"], radius: int
    ) -> List["Entity"]:
        return [
            entity
            for entity in entities
            if entity.entity_type == EntityType.MONSTER
            and self._distance_to(entity) <= radius
        ]

    def move(
        self, dx: int, dy: int, game_map: "GameMap", entities: List["Entity"]
    ) -> None:
        new_x = self.x + dx
        new_y = self.y + dy

        if self._is_valid_move(new_x, new_y, game_map, entities):
            self.x = new_x
            self.y = new_y

            # ゴールドの自動拾い
            for entity in list(entities):  # リストのコピーを作成して反復
                if (
                    entity.entity_type == EntityType.GOLD
                    and entity.x == self.x
                    and entity.y == self.y
                ):
                    self._collect_gold(entity, entities)
                    break

    def _is_valid_move(
        self, x: int, y: int, game_map: "GameMap", entities: List["Entity"]
    ) -> bool:
        return (
            game_map.in_bounds(x, y)
            and game_map.tiles[x][y].walkable
            and not any(
                entity.blocks and entity.x == x and entity.y == y for entity in entities
            )
        )

    def _collect_gold(self, gold: "Entity", entities: List["Entity"]) -> None:
        self.gold += gold.gold_amount  # goldプロパティに加算
        entities.remove(gold)

    def pick_up(self, entities: List["Entity"]) -> None:
        for entity in list(entities):  # エンティティのリストのコピーを作成
            if entity.x == self.x and entity.y == self.y:
                if entity.entity_type == EntityType.GOLD:
                    self._collect_gold(entity, entities)
                    break
                elif entity.entity_type not in [EntityType.PLAYER, EntityType.MONSTER]:
                    if len(self.inventory) >= 26:  # インベントリ容量
                        return

                    # スタック可能なアイテムを探す
                    stacked = False
                    if entity.stack_size:
                        for inv_item in self.inventory:
                            if inv_item.can_stack_with(entity):
                                if inv_item.stack_with(entity):
                                    entities.remove(entity)
                                    stacked = True
                                    break

                    # スタックできなかった場合は新しいアイテムとして追加
                    if not stacked:
                        self.inventory.append(entity)
                        entities.remove(entity)
                    break

    def take_turn(
        self, target: "Entity", game_map: "GameMap", entities: List["Entity"]
    ) -> None:
        # 移動カウンターを更新
        self.move_count += self.speed
        if self.move_count < 1.0:
            return

        # 混乱状態の処理
        if self.confused_turns > 0:
            self._handle_confusion(game_map, entities)
            self.confused_turns -= 1
            self.move_count -= 1.0
            return

        # ターゲットまでの距離を計算
        distance = self._distance_to(target)

        # 視界内にいるかチェック
        if distance <= self.sight_radius:
            if distance <= 1:
                self.attack(target, entities)
            else:
                self._move_towards(target.x, target.y, game_map, entities)

        # 移動カウンターをリセット
        self.move_count -= 1.0

        # 再生能力の処理
        if self.regeneration and self.hp < self.max_hp:
            self.heal(1)

    def _handle_confusion(self, game_map: "GameMap", entities: List["Entity"]) -> None:
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx, dy, game_map, entities)

    def _distance_to(self, other: "Entity") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx**2 + dy**2) ** 0.5

    def _add_xp(self, amount: int) -> None:
        """
        経験値を追加し、レベルアップの条件を満たしているかチェックする
        オリジナルRogueの経験値テーブルに準拠：
        Lv1:    0 XP (初期値)
        Lv2:   10 XP
        Lv3:   20 XP
        Lv4:   40 XP
        Lv5:   80 XP
        Lv6:  160 XP
        Lv7:  320 XP
        Lv8:  640 XP
        Lv9: 1280 XP
        以降、同様に倍増
        """
        self.xp += amount
        xp_needed = 10  # Lv2に必要な経験値

        # 現在のレベルまでに必要な経験値を計算
        for level in range(2, self.level + 1):
            xp_needed *= 2

        # レベルアップチェック
        while self.xp >= xp_needed:
            self.level += 1
            self._level_up()
            xp_needed *= 2

    def _level_up(self) -> None:
        """
        レベルアップ時の処理（オリジナルRogueに準拠）
        - HPは(4,8)の範囲でランダムに増加
        - 筋力は18までは50%の確率で1上昇
        - 筋力は19以上は10%の確率で1上昇（最大25まで）
        """
        from engine.game import Game  # 循環参照を避けるためにローカルインポート
        import random

        # レベルアップメッセージ
        Game.instance.add_message(MESSAGES["level_up"].format(self.level))

        # HP増加 (4-8)
        hp_increase = random.randint(4, 8)
        self.max_hp += hp_increase
        self.hp = self.max_hp  # HPを全回復

        # 筋力増加
        old_strength = self.strength
        if self.strength < 18 and random.random() < 0.5:
            self.strength += 1
        elif 18 <= self.strength < 25 and random.random() < 0.1:
            self.strength += 1

        # 筋力が上がった場合はメッセージを表示
        if self.strength > old_strength:
            Game.instance.add_message(MESSAGES["strength_up"].format(self.strength))

        # 基本攻撃力の増加（レベルに応じて）
        if isinstance(self.power, tuple):
            min_damage, max_damage = self.power
            # レベル3,5,7,9ごとに最小ダメージ+1
            if self.level % 2 == 1 and self.level > 1:
                min_damage += 1
            # レベル2,4,6,8ごとに最大ダメージ+1
            if self.level % 2 == 0:
                max_damage += 1
            self.power = (min_damage, max_damage)

    def _move_towards(
        self,
        target_x: int,
        target_y: int,
        game_map: "GameMap",
        entities: List["Entity"],
    ) -> None:
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.move(dx, dy, game_map, entities)

    def attack(self, target: "Entity", entities: List["Entity"]) -> None:
        from engine.game import Game  # 循環参照を避けるためにローカルインポート

        # 武器のダメージを計算
        damage = 1  # 素手の場合のデフォルトダメージ
        hit_bonus = 0

        # 装備中の武器を探す
        weapon = next(
            (item for item in self.inventory if item.entity_type == EntityType.WEAPON),
            None,
        )

        if weapon and weapon.damage_dice:
            dice_count, dice_sides = weapon.damage_dice
            damage = sum(random.randint(1, dice_sides) for _ in range(dice_count))
            hit_bonus = weapon.hit_bonus

        # 特殊能力の処理
        if self.special == "rust" and target.inventory:
            # 武器や防具を錆びさせる
            for item in target.inventory:
                if item.entity_type in [EntityType.WEAPON, EntityType.ARMOR]:
                    if item.hit_bonus > 0:
                        item.hit_bonus -= 1
                    if item.defense > 0:
                        item.defense -= 1
        elif self.special == "fire":
            # 追加の火炎ダメージ
            damage += random.randint(3, 6)

        # 攻撃の実行
        if self.entity_type == EntityType.MONSTER:
            # モンスターの攻撃メッセージ
            Game.instance.add_message(MESSAGES["monster_attack"].format(self.name))
            Game.instance.add_message(MESSAGES["monster_damage"].format(self.name, damage))

        target.take_damage(damage)

        # 死亡判定
        if target.hp <= 0:
            if target.entity_type == EntityType.MONSTER:
                entities.remove(target)
                if self.entity_type == EntityType.PLAYER:
                    self._add_xp(target.xp_given)
                    Game.instance.add_message(f"{target.name} {MESSAGES['monster_death']}")
            elif target.entity_type == EntityType.PLAYER:
                Game.instance.add_message(MESSAGES["death"])
