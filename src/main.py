#!/usr/bin/env python3
"""
Main entry point for the Rogue game
"""
from injector import Injector
from core.game_engine import GameEngine
from core.game_state import GameState
from core.input_handler import InputHandler
from core.renderer import Renderer
from core.map import GameMap
from entities.player import Player
from utils.logger import get_logger

logger = get_logger(__name__)


def configure(binder):
    """
    Configure dependency injection bindings

    Args:
        binder: Injector binder instance
    """
    # Initialize renderer
    renderer = Renderer()

    # Generate initial map
    game_map = GameMap()
    entities = game_map.generate()

    # Create player at first room center
    player = Player(x=game_map.rooms[0].center[0], y=game_map.rooms[0].center[1])

    # Initialize player's field of view
    player._update_fov(game_map)

    # Create initial game state
    game_state = GameState(player=player, current_map=game_map, entities=entities)

    # Configure dependency bindings
    binder.bind(GameState, to=game_state)
    binder.bind(InputHandler, to=InputHandler())
    binder.bind(Renderer, to=renderer)


def main():
    """
    Game entry point
    Sets up dependency injection and starts game
    """
    logger.info("Starting Rogue game")

    # Setup DI container
    injector = Injector(configure)

    # Get and run game engine
    game = injector.get(GameEngine)
    game.run()


if __name__ == "__main__":
    main()
