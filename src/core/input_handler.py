"""
Handles all user input and converts them to game commands
"""

from blessed import Terminal
from utils.logger import get_logger
from typing import Optional

logger = get_logger(__name__)


class InputHandler:
    """
    Handles keyboard input and converts it to game commands
    Uses blessed terminal for input processing
    """

    def __init__(self):
        self.terminal = Terminal()

    def get_command(self) -> Optional[str]:
        """
        Process keyboard input and return corresponding command

        Returns:
            str or None: Command string if valid input, None otherwise
        """
        key = self.terminal.inkey()

        if key.name == "KEY_ESCAPE" or key == "q":
            return "quit"

        # y/n confirmation
        if key == "y":
            return "y"
        if key == "n":
            return "n"

        # Movement commands
        if key.name == "KEY_UP" or key == "k":
            return "move_up"
        if key.name == "KEY_DOWN" or key == "j":
            return "move_down"
        if key.name == "KEY_LEFT" or key == "h":
            return "move_left"
        if key.name == "KEY_RIGHT" or key == "l":
            return "move_right"

        # Stair movement
        if key == ">":
            return "down"
        if key == "<":
            return "up"

        return None
