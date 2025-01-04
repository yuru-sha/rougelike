#!/usr/bin/env python3
from typing import List, Tuple
import tcod
from tcod import libtcodpy
from entity.entity import Entity, EntityType
from map.game_map import GameMap
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_HEIGHT
from utils.logger import setup_logger


class Renderer:
    """Handles all rendering operations for the game."""

    def __init__(self, console: tcod.console.Console):
        """Initialize the renderer.

        Args:
            console: The TCOD console to render to.
        """
        self.logger = setup_logger("renderer")
        self.logger.info("Initializing renderer")
        self.console = console
        self.game_map = None

    def render_all(
        self,
        entities: List[Entity],
        game_map: GameMap,
        player: Entity,
        messages: List[str],
    ) -> None:
        """Render the entire game screen.

        Args:
            entities: List of all entities to render.
            game_map: The current game map.
            player: The player entity.
            messages: List of messages to display.
        """
        self.logger.debug("Rendering frame")
        # Clear console completely
        self.console.clear()

        self.game_map = game_map  # Store game_map reference
        self._render_map(game_map)
        self._render_entities(entities)
        self._render_ui(player)
        self._render_messages(messages)

    def _render_map(self, game_map: GameMap) -> None:
        """Render the game map with FOV.

        Args:
            game_map: The game map to render.
        """
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = game_map.visible[x][y]
                explored = game_map.explored[x][y]

                if not visible and not explored:
                    continue

                wall = not game_map.tiles[x][y].transparent
                if wall:
                    if visible:
                        self.console.print(x, y + 1, "#", (255, 255, 255), (0, 0, 0))
                    elif explored:
                        self.console.print(x, y + 1, "#", (128, 128, 128), (0, 0, 0))
                else:
                    if visible:
                        self.console.print(x, y + 1, ".", (192, 192, 192), (0, 0, 0))
                    elif explored:
                        self.console.print(x, y + 1, ".", (64, 64, 64), (0, 0, 0))

    def _render_entities(self, entities: List[Entity]) -> None:
        """Render all entities in the game.

        Args:
            entities: List of entities to render.
        """
        # エンティティを描画順序でソート
        # 1. アイテム（最背面）
        # 2. モンスター
        # 3. プレイヤー（最前面）
        def get_render_order(entity: Entity) -> int:
            if entity.entity_type == EntityType.PLAYER:
                return 3
            elif entity.entity_type == EntityType.MONSTER:
                return 2
            else:
                return 1

        entities_in_render_order = sorted(entities, key=get_render_order)

        for entity in entities_in_render_order:
            # プレイヤーは常に表示、他のエンティティはFOV内のみ表示
            if (
                entity.entity_type == EntityType.PLAYER
                or self.game_map.visible[entity.x][entity.y]
            ):
                self._draw_entity(entity)

    def _draw_entity(self, entity: Entity) -> None:
        self.console.print(entity.x, entity.y + 1, entity.char, entity.color, (0, 0, 0))

    def _render_ui(self, player: Entity) -> None:
        """Render the game UI including status bar and message area.

        Args:
            player: The player entity whose stats to display.
        """
        # Draw status bar background (line 1)
        for x in range(SCREEN_WIDTH):
            self.console.print(x, 0, " ", (255, 255, 255), (0, 0, 0))

        # Display NetHack-style status
        status_text = (
            f"{player.name} "  # Player name
            f"St:{player.strength} "  # Strength
            f"HP:{player.hp}/{player.max_hp} "  # HP
            f"Lv:{player.level} "  # Player level
            f"Dlv:{player.dungeon_level} "  # Dungeon level
            f"$:{player.gold} "  # Gold
            f"XP:{player.xp}"  # Experience
        )

        self.console.print(
            1,
            0,  # Display on line 1
            status_text,
            (255, 255, 255),
            (0, 0, 0),
            alignment=libtcodpy.LEFT,
        )

        # Draw message area background (lines 47-49)
        for x in range(SCREEN_WIDTH):
            for y in range(47, SCREEN_HEIGHT):
                self.console.print(x, y, " ", (255, 255, 255), (0, 0, 0))

    def _render_messages(self, messages: List[str]) -> None:
        """Render the message log in the message area.

        Args:
            messages: List of messages to display.
        """
        # Clear message area background (lines 47-49)
        for x in range(SCREEN_WIDTH):
            for y in range(47, SCREEN_HEIGHT):
                self.console.print(x, y, " ", (255, 255, 255), (0, 0, 0))

        # Display latest 3 messages
        for i, message in enumerate(messages[-3:]):
            self.console.print(
                1, 47 + i, message, (255, 255, 255), (0, 0, 0), alignment=libtcodpy.LEFT
            )

    def clear_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            self._clear_entity(entity)

    def _clear_entity(self, entity: Entity) -> None:
        self.console.print(entity.x, entity.y + 1, " ", (0, 0, 0), (0, 0, 0))
