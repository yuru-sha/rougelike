"""
Handles all user input and converts them to game commands
"""
from blessed import Terminal
from utils.logger import get_logger
from typing import Optional

logger = get_logger(__name__)

class InputHandler:
    def __init__(self):
        self.terminal = Terminal()

    def get_command(self) -> Optional[str]:
        """キー入力を処理してコマンドを返す"""
        key = self.terminal.inkey()
        
        if key.name == 'KEY_ESCAPE' or key == 'q':
            return 'quit'
        
        # 移動
        if key.name == 'KEY_UP' or key == 'k':
            return 'move_up'
        if key.name == 'KEY_DOWN' or key == 'j':
            return 'move_down'
        if key.name == 'KEY_LEFT' or key == 'h':
            return 'move_left'
        if key.name == 'KEY_RIGHT' or key == 'l':
            return 'move_right'
        
        # 階段
        if key == '>':
            return 'down'
        if key == '<':
            return 'up'
        
        return None 