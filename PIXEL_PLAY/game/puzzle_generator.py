import os
import random
import cv2
import numpy as np
from components.image_processor import (
    load_and_resize_image, 
    split_image_into_tiles, 
    select_missing_tiles,
    transform_tile
)

def get_available_images():
    """Get a list of all available images in the assets directory."""
    image_dir = os.path.join("assets", "images")
    
    # Create directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        
    # Get all image files
    image_files = []
    for file in os.listdir(image_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(os.path.join(image_dir, file))
    
    return image_files

def get_random_image():
    """Get a random image from the available images."""
    images = get_available_images()
    if not images:
        raise FileNotFoundError("No images found in the assets/images directory.")
    
    return random.choice(images)

def create_puzzle(image_path, grid_size, num_missing_tiles):
    """Create a puzzle from the given image."""
    # Load and resize the image
    image = load_and_resize_image(image_path)
    
    # Split the image into tiles
    tiles, positions = split_image_into_tiles(image, grid_size)
    
    # Select positions for missing tiles
    missing_positions = select_missing_tiles(positions, num_missing_tiles, grid_size)
    
    # Create shuffled tiles for the user to place
    shuffled_tiles = []
    for pos in missing_positions:
        # Get the tile at this position
        tile = tiles[pos].copy()
        
        # Apply random transformation
        transformed_tile = transform_tile(tile)
        
        # Add to shuffled tiles
        shuffled_tiles.append({
            'image': transformed_tile,
            'original_position': pos,
            'visible': True,
            'transformation': 'random'  # For demonstration purposes
        })
    
    # Shuffle the tiles to randomize their order
    random.shuffle(shuffled_tiles)
    
    return image, tiles, missing_positions, shuffled_tiles