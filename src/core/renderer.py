"""
Terminal renderer for Rogue
Handles all display operations using blessed
"""
from blessed import Terminal
from core.game_state import GameState
from utils.logger import get_logger
import time
from typing import Tuple

logger = get_logger(__name__)

class Renderer:
    def __init__(self):
        self.terminal = Terminal()
        self.screen_buffer = []
        self.message_area_height = 1
        self.current_message = "Welcome to Roguelike!"
        
        # 色の定義を拡張
        self.colors = {
            'visible': self.terminal.white,
            'player': self.terminal.white_bold,
            'wall': self.terminal.white,
            'floor': self.terminal.white,
            'status': self.terminal.white,
            'message': self.terminal.white_bold,
        }
        
        # 画面レイアウト
        self.layout = {
            'message_y': 0,
            'map_start_y': 2,  # メッセージ行 + 空白行
            'status_y': self.terminal.height - 1
        }

    def render(self, game_state: GameState) -> None:
        """ゲーム状態を画面に描画"""
        with self.terminal.location():  # コンテキストマネージャで位置を管理
            self._render_messages()
            self._render_map(game_state)
            self._render_status(game_state)

    def _render_map(self, game_state: GameState) -> None:
        """ダンジョンマップを描画"""
        buffer = []
        map_y = self.layout['map_start_y']
        
        for y in range(game_state.current_map.height):
            screen_y = y + map_y
            for x in range(game_state.current_map.width):
                position = (x, y)
                char = self._get_display_char(position, game_state)
                color = self._get_display_color(position, game_state)
                buffer.append(self.terminal.move_xy(x, screen_y) + color + char)
        
        print(''.join(buffer), end='', flush=True)

    def _get_display_char(self, position: Tuple[int, int], game_state: GameState) -> str:
        """表示する文字を決定"""
        x, y = position
        if position not in game_state.current_map.visible:
            return ' '
        
        if position == game_state.player.position:
            return '@'
        
        for entity in game_state.entities:
            if entity.position == position:
                return entity.char
        
        return game_state.current_map.get_tile_char(x, y)

    def _get_display_color(self, position: Tuple[int, int], game_state: GameState) -> str:
        """表示する色を決定"""
        if position not in game_state.current_map.visible:
            return self.terminal.normal
        
        if position == game_state.player.position:
            return self.colors['player']
            
        x, y = position
        tile = game_state.current_map.get_tile_char(x, y)
        if tile in '|-':
            return self.colors['wall']
        return self.colors['floor']

    def _render_messages(self) -> None:
        """メッセージエリアを描画"""
        with self.terminal.location(0, self.layout['message_y']):
            print(self.colors['message'] + self.current_message.ljust(self.terminal.width))

    def _render_status(self, game_state: GameState) -> None:
        """ステータス行を描画"""
        status = (
            f"Level:{game_state.game_level} "
            f"Gold:{game_state.player.gold} "
            f"Hp:{game_state.player.hp}({game_state.player.max_hp}) "
            f"Str:{game_state.player.strength}({game_state.player.strength}) "
            f"Arm:{getattr(game_state.player, 'armor_class', 0)} "
            f"Exp:{game_state.player.level}/{game_state.player.exp}"
        )
        with self.terminal.location(0, self.layout['status_y']):
            print(self.colors['status'] + status.ljust(self.terminal.width))

    def add_message(self, message: str) -> None:
        """メッセージをバッファに追加"""
        logger.debug(f"Adding message: {message}")
        self.screen_buffer.append(message)
        self.current_message = message  # 現在のメッセージを更新
        
        # 最新の10件のメッセージを保持
        if len(self.screen_buffer) > 10:
            self.screen_buffer.pop(0) 