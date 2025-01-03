#!/usr/bin/env python3
from typing import List, Optional, Tuple
import tcod
from tcod.event import KeySym
from entity.entity import Entity, EntityType
from map.game_map import GameMap
from .render import Renderer
from utils.logger import setup_logger
from config.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MAP_WIDTH,
    MAP_HEIGHT,
    INVENTORY_CAPACITY,
    TITLE,
    STARTING_WEAPON_POWER,
    STARTING_WEAPON_BONUS,
    STARTING_WEAPON_DICE,
    STARTING_BOW_POWER,
    STARTING_BOW_DICE,
    STARTING_ARROWS,
    STARTING_FOOD,
    PLAYER_START_HP,
    PLAYER_START_DAMAGE,
    PLAYER_START_STRENGTH,
)
from config.messages import MESSAGES
from config.items import MELEE_WEAPONS, RANGED_WEAPONS, AMMO, FOODS


class Game:
    def __init__(self):
        self.logger = setup_logger("game")
        self.logger.info("Game initializing...")

        self.player = self._create_player()
        self.entities: List[Entity] = [self.player]
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, 1)
        self.game_map.make_map(self.player, self.entities)
        self._equip_player(self.player)
        self.game_map.compute_fov(
            self.player.x, self.player.y, self.player.sight_radius
        )

        self.logger.info("Game initialized successfully")
        self.messages = []  # メッセージ履歴を保持
        self._show_welcome_message()

    def _show_welcome_message(self) -> None:
        """Display the initial welcome message in the message area."""
        welcome_messages = [
            "Welcome to the Dungeons of Doom!",
            "Your quest: Find the Amulet of Yendor hidden in the depths.",
            "Press ? for help, or press ESC to quit.",
        ]
        for msg in welcome_messages:
            self.messages.append(msg)

    def _create_player(self) -> Entity:
        player = Entity(
            0,
            0,
            "@",
            (255, 255, 255),
            "Player",
            EntityType.PLAYER,
            inventory=[],
            hp=PLAYER_START_HP,
            max_hp=PLAYER_START_HP,
            power=PLAYER_START_DAMAGE,  # 1d4 damage
            strength=PLAYER_START_STRENGTH,
            sight_radius=8,
        )
        return player

    def _create_starting_equipment(self) -> List[Entity]:
        """Create the initial set of equipment for the player.

        Returns:
            List[Entity]: A list containing the starting equipment entities.
        """
        equipment = []

        # Starting weapon (Dagger)
        dagger_data = MELEE_WEAPONS["Dagger"]
        dagger = Entity(
            0,
            0,
            dagger_data["char"],
            dagger_data["color"],
            "Dagger",
            EntityType.WEAPON,
            blocks=False,
            damage_dice=(STARTING_WEAPON_POWER, STARTING_WEAPON_DICE),
            hit_bonus=STARTING_WEAPON_BONUS,
            two_handed=False,
        )
        equipment.append(dagger)

        # Starting ranged weapon (Short Bow)
        bow_data = RANGED_WEAPONS["Short Bow"]
        bow = Entity(
            0,
            0,
            bow_data["char"],
            bow_data["color"],
            "Short Bow",
            EntityType.RANGED,
            blocks=False,
            damage_dice=(STARTING_BOW_POWER, STARTING_BOW_DICE),
            hit_bonus=1,
            two_handed=True,
            ranged=True,
            ammo_type="arrow",
        )
        equipment.append(bow)

        # Starting ammunition
        arrow_data = AMMO["Arrow"]
        arrows = Entity(
            0,
            0,
            arrow_data["char"],
            arrow_data["color"],
            f"Arrows ({STARTING_ARROWS})",
            EntityType.AMMO,
            blocks=False,
            damage_dice=arrow_data["damage"],
            ammo_type="arrow",
            ammo_count=STARTING_ARROWS,
        )
        equipment.append(arrows)

        # Starting food
        food_data = FOODS["Ration"]
        food = Entity(
            0,
            0,
            food_data["char"],
            food_data["color"],
            f"Food Rations ({STARTING_FOOD})",
            EntityType.FOOD,
            blocks=False,
            nutrition=food_data["nutrition"],
            food_count=STARTING_FOOD,
        )
        equipment.append(food)

        return equipment

    def _equip_player(self, player: Entity) -> None:
        starting_equipment = self._create_starting_equipment()
        for item in starting_equipment:
            player.inventory.append(item)

    def run(self) -> None:
        tileset = tcod.tileset.load_tilesheet(
            "assets/fonts/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        )

        with tcod.context.new_terminal(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            tileset=tileset,
            title=TITLE,
            vsync=True,
        ) as context:
            console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
            renderer = Renderer(console)

            # 初期ゲーム状態を設定
            self.game_state = "playing"

            while True:
                renderer.render_all(
                    self.entities, self.game_map, self.player, self.messages
                )

                # インベントリ表示中はインベントリを描画
                if self.game_state == "inventory":
                    self._render_inventory(console)

                context.present(console)

                renderer.clear_all(self.entities)

                for event in tcod.event.wait():
                    action = self._handle_input(event)
                    if action:
                        if self._process_result(action):
                            return

                # プレイ中のみモンスターのターンを処理
                if self.game_state == "playing":
                    self._process_monster_turns()

    def _handle_input(self, event: tcod.event.Event) -> Optional[str]:
        if isinstance(event, tcod.event.Quit):
            return "quit"
        elif isinstance(event, tcod.event.KeyDown):
            return self._handle_key(event)
        return None

    def _handle_key(self, event: tcod.event.KeyDown) -> Optional[str]:
        # インベントリ表示中は専用の入力処理
        if hasattr(self, "game_state") and self.game_state == "inventory":
            return self._handle_inventory_input(event)

        if self._is_movement_key(event):
            dx, dy = self._get_movement_delta(event)
            self._move_player(dx, dy)
            return None

        if event.sym == KeySym.g:
            return self._handle_pickup()

        if event.sym == KeySym.i:
            self._show_inventory()
            return None

        if event.sym == KeySym.d:
            return self._drop_item()

        if self._is_stairs_key(event):
            return self._handle_stairs(event)

        if event.sym == KeySym.ESCAPE:
            return "quit"

        return None

    def _is_movement_key(self, event: tcod.event.KeyDown) -> bool:
        return event.sym in (
            KeySym.UP,
            KeySym.DOWN,
            KeySym.LEFT,
            KeySym.RIGHT,
            KeySym.h,
            KeySym.j,
            KeySym.k,
            KeySym.l,
        )

    def _get_movement_delta(self, event: tcod.event.KeyDown) -> Tuple[int, int]:
        key = event.sym

        if key in (KeySym.UP, KeySym.k):
            return (0, -1)
        elif key in (KeySym.DOWN, KeySym.j):
            return (0, 1)
        elif key in (KeySym.LEFT, KeySym.h):
            return (-1, 0)
        elif key in (KeySym.RIGHT, KeySym.l):
            return (1, 0)

        return (0, 0)

    def _move_player(self, dx: int, dy: int) -> None:
        """Move the player by the given delta if possible.

        Args:
            dx: The change in x-coordinate.
            dy: The change in y-coordinate.
        """
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        # Check if within map bounds
        if not self.game_map.in_bounds(new_x, new_y):
            return

        # Check if walkable
        if not self.game_map.tiles[new_x][new_y].walkable:
            return

        # Check for monster collision
        target = None
        for entity in self.entities:
            if (
                entity.blocks
                and entity.x == new_x
                and entity.y == new_y
                and entity.entity_type == EntityType.MONSTER
            ):
                target = entity
                break

        if target:
            # Attack monster
            self._attack_monster(target)
        else:
            # Move
            self.player.x = new_x
            self.player.y = new_y

            # Auto pickup items at destination
            self._auto_pickup()

            # Update FOV
            self.game_map.compute_fov(
                self.player.x, self.player.y, self.player.sight_radius
            )

    def _auto_pickup(self) -> None:
        """Automatically pick up gold at the player's current position."""
        # Look for gold at player's position
        for entity in list(self.entities):  # Create copy of list for iteration
            if (
                entity.x == self.player.x
                and entity.y == self.player.y
                and entity.entity_type == EntityType.GOLD
            ):
                # Add gold to player's purse
                self.player.gold += entity.gold_amount
                self.entities.remove(entity)

    def _attack_monster(self, monster: Entity) -> None:
        """Handle player's attack against a monster.

        Args:
            monster: The monster entity being attacked.
        """
        # Find player's equipped weapon
        weapon = None
        for item in self.player.inventory:
            if item.entity_type == EntityType.WEAPON:
                weapon = item
                break

        # Calculate base damage
        damage = self._roll_damage(self.player.power)

        # Add weapon damage
        if weapon and weapon.damage_dice:
            weapon_damage = self._roll_damage(weapon.damage_dice)
            damage += weapon_damage

            # Apply hit bonus
            if weapon.hit_bonus:
                damage += weapon.hit_bonus

        # Apply damage
        monster.take_damage(damage)

        # Check if monster is defeated
        if monster.hp <= 0:
            self.entities.remove(monster)
            # Award experience points
            if monster.xp_given:
                self.player._add_xp(monster.xp_given)

    def _roll_damage(self, damage_dice: Tuple[int, int]) -> int:
        """Roll damage based on dice configuration.

        Args:
            damage_dice: A tuple containing (base_damage, number_of_dice).

        Returns:
            int: The total damage value.
        """
        import random

        base_damage, dice = damage_dice
        return base_damage + random.randint(1, dice)

    def _process_monster_turns(self) -> None:
        for entity in self.entities:
            if entity.entity_type == EntityType.MONSTER and entity.hp > 0:
                entity.take_turn(self.player, self.game_map, self.entities)

    def _is_stairs_key(self, event: tcod.event.KeyDown) -> bool:
        return event.sym in (KeySym.PERIOD, KeySym.COMMA)

    def _handle_stairs(self, event: tcod.event.KeyDown) -> Optional[str]:
        for entity in self.entities:
            if entity.x == self.player.x and entity.y == self.player.y:
                if (
                    event.sym == KeySym.PERIOD
                    and entity.entity_type == EntityType.STAIRS_DOWN
                ):
                    self._change_level(self.player.dungeon_level + 1)
                    return None
                elif (
                    event.sym == KeySym.COMMA
                    and entity.entity_type == EntityType.STAIRS_UP
                ):
                    self._change_level(self.player.dungeon_level - 1)
                    return None
        return None

    def _handle_pickup(self) -> str:
        self.player.pick_up(self.entities)
        return None

    def _show_inventory(self) -> None:
        if not self.player.inventory:
            return

        # Set game state to inventory mode
        self.game_state = "inventory"
        self.inventory_index = None

    def _handle_inventory_input(self, event: tcod.event.KeyDown) -> Optional[str]:
        # ESCキーでインベントリを閉じる
        if event.sym == KeySym.ESCAPE:
            self.game_state = "playing"
            return None

        # a-zキーでアイテムを選択
        index = event.sym - KeySym.a
        if 0 <= index < len(self.player.inventory):
            self._use_item(index)
            self.game_state = "playing"
            return None

        return None

    def _use_item(self, index: int) -> None:
        if index >= len(self.player.inventory):
            return

        item = self.player.inventory[index]
        if item.effect:
            self.player.use_item(item, self.entities, self.game_map)

    def _drop_item(self) -> Optional[str]:
        if not self.player.inventory:
            return MESSAGES["inventory_empty"]

        print("\nSelect an item to drop:")
        for i, item in enumerate(self.player.inventory):
            print(f"{chr(97 + i)}) {item.name}")

        key = input()
        if ord("a") <= ord(key) <= ord("z"):
            item_index = ord(key) - ord("a")
            if item_index < len(self.player.inventory):
                item = self.player.inventory[item_index]
                self.player.drop_item(item, self.entities)
                return None

        return None

    def _process_result(self, result: str) -> bool:
        if result == "quit":
            return True

        if self.player.hp <= 0:
            print(MESSAGES["death"])
            return True

        for entity in self.entities:
            if (
                entity.entity_type == EntityType.AMULET
                and entity.x == self.player.x
                and entity.y == self.player.y
            ):
                print(MESSAGES["victory"])
                return True

        return False

    def _change_level(self, new_level: int) -> None:
        self.player.dungeon_level = new_level
        self.entities = [self.player]
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, new_level)
        self.game_map.make_map(self.player, self.entities)
        # 新しい階層でFOVを計算
        self.game_map.compute_fov(
            self.player.x, self.player.y, self.player.sight_radius
        )

    def _render_inventory(self, console: tcod.console.Console) -> None:
        # Set inventory window position and size
        inventory_width = 40
        inventory_height = len(self.player.inventory) + 2
        inventory_x = SCREEN_WIDTH // 2 - inventory_width // 2
        inventory_y = SCREEN_HEIGHT // 2 - inventory_height // 2

        # Draw window background
        console.draw_frame(
            inventory_x,
            inventory_y,
            inventory_width,
            inventory_height,
            "Inventory",
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        # Draw item list
        if not self.player.inventory:
            console.print(
                inventory_x + 1, inventory_y + 1, "Empty inventory", fg=(255, 255, 255)
            )
        else:
            # Find equipped weapons
            equipped_weapon = None
            equipped_ranged = None
            for item in self.player.inventory:
                if item.entity_type == EntityType.WEAPON:
                    equipped_weapon = item
                elif item.entity_type == EntityType.RANGED:
                    equipped_ranged = item

            for i, item in enumerate(self.player.inventory):
                key = chr(ord("a") + i)
                equipped_mark = ""

                # Add marks for equipped items
                if item == equipped_weapon:
                    equipped_mark = " (wielded)"
                elif item == equipped_ranged:
                    equipped_mark = " (ready)"
                elif (
                    item.entity_type == EntityType.AMMO
                    and equipped_ranged
                    and item.ammo_type == equipped_ranged.ammo_type
                ):
                    equipped_mark = " (quivered)"

                # Get item name with stack count
                item_name = item.display_name

                text = f"{key}) {item_name}{equipped_mark}"
                console.print(
                    inventory_x + 1, inventory_y + i + 1, text, fg=(255, 255, 255)
                )
