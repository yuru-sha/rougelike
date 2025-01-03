#!/usr/bin/env python3
import logging
import os
import glob
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name: str) -> logging.Logger:
    """各コンポーネント用のロガーを設定"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ログディレクトリがなければ作成
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 古いログファイルを削除（最新5件を残す）
    _cleanup_old_logs()

    # ファイル出力用ハンドラ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/roguelike_{timestamp}.log"
    fh = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"  # 10MB
    )
    fh.setLevel(logging.DEBUG)

    # コンソール出力用ハンドラ
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # フォーマッタを作成
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # ハンドラをロガーに追加
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def _cleanup_old_logs() -> None:
    """古いログファイルを削除（最新5件を残す）"""
    pattern = "logs/roguelike_*.log"
    files = glob.glob(pattern)
    if len(files) > 5:
        # タイムスタンプでソート
        files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        # 古いファイルを削除
        for file in files[5:]:
            try:
                os.remove(file)
            except OSError:
                pass
