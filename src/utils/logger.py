"""
Logging utility for the game
Handles all logging operations with rotation
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """ロガーインスタンスを設定して返す"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # ログディレクトリの作成
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 古いログファイルを削除
        _cleanup_old_logs(log_dir)
            
        # ファイル名に日時を含める
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/roguelike_{timestamp}.log"
        
        # ローテーション付きファイルハンドラー
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=2  # 3件のログを保持（現在のファイル + 2つのバックアップ）
        )
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    return logger

def _cleanup_old_logs(log_dir: str, keep_count: int = 3) -> None:
    """古いログファイルを削除"""
    log_files = []
    for file in os.listdir(log_dir):
        if file.startswith("roguelike_") and file.endswith(".log"):
            full_path = os.path.join(log_dir, file)
            log_files.append((full_path, os.path.getmtime(full_path)))
    
    # 更新日時でソート
    log_files.sort(key=lambda x: x[1], reverse=True)
    
    # 古いファイルを削除
    for file_path, _ in log_files[keep_count:]:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting log file {file_path}: {e}") 