import logging
import sys
from datetime import datetime
from logging import FileHandler, StreamHandler
from pathlib import Path


def cleanup_old_logs(log_dir: Path, prefix: str, keep_files: int = 5) -> None:
    """
    古いログファイルを削除します。

    Args:
        log_dir (Path): ログディレクトリのパス
        prefix (str): ログファイルのプレフィックス
        keep_files (int): 保持するファイル数
    """
    log_files = sorted(
        [f for f in log_dir.glob(f"{prefix}*.log")],
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    for old_file in log_files[keep_files:]:
        old_file.unlink()


def setup_logger(name: str = "roguelike") -> logging.Logger:
    """
    ロガーの設定を行い、設定済みのロガーインスタンスを返します。

    Args:
        name (str): ロガーの名前。デフォルトは "roguelike"

    Returns:
        logging.Logger: 設定済みのロガーインスタンス
    """
    # ロガーの取得
    logger = logging.getLogger(name)

    # 既に設定済みの場合は、そのまま返す
    if logger.handlers:
        return logger

    # ログレベルの設定
    logger.setLevel(logging.DEBUG)

    # フォーマッターの作成
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # コンソール出力用ハンドラーの設定
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # フグディレクトリの設定
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 現在時刻を含むファイル名の生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"roguelike_{timestamp}.log"

    # ファイル出力用ハンドラーの設定
    file_handler = FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 古いログファイルの削除
    cleanup_old_logs(log_dir, "roguelike_")

    return logger


# デフォルトのロガーインスタンスを作成
logger = setup_logger()
