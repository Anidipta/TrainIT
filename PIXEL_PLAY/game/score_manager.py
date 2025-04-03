import streamlit as st
import time
import json
import os
from utils.config import SCORING

class ScoreManager:
    def __init__(self):
        self.scores_file = os.path.join("assets", "scores.json")
        self.ensure_scores_file()
    
    def ensure_scores_file(self):
        """Ensure the scores file exists."""
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump({"8x8": [], "16x16": [], "24x24": []}, f)
    
    def load_scores(self):
        """Load scores from the scores file."""
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or doesn't exist, create a new one
            self.ensure_scores_file()
            return {"8x8": [], "16x16": [], "24x24": []}
    
    def save_score(self, player_name, score, attempts, time_taken, game_mode):
        """Save a player's score."""
        scores = self.load_scores()
        
        # Add new score
        new_score = {
            "player": player_name,
            "score": score,
            "attempts": attempts,
            "time": time_taken,
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        scores[game_mode].append(new_score)
        
        # Sort scores (highest first)
        scores[game_mode] = sorted(scores[game_mode], key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10 scores
        scores[game_mode] = scores[game_mode][:10]
        
        # Save scores
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f)
    
    def get_top_scores(self, game_mode, limit=10):
        """Get top scores for a given game mode."""
        scores = self.load_scores()
        return scores.get(game_mode, [])[:limit]
    
    def calculate_final_score(self, base_score, attempts, time_taken, time_limit=None):
        """Calculate final score based on base score, attempts, and time."""
        # Base score
        final_score = base_score
        
        # Penalty for attempts
        attempt_penalty = max(0, attempts - 1) * 5  # 5 points per additional attempt
        final_score -= attempt_penalty
        
        # Time bonus if time limit is enabled
        if time_limit is not None:
            time_remaining = max(0, time_limit - time_taken)
            time_bonus = time_remaining * SCORING["time_bonus"]
            final_score += time_bonus
        
        # Add completion bonus
        final_score += SCORING["completion_bonus"]
        
        return max(0, final_score)  # Ensure score is not negative