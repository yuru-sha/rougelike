# ローグライクゲーム

オリジナルのRogue（1980年代）にインスパイアされた、TCODライブラリを使用したPython実装のローグライクゲームです。

[English version here](README.md)

## 特徴

- TCODライブラリを使用したクラシックなASCIIベースのグラフィックス
- 自動生成されるダンジョン
- ターンベースの戦闘システム
- 様々なアイテムと装備
- FOVとトラッキング機能を持つモンスターAI
- クラシックなローグライクメカニクス（空腹度、インベントリ管理など）

## 必要条件

- Python 3.9以上
- TCODライブラリ
- その他の依存関係は`requirements.txt`に記載

## インストール方法

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/roguelike.git
cd roguelike
```

2. 仮想環境の作成（推奨）:
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

## プレイ方法

ゲームの起動:
```bash
python src/main.py
```

### 操作方法

- 矢印キーまたはhjkl: 移動
- g: アイテムを拾う
- i: インベントリを開く
- d: アイテムを落とす
- ESC: ゲーム終了
- ?: ヘルプ

## 開発

開発用の追加依存関係のインストール:
```bash
pip install -r requirements-dev.txt
```

テストの実行:
```bash
pytest
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細はLICENSEファイルを参照してください。

## 謝辞

- オリジナルのRogueゲーム制作者
- TCODライブラリ開発者
- Pythonコミュニティ
- Cursor - AIペアプログラミングアシスタント 