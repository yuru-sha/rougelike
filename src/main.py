#!/usr/bin/env python3
import tcod
from typing import Optional, Set, Tuple, List
import random

# ゲームの設定
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

TITLE = "Roguelike Game"

class Tile:
    """マップタイル。通行可能かどうかを管理する。"""
    def __init__(self, walkable: bool, transparent: bool):
        self.walkable = walkable
        self.transparent = transparent

class Rectangle:
    """部屋を表す矩形"""
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y
    
    def intersects(self, other: "Rectangle") -> bool:
        """この部屋が他の部屋と重なっているかどうかを判定"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
    
    def initialize_tiles(self) -> List[List[Tile]]:
        """マップを壁で初期化"""
        tiles = [[Tile(walkable=False, transparent=False)
                 for y in range(self.height)]
                for x in range(self.width)]
        return tiles
    
    def in_bounds(self, x: int, y: int) -> bool:
        """指定された座標がマップの範囲内かどうかを判定"""
        return 0 <= x < self.width and 0 <= y < self.height

    def create_room(self, room: Rectangle) -> None:
        """部屋を作成"""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].walkable = True
                self.tiles[x][y].transparent = True
    
    def create_h_tunnel(self, x1: int, x2: int, y: int) -> None:
        """水平方向の通路を作成"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True
    
    def create_v_tunnel(self, y1: int, y2: int, x: int) -> None:
        """垂直方向の通路を作成"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True

    def make_map(self) -> Tuple[int, int]:
        """ダンジョンを生成し、プレイヤーの開始位置を返す"""
        rooms: List[Rectangle] = []
        player_x = 0
        player_y = 0

        for r in range(MAX_ROOMS):
            # ランダムな部屋のサイズと位置を決定
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)
            
            new_room = Rectangle(x, y, w, h)
            
            # 他の部屋と重なっていないか確認
            for other_room in rooms:
                if new_room.intersects(other_room):
                    break
            else:  # 重なっていない場合
                # 部屋を作成
                self.create_room(new_room)
                
                # 部屋の中心座標を取得
                new_x, new_y = new_room.center
                
                if len(rooms) == 0:
                    # 最初の部屋の場合、プレイヤーの開始位置とする
                    player_x, player_y = new_x, new_y
                else:
                    # 前の部屋と通路でつなぐ
                    prev_x, prev_y = rooms[-1].center
                    
                    # 50%の確率で水平→垂直か垂直→水平を選択
                    if random.random() < 0.5:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                
                rooms.append(new_room)
        
        return player_x, player_y

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int, game_map: GameMap) -> None:
        """移動先が通行可能な場合のみ移動"""
        if game_map.tiles[self.x + dx][self.y + dy].walkable:
            self.x += dx
            self.y += dy

def handle_input(event: tcod.event.Event, player: Player, game_map: GameMap) -> Optional[bool]:
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
            player.move(dx, dy, game_map)
        elif event.sym == tcod.event.KeySym.ESCAPE:
            return True
    
    return None

def main():
    # フォントの設定
    tileset = tcod.tileset.load_tilesheet(
        "assets/fonts/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # マップを生成
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    player_x, player_y = game_map.make_map()
    player = Player(player_x, player_y)

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
            
            # マップの描画
            for x in range(game_map.width):
                for y in range(game_map.height):
                    if game_map.tiles[x][y].walkable:
                        root_console.print(x=x, y=y, string=".")
                    else:
                        root_console.print(x=x, y=y, string="#")
            
            # プレイヤーの描画
            root_console.print(x=player.x, y=player.y, string="@")
            
            # 画面の更新
            context.present(root_console)
            
            # イベント処理
            for event in tcod.event.wait():
                if handle_input(event, player, game_map):
                    raise SystemExit()

if __name__ == "__main__":
    main()
