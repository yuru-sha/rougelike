"""
Score management system for Rogue
Handles saving and loading high scores
"""
import json
import os
from datetime import datetime
from typing import List, Dict
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

    def add_score(self, score: int, player_name: str) -> None:
        """
        Add a new high score entry
        
        Args:
            score: Player's final score
            player_name: Name of the player
        """
        scores = self._load_scores()
        
        # Create new score entry
        new_score = {
            'score': score,
            'player': player_name,
            'date': datetime.now().isoformat()
        }
        
        scores.append(new_score)
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top scores
        scores = scores[:self.max_scores]
        
        self._save_scores(scores)
        logger.info(f"Added new score: {score} by {player_name}")

    def get_high_scores(self) -> List[Dict]:
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

    def _load_scores(self) -> List[Dict]:
        # Load scores from file
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error(f"Error loading scores from {self.scores_file}")
            return []

    def _save_scores(self, scores: List[Dict]) -> None:
        # Save scores to file
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(scores, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving scores to {self.scores_file}: {e}") 