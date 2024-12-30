def handle_player_move(game_manager: GameManager, dx: int, dy: int) -> None:
    current_progress = game_manager.progress
    new_player_pos = current_progress.player.move(dx, dy)

    new_progress = GameProgress(
        player=new_player_pos,
        current_map=current_progress.current_map,
        entities=current_progress.entities,
        game_level=current_progress.game_level,
        explored_levels=current_progress.explored_levels,
        has_amulet=current_progress.has_amulet,
    )

    game_manager.update_progress(new_progress)
