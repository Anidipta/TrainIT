import streamlit as st
import random
from game.puzzle_generator import get_random_image, create_puzzle

def initialize_game(game_mode, num_missing_tiles):
    """Initialize a new game with the selected mode."""
    # Get grid size from game mode (e.g., "8x8", "16x16", "24x24")
    grid_size = int(game_mode.split('x')[0])
    
    # Choose a random image and create the puzzle
    image_path = get_random_image()
    puzzle_img, puzzle_tiles, missing_positions, shuffled_tiles = create_puzzle(
        image_path, grid_size, num_missing_tiles
    )
    
    # Store game state in session state
    st.session_state.puzzle_image = puzzle_img
    st.session_state.puzzle_tiles = puzzle_tiles
    st.session_state.missing_positions = missing_positions
    st.session_state.shuffled_tiles = shuffled_tiles
    st.session_state.correct_placements = {}  # Map of correctly placed tiles
    
    # Reset game stats
    st.session_state.score = 0
    st.session_state.attempts = 0
    
    # Game is now initialized
    st.session_state.game_initialized = True
    st.session_state.game_over = False
    st.session_state.game_won = False

def check_tile_placement(tile_index, position):
    """Check if a tile is correctly placed."""
    # Get the original position of the tile
    original_position = st.session_state.shuffled_tiles[tile_index]['original_position']
    
    # Check if this is the correct position
    return original_position == position

def update_game_state(tile_index, position, correct):
    """Update the game state after a tile placement."""
    # Increment attempts
    st.session_state.attempts += 1
    
    if correct:
        # Update score
        st.session_state.score += 100
        
        # Mark tile as correctly placed
        st.session_state.correct_placements[position] = tile_index
        
        # Hide tile from shuffled tiles
        st.session_state.shuffled_tiles[tile_index]['visible'] = False
        
        # Check if all tiles are placed correctly
        if len(st.session_state.correct_placements) == len(st.session_state.missing_positions):
            # Game completed
            st.session_state.game_over = True
            st.session_state.game_won = True
    else:
        # Incorrect placement, penalize score
        st.session_state.score = max(0, st.session_state.score - 10)