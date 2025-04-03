# Puzzle Tiles Game

A fun and interactive puzzle game built with Streamlit and OpenCV. Select puzzle difficulty, solve puzzles using hand gestures via MediaPipe hand tracking, and challenge yourself to place missing tiles correctly!

## Overview

This game randomly selects images and divides them into tiles (8x8, 16x16, or 24x24). Several tiles are removed, transformed (rotated/flipped), and shuffled to the side. Your task is to use hand gestures to select and place these tiles in their correct positions to complete the image.

## Features

- **Multiple Difficulty Levels**: Choose between 8x8, 16x16, or 24x24 grid sizes
- **Hand Gesture Controls**: Use intuitive hand movements to interact with the game
  - Pinch your index finger and thumb together to select and move tiles
- **Interactive Feedback**: 
  - Correct placements turn green and stay in place
  - Incorrect placements turn red and return to the shuffled area
- **Visual Celebrations**: Enjoy balloon animations upon puzzle completion
- **Score Tracking**: Monitor your progress with a scoring system

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Anidipta/TrainIT.git
   cd TrainIT/pixel_play
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## Requirements

- Python 3.7+
- Webcam for hand tracking
- Dependencies listed in `requirements.txt`:
  - streamlit
  - opencv-python
  - mediapipe
  - numpy
  - pillow

## How to Play

1. Launch the game and allow webcam access
2. Select your desired grid size (8x8, 16x16, or 24x24)
3. A random image will be divided into tiles with some removed
4. Use hand gestures to move tiles:
   - Bring your index finger and thumb together to "pinch" a tile
   - Move your hand to drag the selected tile
   - Release the pinch to place the tile
5. Complete the puzzle by placing all tiles correctly

## Project Structure

```
puzzle_game/
│
├── app.py                   # Main Streamlit application
├── requirements.txt         # Dependencies for the project
│
├── assets/
│   ├── images/              # Store puzzle images here
│   ├── sounds/              # Store game sounds here
│   └── styles/              # CSS styles for the application
│
├── components/
│   ├── __init__.py
│   ├── game_ui.py           # UI components for the game
│   ├── image_processor.py   # Functions for image processing
│   └── hand_tracker.py      # MediaPipe hand tracking functionality
│
├── game/
│   ├── __init__.py
│   ├── game_logic.py        # Core game mechanics
│   ├── puzzle_generator.py  # Generate puzzles from images
│   └── score_manager.py     # Handle scoring and game progress
│
└── utils/
    ├── __init__.py
    ├── config.py            # Configuration settings
    └── helpers.py           # Helper functions
```

## Adding Custom Images

To add your own puzzle images:
1. Place image files in the `assets/images/` directory
2. Supported formats: JPG, PNG
3. For best results, use square images of at least 800x800 pixels

## Troubleshooting

- **Camera Not Detected**: Ensure your webcam is properly connected and not in use by another application
- **Hand Tracking Issues**: Make sure your hands are clearly visible in good lighting
- **Performance Issues**: Try using a lower grid size for better performance on slow