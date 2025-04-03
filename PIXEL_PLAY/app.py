import streamlit as st
import os
from components.game_ui import create_sidebar, render_game_over, render_game_ui
from components.hand_tracker import start_camera
from game.game_logic import initialize_game, check_tile_placement, update_game_state
from game.puzzle_generator import get_available_images, create_puzzle
from utils.config import TITLE, INSTRUCTIONS, GAME_MODES

# Configure Streamlit page
st.set_page_config(
    page_title="Puzzle Tiles Game",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
with open(os.path.join("assets", "styles", "main.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state if not exists
    if "game_initialized" not in st.session_state:
        st.session_state.game_initialized = False
        st.session_state.game_over = False
        st.session_state.game_won = False
        st.session_state.selected_tile = None
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.game_mode = None
        st.session_state.puzzle_image = None
        st.session_state.puzzle_tiles = None
        st.session_state.missing_positions = None
        st.session_state.shuffled_tiles = None

    # Create sidebar UI
    create_sidebar()

    # Display title and instructions on first visit
    if not st.session_state.game_initialized:
        st.title(TITLE)
        st.markdown(INSTRUCTIONS)
        
        # Game mode selection
        mode_col1, mode_col2, mode_col3 = st.columns(3)
        with mode_col1:
            if st.button("8x8 Puzzle", use_container_width=True):
                st.session_state.game_mode = GAME_MODES[0]
                start_new_game()
        
        with mode_col2:
            if st.button("16x16 Puzzle", use_container_width=True):
                st.session_state.game_mode = GAME_MODES[1]
                start_new_game()
                
        with mode_col3:
            if st.button("24x24 Puzzle", use_container_width=True):
                st.session_state.game_mode = GAME_MODES[2]
                start_new_game()
    
    # Handle game over state
    elif st.session_state.game_over:
        render_game_over()
        
        # Restart button
        if st.button("Play Again"):
            reset_game()
    
    # Render active game
    else:
        render_game_ui()
        start_camera()

def start_new_game():
    # Get available images
    available_images = get_available_images()
    if not available_images:
        st.error("No images found in the assets/images directory!")
        return
    
    # Create puzzle based on selected mode
    mode = st.session_state.game_mode
    grid_size = int(mode.split('x')[0])
    
    # Determine number of missing tiles based on grid size
    if grid_size == 8:
        missing_tiles = 3
    elif grid_size == 16:
        missing_tiles = 7
    else:  # 24x24
        missing_tiles = 10
        
    # Initialize the game
    initialize_game(mode, missing_tiles)
    st.session_state.game_initialized = True

def reset_game():
    st.session_state.game_initialized = False
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.selected_tile = None
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.game_mode = None
    st.session_state.puzzle_image = None
    st.session_state.puzzle_tiles = None
    st.session_state.missing_positions = None
    st.session_state.shuffled_tiles = None
    st.rerun()

if __name__ == "__main__":
    main()