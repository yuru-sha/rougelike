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
            "visible": self.terminal.white,
            "player": self.terminal.white_bold,
            "wall": self.terminal.white,
            "floor": self.terminal.white,
            "status": self.terminal.white,
            "message": self.terminal.white_bold,
        }

        # 画面レイアウト
        self.layout = {
            "message_y": 0,
            "map_start_y": 1,  # メッセージ行のみ（空白行なし）
            "map_height": 22,  # マップの高さを22行に設定
            "status_y": 23,  # マップの下にステータス行を配置
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
        map_y = self.layout["map_start_y"]

        for y in range(game_state.current_map.height):
            screen_y = y + map_y
            for x in range(game_state.current_map.width):
                position = (x, y)
                char = self._get_display_char(position, game_state)
                color = self._get_display_color(position, game_state)
                buffer.append(self.terminal.move_xy(x, screen_y) + color + char)

        print("".join(buffer), end="", flush=True)

    def _get_display_char(
        self, position: Tuple[int, int], game_state: GameState
    ) -> str:
        """表示する文字を決定"""
        x, y = position
        if position not in game_state.current_map.visible:
            return " "

        if position == game_state.player.position:
            return "@"

        for entity in game_state.entities:
            if entity.position == position:
                return entity.char

        return game_state.current_map.get_tile_char(x, y)

    def _get_display_color(
        self, position: Tuple[int, int], game_state: GameState
    ) -> str:
        """表示する色を決定"""
        if position not in game_state.current_map.visible:
            return self.terminal.normal

        if position == game_state.player.position:
            return self.colors["player"]

        x, y = position
        tile = game_state.current_map.get_tile_char(x, y)
        if tile in "|-":
            return self.colors["wall"]
        return self.colors["floor"]

    def _render_messages(self) -> None:
        """メッセージエリアを描画"""
        with self.terminal.location(0, self.layout["message_y"]):
            print(
                self.colors["message"] + self.current_message.ljust(self.terminal.width)
            )

    def _render_status(self, game_state: GameState) -> None:
        """ステータス行を描画"""
        player = game_state.player
        status = (
            f"Level:{game_state.game_level} "
            f"Gold:{player.gold} "
            f"Hp:{player.hp}({player.max_hp}) "
            f"Str:{player.strength} "
            f"Ac:{getattr(player, 'armor_class', 0)} "
            f"Exp:{player.level}/{player.exp}"
        )
        with self.terminal.location(0, self.layout["status_y"]):
            print(self.colors["status"] + status.ljust(self.terminal.width))

    def add_message(self, message: str) -> None:
        """メッセージをバッファに追加"""
        logger.debug(f"Adding message: {message}")
        self.screen_buffer.append(message)
        self.current_message = message  # 現在のメッセージを更新

        # 最新の10件のメッセージを保持
        if len(self.screen_buffer) > 10:
            self.screen_buffer.pop(0)

    def clear(self) -> None:
        """Clear the terminal screen"""
        print(self.terminal.clear)

    def get_player_name(self) -> str:
        """
        Get player name input

        Returns:
            str: Player name (max 15 chars)
        """
        print(
            self.terminal.move(
                self.terminal.height // 2 - 5, self.terminal.width // 2 - 10
            )
        )
        print("Enter your name: ", end="", flush=True)

        # Clear input buffer
        import sys, termios, tty

        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

        # Get name (max 15 chars)
        return input()[:15]

    def show_game_over(self, score: int, gold: int, level: int, depth: int) -> None:
        """
        Display game over screen

        Args:
            score: Final score
            gold: Gold collected
            level: Player level
            depth: Maximum dungeon depth reached
        """
        self.clear()

        messages = [
            "GAME OVER",
            "=" * 40,
            f"Final Score: {score}",
            f"Gold: {gold}",
            f"Level: {level}",
            f"Max Depth: {depth}",
            "-" * 40,
            "",
            "Press any key to continue...",
        ]

        # Display messages in center of screen
        y = (self.terminal.height - len(messages)) // 2
        for i, msg in enumerate(messages):
            x = (self.terminal.width - len(msg)) // 2
            print(self.terminal.move(y + i, x) + msg)

        # Wait for key press
        self.terminal.inkey()
