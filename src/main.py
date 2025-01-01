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
    """Configure dependency injection"""
    # Initialize renderer
    renderer = Renderer()
    
    # Generate map
    game_map = GameMap()
    entities = game_map.generate()
    
    # Create player
    player = Player(
        x=game_map.rooms[0].center[0],
        y=game_map.rooms[0].center[1]
    )
    
    # Initialize player's FOV
    player._update_fov(game_map)
    
    # Create initial game state
    game_state = GameState(
        player=player,
        current_map=game_map,
        entities=entities
    )
    
    # Add welcome message
    renderer.add_message("Welcome to Roguelike!")
    
    # 依存関係の設定
    binder.bind(GameState, to=game_state)
    binder.bind(InputHandler, to=InputHandler())
    binder.bind(Renderer, to=renderer)

def main():
    """ゲームのエントリーポイント"""
    logger.info("Starting Rogue game")
    
    # DIコンテナの設定
    injector = Injector(configure)
    
    # ゲームエンジンの取得と実行
    game = injector.get(GameEngine)
    game.run()

if __name__ == "__main__":
    main() 