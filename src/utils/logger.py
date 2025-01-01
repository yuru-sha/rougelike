"""
Logging utility for the game
Handles all logging operations with rotation
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory if not exists
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Clean up old log files
        _cleanup_old_logs(log_dir)
            
        # Include timestamp in filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/roguelike_{timestamp}.log"
        
        # Setup rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,  # 1MB per file
            backupCount=2  # Keep 3 files (current + 2 backups)
        )
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    return logger

def _cleanup_old_logs(log_dir: str, keep_count: int = 3) -> None:
    """
    Remove old log files, keeping only the most recent ones
    
    Args:
        log_dir: Directory containing log files
        keep_count: Number of recent files to keep
    """
    log_files = []
    for file in os.listdir(log_dir):
        if file.startswith("roguelike_") and file.endswith(".log"):
            full_path = os.path.join(log_dir, file)
            log_files.append((full_path, os.path.getmtime(full_path)))
    
    # Sort by modification time
    log_files.sort(key=lambda x: x[1], reverse=True)
    
    # Remove old files
    for file_path, _ in log_files[keep_count:]:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting log file {file_path}: {e}") 