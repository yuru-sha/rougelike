import logging
import shutil
from datetime import datetime
from pathlib import Path
from unittest import TestCase, main

from src.utils.logger import setup_logger, cleanup_old_logs


class TestLogger(TestCase):
    def setUp(self):
        """テスト実行前の準備"""
        self.test_log_dir = Path("test_logs")
        self.test_log_dir.mkdir(exist_ok=True)
    
    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        if self.test_log_dir.exists():
            shutil.rmtree(self.test_log_dir)
    
    def test_logger_creation(self):
        """ロガーが正しく作成されることをテスト"""
        logger = setup_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_logger")
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertEqual(len(logger.handlers), 2)  # コンソールとファイルの2つのハンドラー
    
    def test_logger_singleton(self):
        """同じ名前のロガーが再利用されることをテスト"""
        logger1 = setup_logger("test_singleton")
        handlers_count = len(logger1.handlers)
        logger2 = setup_logger("test_singleton")
        self.assertEqual(logger1, logger2)
        self.assertEqual(len(logger2.handlers), handlers_count)
    
    def test_cleanup_old_logs(self):
        """古いログファイルが正しく削除されることをテスト"""
        # テスト用のログファイルを作成
        test_files = []
        for i in range(7):
            timestamp = datetime.now().strftime(f"%Y%m%d_%H%M%S_{i}")
            log_file = self.test_log_dir / f"roguelike_{timestamp}.log"
            log_file.touch()
            test_files.append(log_file)
        
        # 5ファイルだけ残すようにクリーンアップ
        cleanup_old_logs(self.test_log_dir, "roguelike_", keep_files=5)
        
        # 残っているファイル数を確認
        remaining_files = list(self.test_log_dir.glob("roguelike_*.log"))
        self.assertEqual(len(remaining_files), 5)
        
        # 最新の5ファイルが残っていることを確認
        for file in test_files[-5:]:
            self.assertTrue(file.exists())
        
        # 古い2ファイルが削除されていることを確認
        for file in test_files[:2]:
            self.assertFalse(file.exists())


if __name__ == "__main__":
    main() 