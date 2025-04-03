# Game modes available
GAME_MODES = ["8x8", "16x16", "24x24"]

# Game title
TITLE = "🧩 Puzzle Tiles Game"

# Game instructions
INSTRUCTIONS = """
## Welcome to Puzzle Tiles!

In this game, you'll solve a puzzle by placing missing tiles back in their correct positions.

### How to Play:
1. Select a game mode below to start
2. Use your index finger and thumb (pinched together) to select and move tiles
3. Place the tiles in the correct positions to complete the puzzle
4. Get feedback on your placements (green for correct, red for incorrect)
5. Complete the puzzle to win!

### Game Modes:
- **8x8**: Easy mode with 3 missing tiles
- **16x16**: Medium mode with 7 missing tiles
- **24x24**: Hard mode with 10 missing tiles

Select a mode below to begin:
"""

# Feedback messages
FEEDBACK = {
    "correct": "Great job! That's the correct placement.",
    "incorrect": "Not quite right. Try again!",
    "win": "Congratulations! You've completed the puzzle!",
}

# Camera configuration
CAMERA_CONFIG = {
    "width": 640,
    "height": 480,
    "fps": 30
}

# Hand tracking configuration
HAND_TRACKING = {
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
    "max_num_hands": 1,
    "pinch_threshold": 0.05  # Distance threshold for pinch detection
}

# Scoring configuration
SCORING = {
    "correct_placement": 100,  # Points for correct placement
    "incorrect_placement": -10,  # Penalty for incorrect placement
    "completion_bonus": 500,  # Bonus for completing the puzzle
    "time_bonus": 10  # Points per second remaining (if time limit is enabled)
}