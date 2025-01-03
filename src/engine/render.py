#!/usr/bin/env python3
from typing import List, Tuple
import tcod
from tcod import libtcodpy
from entity.entity import Entity, EntityType
from map.game_map import GameMap
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_HEIGHT

class Renderer:
    def __init__(self, console: tcod.console.Console):
        self.console = console
        self.game_map = None

    def render_all(self, entities: List[Entity], game_map: GameMap, player: Entity) -> None:
        # コンソールを完全にクリア
        self.console.clear()
        
        self.game_map = game_map  # game_mapを保存
        self._render_map(game_map)
        self._render_entities(entities)
        self._render_ui(player)

    def _render_map(self, game_map: GameMap) -> None:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = game_map.visible[x][y]
                explored = game_map.explored[x][y]

                if not visible and not explored:
                    continue

                wall = not game_map.tiles[x][y].transparent
                if wall:
                    if visible:
                        self.console.print(x, y + 1, '#', (255, 255, 255), (0, 0, 0))
                    elif explored:
                        self.console.print(x, y + 1, '#', (128, 128, 128), (0, 0, 0))
                else:
                    if visible:
                        self.console.print(x, y + 1, '.', (192, 192, 192), (0, 0, 0))
                    elif explored:
                        self.console.print(x, y + 1, '.', (64, 64, 64), (0, 0, 0))

    def _render_entities(self, entities: List[Entity]) -> None:
        # エンティティを描画順にソート
        entities_in_render_order = sorted(
            entities,
            key=lambda x: 1 if x.entity_type == EntityType.PLAYER else 0
        )

        for entity in entities_in_render_order:
            # プレイヤーは常に表示、それ以外は可視タイルにいる場合のみ表示
            if entity.entity_type == EntityType.PLAYER or self.game_map.visible[entity.x][entity.y]:
                self._draw_entity(entity)

    def _draw_entity(self, entity: Entity) -> None:
        self.console.print(
            entity.x, entity.y + 1,
            entity.char,
            entity.color,
            (0, 0, 0)
        )

    def _render_ui(self, player: Entity) -> None:
        # ステータスバーの背景（1行目）
        for x in range(SCREEN_WIDTH):
            self.console.print(x, 0, ' ', (255, 255, 255), (0, 0, 0))

        # NetHack風のステータス表示
        status_text = (
            f"{player.name} "  # プレイヤー名
            f"St:{player.strength} "  # 筋力
            f"HP:{player.hp}/{player.max_hp} "  # HP
            f"Lv:{player.level} "  # プレイヤーレベル
            f"Dlv:{player.dungeon_level} "  # ダンジョンレベル
            f"$:{player.gold} "  # 所持金
            f"XP:{player.xp}"  # 経験値
        )
        
        self.console.print(
            1, 0,  # 1行目に表示
            status_text,
            (255, 255, 255),
            (0, 0, 0),
            alignment=libtcodpy.LEFT
        )

        # メッセージ領域の背景（48-50行目）
        for x in range(SCREEN_WIDTH):
            for y in range(47, SCREEN_HEIGHT):
                self.console.print(x, y, ' ', (255, 255, 255), (0, 0, 0))

    def clear_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            self._clear_entity(entity)

    def _clear_entity(self, entity: Entity) -> None:
        self.console.print(
            entity.x, entity.y + 1,
            ' ',
            (0, 0, 0),
            (0, 0, 0)
        ) 