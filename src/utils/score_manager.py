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
    def __init__(self, scores_file: str = "scores.json"):
        self.scores_file = os.path.join("data", scores_file)
        self._ensure_data_dir()
        self.high_scores = self._load_scores()
        
    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.scores_file), exist_ok=True)
    
    def _load_scores(self) -> List[Dict]:
        """Load scores from file"""
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading scores: {e}")
            return []
    
    def _save_scores(self) -> None:
        """Save scores to file"""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving scores: {e}")
    
    def add_score(self, name: str, score: int, gold: int, level: int, depth: int) -> int:
        """Add new score and return ranking position"""
        new_score = {
            'name': name,
            'score': score,
            'gold': gold,
            'level': level,
            'depth': depth,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Binary search for insertion position
        position = self._find_insertion_position(score)
        
        # Insert score and maintain top 10
        self.high_scores.insert(position, new_score)
        self.high_scores = self.high_scores[:10]
        self._save_scores()
        
        return position + 1

    def _find_insertion_position(self, score: int) -> int:
        """Binary search for score insertion position"""
        left, right = 0, len(self.high_scores)
        
        while left < right:
            mid = (left + right) // 2
            if self.high_scores[mid]['score'] < score:
                right = mid
            else:
                left = mid + 1
                
        return left

    def get_high_scores(self) -> List[Dict]:
        """Get list of high scores"""
        return self.high_scores 