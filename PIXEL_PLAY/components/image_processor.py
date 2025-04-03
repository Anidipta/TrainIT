import cv2
import numpy as np
import random
from PIL import Image

def load_and_resize_image(image_path, target_size=(800, 800)):
    """Load an image and resize it to the target size."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")
    
    # Resize image while maintaining aspect ratio
    h, w = img.shape[:2]
    target_w, target_h = target_size
    
    # Calculate new dimensions
    ratio = min(target_w / w, target_h / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    
    # Resize image
    resized_img = cv2.resize(img, (new_w, new_h))
    
    # Create a black canvas of target size
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    
    # Calculate position to center the image
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    
    # Place the resized image on the canvas
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_img
    
    return canvas

def split_image_into_tiles(img, grid_size):
    """Split an image into a grid of tiles."""
    h, w = img.shape[:2]
    tile_h, tile_w = h // grid_size, w // grid_size
    
    tiles = []
    positions = []
    
    for i in range(grid_size):
        for j in range(grid_size):
            y1, y2 = i * tile_h, (i + 1) * tile_h
            x1, x2 = j * tile_w, (j + 1) * tile_w
            
            tile = img[y1:y2, x1:x2].copy()
            tiles.append(tile)
            positions.append(i * grid_size + j)
    
    return tiles, positions

def select_missing_tiles(positions, num_missing, grid_size):
    """Select random non-adjacent positions for missing tiles."""
    missing_positions = []
    
    while len(missing_positions) < num_missing:
        # Select a random position
        pos = random.choice(positions)
        
        # Check if this position is already selected
        if pos in missing_positions:
            continue
        
        # Check if any adjacent positions are already selected
        is_adjacent = False
        for mp in missing_positions:
            # Calculate row and column for both positions
            pos_row, pos_col = pos // grid_size, pos % grid_size
            mp_row, mp_col = mp // grid_size, mp % grid_size
            
            # Check if they're adjacent (horizontally, vertically, or diagonally)
            if abs(pos_row - mp_row) <= 1 and abs(pos_col - mp_col) <= 1:
                is_adjacent = True
                break
        
        if not is_adjacent:
            missing_positions.append(pos)
    
    return missing_positions

def transform_tile(tile):
    """Apply random transformation (rotation or flip) to a tile."""
    transformation = random.choice(['rotate_90', 'rotate_-90', 'flip_h', 'flip_v', 'none'])
    
    if transformation == 'rotate_90':
        return cv2.rotate(tile, cv2.ROTATE_90_CLOCKWISE)
    elif transformation == 'rotate_-90':
        return cv2.rotate(tile, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif transformation == 'flip_h':
        return cv2.flip(tile, 1)
    elif transformation == 'flip_v':
        return cv2.flip(tile, 0)
    else:
        return tile  # No transformation