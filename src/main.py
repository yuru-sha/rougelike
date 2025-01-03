#!/usr/bin/env python3
import tcod
from typing import Optional

# ゲームの設定
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
TITLE = "Roguelike Game"

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

def handle_input(event: tcod.event.Event, player: Player) -> Optional[bool]:
    """キー入力を処理する。Trueを返すとゲームを終了する。"""
    if event.type == "QUIT":
        return True
        
    if event.type == "KEYDOWN":
        # 移動キーの設定
        if event.sym in {
            # 矢印キー
            tcod.event.KeySym.UP: (0, -1),
            tcod.event.KeySym.DOWN: (0, 1),
            tcod.event.KeySym.LEFT: (-1, 0),
            tcod.event.KeySym.RIGHT: (1, 0),
            # viキーバインド
            tcod.event.KeySym.k: (0, -1),  # 上
            tcod.event.KeySym.j: (0, 1),   # 下
            tcod.event.KeySym.h: (-1, 0),  # 左
            tcod.event.KeySym.l: (1, 0),   # 右
            # 斜め移動
            tcod.event.KeySym.y: (-1, -1), # 左上
            tcod.event.KeySym.u: (1, -1),  # 右上
            tcod.event.KeySym.b: (-1, 1),  # 左下
            tcod.event.KeySym.n: (1, 1),   # 右下
        }.keys():
            dx, dy = {
                # 矢印キー
                tcod.event.KeySym.UP: (0, -1),
                tcod.event.KeySym.DOWN: (0, 1),
                tcod.event.KeySym.LEFT: (-1, 0),
                tcod.event.KeySym.RIGHT: (1, 0),
                # viキーバインド
                tcod.event.KeySym.k: (0, -1),  # 上
                tcod.event.KeySym.j: (0, 1),   # 下
                tcod.event.KeySym.h: (-1, 0),  # 左
                tcod.event.KeySym.l: (1, 0),   # 右
                # 斜め移動
                tcod.event.KeySym.y: (-1, -1), # 左上
                tcod.event.KeySym.u: (1, -1),  # 右上
                tcod.event.KeySym.b: (-1, 1),  # 左下
                tcod.event.KeySym.n: (1, 1),   # 右下
            }[event.sym]
            player.move(dx, dy)
        elif event.sym == tcod.event.KeySym.ESCAPE:
            return True
    
    return None

def main():
    # フォントの設定
    tileset = tcod.tileset.load_tilesheet(
        "assets/fonts/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # プレイヤーを中央に配置

    # コンソールの初期化
    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title=TITLE,
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        
        while True:
            root_console.clear()
            
            # プレイヤーの描画
            root_console.print(x=player.x, y=player.y, string="@")
            
            # 画面の更新
            context.present(root_console)
            
            # イベント処理
            for event in tcod.event.wait():
                if handle_input(event, player):
                    raise SystemExit()

if __name__ == "__main__":
    main()
