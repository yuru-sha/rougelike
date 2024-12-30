# Rogue like

## 概要
このプロジェクトは、1980年代の古典的ローグライクゲーム「Rogue」のPython実装です。オリジナルの仕様と動作を可能な限り忠実に再現しつつ、モダンなコード設計を採用しています。

## 特徴
- オリジナルRogueの忠実な再現
- 手続き的ダンジョン生成
- ターンベースの戦闘システム
- 伝統的なアスキーアート表示
- スコアシステムとランキング機能

## 技術スタック
- Python 3.8+
- blessed (ターミナル操作)
- injector (依存性注入)
- dataclasses (データモデル)

## インストール

```bash
git clone https://github.com/yuru-sha/roguelike.git
cd roguelike
pip install -r requirements.txt
```

## 実行方法

```bash
python src/main.py
```

## プロジェクト構造

```
src/
├── core/ # ゲームエンジンとコアロジック
├── entities/ # ゲーム内エンティティ
├── utils/ # ユーティリティ関数
└── constants/ # ゲーム定数
```

## ライセンス
MIT License
