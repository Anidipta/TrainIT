import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
from game.game_logic import update_game_state, check_tile_placement

def create_sidebar():
    """Create the sidebar with game information and settings."""
    with st.sidebar:
        st.title("🧩 Puzzle Tiles Game")
        st.markdown("---")
        
        if st.session_state.game_initialized:
            st.subheader("Game Stats")
            st.metric("Score", st.session_state.score)
            st.metric("Attempts", st.session_state.attempts)
            st.metric("Game Mode", st.session_state.game_mode)
            
            # Reset game button
            if st.button("Restart Game"):
                st.session_state.game_initialized = False
                st.session_state.game_over = False
                st.session_state.game_won = False
                st.experimental_rerun()
        
        st.markdown("---")
        st.subheader("How to Play")
        st.markdown("""
        1. Select a missing tile with your index finger and thumb pinched together
        2. Drag the tile to its correct position in the puzzle
        3. Release to place the tile
        4. Complete the puzzle to win!
        """)

def render_game_over():
    """Render the game over screen."""
    if st.session_state.game_won:
        st.title("🎉 Congratulations! You solved the puzzle!")
        st.balloons()
        # Display completed image
        st.image(st.session_state.puzzle_image, caption="Completed Puzzle")
        
        # Display game stats
        st.subheader("Game Statistics")
        st.metric("Final Score", st.session_state.score)
        st.metric("Attempts", st.session_state.attempts)
        st.metric("Game Mode", st.session_state.game_mode)
    else:
        st.title("Game Over")
        st.write("Better luck next time!")

def render_game_ui():
    """Render the main game UI with puzzle and tiles."""
    st.title(f"Puzzle Game - {st.session_state.game_mode}")
    
    # Create two columns - one for puzzle and one for tiles
    puzzle_col, tiles_col = st.columns([0.7, 0.3])
    
    with puzzle_col:
        st.subheader("Puzzle Board")
        # Display current puzzle state
        if st.session_state.puzzle_image is not None:
            # Create a placeholder for the puzzle
            puzzle_placeholder = st.empty()
            
            # Display the puzzle with missing tiles
            puzzle_board = create_puzzle_board()
            puzzle_placeholder.image(puzzle_board, use_column_width=True)
    
    with tiles_col:
        st.subheader("Available Tiles")
        # Display shuffled tiles
        if st.session_state.shuffled_tiles is not None:
            tiles_container = st.container()
            with tiles_container:
                # Display each shuffled tile
                for i, tile in enumerate(st.session_state.shuffled_tiles):
                    if tile['visible']:  # Only show tiles that haven't been placed yet
                        tile_img = Image.fromarray(tile['image'])
                        st.image(tile_img, caption=f"Tile {i+1}", use_column_width=True)

def create_puzzle_board():
    """Create the current puzzle board image with missing tiles."""
    # Get puzzle dimensions
    grid_size = int(st.session_state.game_mode.split('x')[0])
    puzzle_img = st.session_state.puzzle_image.copy()
    
    # Create a mask for missing tiles
    for pos in st.session_state.missing_positions:
        if pos not in st.session_state.correct_placements:
            # Calculate tile position
            tile_height = puzzle_img.shape[0] // grid_size
            tile_width = puzzle_img.shape[1] // grid_size
            
            row, col = pos // grid_size, pos % grid_size
            y1, y2 = row * tile_height, (row + 1) * tile_height
            x1, x2 = col * tile_width, (col + 1) * tile_width
            
            # Draw a gray rectangle to represent missing tile
            cv2.rectangle(puzzle_img, (x1, y1), (x2, y2), (200, 200, 200), -1)
            cv2.rectangle(puzzle_img, (x1, y1), (x2, y2), (0, 0, 0), 2)
    
    return puzzle_img

def display_feedback(correct, tile_index, position):
    """Display feedback when a tile is placed."""
    grid_size = int(st.session_state.game_mode.split('x')[0])
    puzzle_img = st.session_state.puzzle_image.copy()
    
    # Calculate tile position
    tile_height = puzzle_img.shape[0] // grid_size
    tile_width = puzzle_img.shape[1] // grid_size
    
    row, col = position // grid_size, position % grid_size
    y1, y2 = row * tile_height, (row + 1) * tile_height
    x1, x2 = col * tile_width, (col + 1) * tile_width
    
    # Draw colored rectangle based on correctness
    color = (0, 255, 0) if correct else (0, 0, 255)  # Green for correct, Red for incorrect
    
    # Create a copy of the image with the feedback
    feedback_img = puzzle_img.copy()
    cv2.rectangle(feedback_img, (x1, y1), (x2, y2), color, -1)
    
    # Blend original tile with the color for a semi-transparent effect
    tile_img = st.session_state.shuffled_tiles[tile_index]['image']
    resized_tile = cv2.resize(tile_img, (x2-x1, y2-y1))
    
    alpha = 0.7
    feedback_img[y1:y2, x1:x2] = cv2.addWeighted(
        resized_tile, alpha,
        feedback_img[y1:y2, x1:x2], 1-alpha, 0
    )
    
    # Display feedback
    st.image(feedback_img, use_column_width=True)
    time.sleep(1)  # Show for 1 second