"""
Score management system for Rogue
Handles saving and loading high scores
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class ScoreManager:
    """
    Manages high score persistence and retrieval
    
    Attributes:
        scores_file: Path to high scores JSON file
        max_scores: Maximum number of high scores to keep
    """
    def __init__(self, scores_file: str = "scores.json", max_scores: int = 10):
        self.scores_file = scores_file
        self.max_scores = max_scores
        self._ensure_scores_file()

    def add_score(
        self, 
        name: str, 
        score: int, 
        gold: int, 
        level: int, 
        depth: int,
        victory: bool = False
    ) -> int:
        """
        Add new score and return ranking position
        
        Args:
            name: Player name
            score: Total score
            gold: Gold collected
            level: Player level
            depth: Maximum dungeon depth reached
            victory: Whether player achieved victory
            
        Returns:
            int: Ranking position (1-based)
        """
        new_score = {
            'name': name,
            'score': score,
            'gold': gold,
            'level': level,
            'depth': depth,
            'victory': victory,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Binary search for insertion position
        position = self._find_insertion_position(score)
        
        # Insert score and maintain top scores
        scores = self._load_scores()
        scores.insert(position, new_score)
        scores = scores[:self.max_scores]
        
        self._save_scores(scores)
        logger.info(f"Added score: {score} by {name} (rank: {position + 1})")
        
        return position + 1

    def get_high_scores(self) -> List[Dict[str, Any]]:
        """
        Get list of high scores
        
        Returns:
            List[Dict]: List of score entries, sorted by score
        """
        return self._load_scores()

    def _ensure_scores_file(self) -> None:
        # Create scores file if it doesn't exist
        if not os.path.exists(self.scores_file):
            self._save_scores([])

    def _load_scores(self) -> List[Dict[str, Any]]:
        # Load scores from file
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error(f"Error loading scores from {self.scores_file}")
            return []

    def _save_scores(self, scores: List[Dict[str, Any]]) -> None:
        # Save scores to file
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(scores, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving scores to {self.scores_file}: {e}") 

    def _find_insertion_position(self, score: int) -> int:
        """
        Binary search for score insertion position
        
        Args:
            score: Score to insert
            
        Returns:
            int: Index where score should be inserted
        """
        scores = self._load_scores()
        left, right = 0, len(scores)
        
        while left < right:
            mid = (left + right) // 2
            if scores[mid]['score'] > score:  # 降順でソート
                left = mid + 1
            else:
                right = mid
                
        return left 