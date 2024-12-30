"""
Game engine for Rogue implementation
Handles the main game loop and core game mechanics
"""

from typing import Optional
from blessed import Terminal
from injector import inject
from core.game_state import GameState
from core.input_handler import InputHandler
from core.map import GameMap
from core.renderer import Renderer
from utils.logger import get_logger
from utils.score_manager import ScoreManager
from entities.gold import Gold  # 追加
from entities.amulet import AmuletOfYendor  # 追加
from entities.stairs import Stairs
from entities.monster import Monster  # 追加

logger = get_logger(__name__)


class GameEngine:
    @inject
    def __init__(
        self, game_state: GameState, input_handler: InputHandler, renderer: Renderer
    ):
        self.game_state = game_state
        self.input_handler = input_handler
        self.renderer = renderer
        self.terminal = Terminal()

        # 移動方向の定義
        self.movement_vectors = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
        }
        self.score_manager = ScoreManager()

    def run(self) -> None:
        """Game main loop"""
        logger.info("Starting game")

        with self.terminal.fullscreen(), self.terminal.cbreak():
            while True:
                # 最新のメッセージを表示
                self.renderer.render(self.game_state)

                # 勝利条件をチェック
                if self.game_state.check_victory():
                    self._show_victory()
                    break

                # プレイヤーが死亡していたらゲームオーバー
                if self.game_state.player.is_dead:
                    self._show_game_over()
                    break

                # 入力処理
                if not self._process_input():
                    self._show_game_over()
                    break

                # 位置に応じたメッセージを更新
                self._update_location_message()

    def _process_input(self) -> bool:
        """Process input and return whether to continue game"""
        command = self.input_handler.get_command()
        if command is None:
            return True

        if command == "quit":
            # 途中終了時はスコアを記録しない
            self.renderer.add_message("Really quit? (y/n)")
            self.renderer.render(self.game_state)  # メッセージを表示

            # y/nの入力を待つ
            while True:
                confirm = self.input_handler.get_command()
                if confirm == "y":
                    return False
                elif confirm == "n":
                    self.renderer.add_message("")  # メッセージをクリア
                    return True

        if command.startswith("move_"):
            self._handle_movement(command.split("_")[1])
        elif command in ["up", "down"]:
            self._handle_stairs(command)

        return True

    def _handle_movement(self, direction: str) -> None:
        """Handle player movement in specified direction"""
        if direction not in self.movement_vectors:
            return

        dx, dy = self.movement_vectors[direction]
        player = self.game_state.player
        new_x = player.x + dx
        new_y = player.y + dy

        # Check for monsters at destination
        monster = self._get_monster_at(new_x, new_y)
        if monster:
            self._handle_combat(monster)
            return

        # If no monster, try to move
        if player.move(dx, dy, self.game_state.current_map):
            self._check_pickup()

    def _get_monster_at(self, x: int, y: int) -> Optional[Monster]:
        """Get monster at specified position"""
        for entity in self.game_state.entities:
            if (
                isinstance(entity, Monster)
                and entity.x == x
                and entity.y == y
                and not entity.is_dead
            ):
                return entity
        return None

    def _handle_combat(self, monster: Monster) -> None:
        """Handle combat between player and monster"""
        # Player attacks monster
        hit, damage = self.game_state.player.attack(monster)

        if hit:
            self.renderer.add_message(
                f"You hit the {monster.name} for {damage} damage!"
            )
            if monster.is_dead:
                self.renderer.add_message(f"You have defeated the {monster.name}!")
                return
        else:
            self.renderer.add_message(f"You miss the {monster.name}.")

        # Monster counterattacks if still alive
        hit, damage = monster.attack(self.game_state.player)

        if hit:
            self.renderer.add_message(
                f"The {monster.name} hits you for {damage} damage!"
            )
            if self.game_state.player.is_dead:
                self.renderer.add_message("You have died!")
                return
        else:
            self.renderer.add_message(f"The {monster.name} misses you.")

    def _check_pickup(self) -> None:
        """Check for and handle item pickup at player's position"""
        player = self.game_state.player

        # Use list comprehension for better performance
        pickable_entities = [
            e for e in self.game_state.entities if e.position == player.position
        ]

        for entity in pickable_entities:
            if isinstance(entity, Gold):
                self._handle_gold_pickup(entity)
            elif isinstance(entity, AmuletOfYendor):
                self._handle_amulet_pickup(entity)

    def _handle_gold_pickup(self, gold: Gold) -> None:
        """Handle gold pickup"""
        self.game_state.player.add_gold(gold.amount)
        self.game_state.entities.remove(gold)
        self.renderer.add_message(f"You found {gold.amount} gold pieces.")
        logger.info(f"Player picked up {gold.amount} gold")

    def _handle_amulet_pickup(self, amulet: AmuletOfYendor) -> None:
        """Handle Amulet pickup"""
        self.game_state.has_amulet = True
        self.game_state.entities.remove(amulet)
        self.renderer.add_message("You found the Amulet of Yendor!")
        logger.info("Player found the Amulet of Yendor")

    def _update_location_message(self) -> None:
        """Update message based on current location"""
        x, y = self.game_state.player.position

        for room in self.game_state.current_map.rooms:
            if room.x <= x < room.x + room.width and room.y <= y < room.y + room.height:
                break

    def _show_game_over(self) -> None:
        """Display game over screen when player dies"""
        self.renderer.clear()

        score = self.game_state.calculate_score()  # Amuletボーナスなし
        gold = self.game_state.player.gold
        level = self.game_state.player.level
        depth = len(self.game_state.explored_levels)

        # "You have died!" メッセージを表示
        self.renderer.add_message("You have died!")

        # Get player name
        name = self.renderer.get_player_name()

        # 死亡時のスコアを記録
        rank = self.score_manager.add_score(
            name=name, score=score, gold=gold, level=level, depth=depth, victory=False
        )

        # Show high scores
        self._show_high_scores(rank)

    def _show_high_scores(self, current_rank: int = None) -> None:
        """Display high score screen"""
        print(self.terminal.clear)

        messages = [
            "HIGH SCORES",
            "=" * 70,  # 幅を広げる
            f"{'Rank':<6}{'Name':<16}{'Score':>8}{'Gold':>8}{'Level':>8}{'Depth':>8}{'Date':>20}",  # 列幅を調整
            "-" * 70,  # 幅を広げる
        ]

        for i, score in enumerate(self.score_manager.get_high_scores(), 1):
            rank_marker = ">" if i == current_rank else " "
            messages.append(
                f"{rank_marker}{i:<5}{score['name']:<16}{score['score']:>8}"
                f"{score['gold']:>8}{score['level']:>8}{score['depth']:>8}"
                f"{score['date']:>20}"  # 日付の列幅を広げる
            )

        messages.extend(["-" * 70, "", "Press any key to exit..."])  # 幅を広げる

        # メッセージを中央に表示
        y = (self.terminal.height - len(messages)) // 2
        for i, msg in enumerate(messages):
            x = (self.terminal.width - len(msg)) // 2
            print(self.terminal.move(y + i, x) + msg)

        # キー入力を待つ
        self.input_handler.get_command()

    def _show_victory(self) -> None:
        """Display victory screen when player wins"""
        self.renderer.clear()

        # Amuletボーナス(20,000)を含むスコア計算
        score = self.game_state.calculate_score()
        gold = self.game_state.player.gold
        level = self.game_state.player.level
        depth = len(self.game_state.explored_levels)

        # "You have won!" メッセージを表示
        self.renderer.add_message("You have won!")

        # Get player name
        name = self.renderer.get_player_name()

        # 勝利時のスコアを記録
        rank = self.score_manager.add_score(
            name=name, score=score, gold=gold, level=level, depth=depth, victory=True
        )

        # Show high scores
        self._show_high_scores(rank)

    def _handle_stairs(self, direction: str) -> None:
        """Handle stair movement"""
        player = self.game_state.player

        # Check for stairs at player's position
        for entity in self.game_state.entities:
            if (
                isinstance(entity, Stairs)
                and entity.position == player.position
                and entity.direction == direction
            ):
                self._change_level(direction)
                return

        self.renderer.add_message(f"I see no {direction} staircase here.")

    def _change_level(self, direction: str) -> None:
        """Change dungeon level"""
        current_level = self.game_state.current_map.level
        new_level = current_level + (1 if direction == "down" else -1)

        if not 1 <= new_level <= 26:
            return

        # Generate new level
        new_map = GameMap(level=new_level)
        entities = new_map.generate()

        # Place player near appropriate stairs
        if direction == "down":
            room = new_map.rooms[0]  # Room with up stairs
        else:
            room = new_map.rooms[-1]  # Room with down stairs

        player = self.game_state.player
        player.x, player.y = room.center
        player._update_fov(new_map)

        # Update game state
        self.game_state.current_map = new_map
        self.game_state.entities = entities
        self.game_state.game_level = new_level
        self.game_state.add_explored_level(new_level)

        self.renderer.add_message(f"Welcome to dungeon level {new_level}!")
