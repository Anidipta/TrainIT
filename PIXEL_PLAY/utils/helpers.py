import os
import random
import cv2
import numpy as np
import streamlit as st

def ensure_assets_directory():
    """Ensure that all required asset directories exist."""
    directories = [
        os.path.join("assets"),
        os.path.join("assets", "images"),
        os.path.join("assets", "sounds"),
        os.path.join("assets", "styles")
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def create_sample_images():
    """Create sample images if none exist."""
    image_dir = os.path.join("assets", "images")
    if not any(file.lower().endswith(('.png', '.jpg', '.jpeg')) for file in os.listdir(image_dir)):
        # Create simple sample images
        for i in range(5):
            # Create a colorful gradient image
            img = np.zeros((800, 800, 3), dtype=np.uint8)
            
            # Create different patterns for each sample image
            if i == 0:
                # Radial gradient
                for y in range(800):
                    for x in range(800):
                        distance = np.sqrt((x - 400)**2 + (y - 400)**2)
                        img[y, x, 0] = np.clip(int(255 - distance * 0.5), 0, 255)  # Blue
                        img[y, x, 1] = np.clip(int(distance * 0.5), 0, 255)        # Green
                        img[y, x, 2] = np.clip(int(128 + np.sin(distance * 0.05) * 127), 0, 255)  # Red
            elif i == 1:
                # Horizontal gradient with waves
                for y in range(800):
                    for x in range(800):
                        img[y, x, 0] = np.clip(int(x / 3), 0, 255)  # Blue
                        img[y, x, 1] = np.clip(int(255 - x / 3), 0, 255)  # Green
                        img[y, x, 2] = np.clip(int(128 + np.sin(y * 0.05) * 127), 0, 255)  # Red
            elif i == 2:
                # Checkerboard pattern
                check_size = 50
                for y in range(800):
                    for x in range(800):
                        if (x // check_size + y // check_size) % 2 == 0:
                            img[y, x] = [50, 50, 200]  # Dark blue
                        else:
                            img[y, x] = [200, 200, 50]  # Light yellow
            elif i == 3:
                # Spiral pattern
                for y in range(800):
                    for x in range(800):
                        dx, dy = x - 400, y - 400
                        angle = np.arctan2(dy, dx)
                        distance = np.sqrt(dx**2 + dy**2)
                        spiral = (angle + distance * 0.01) % (2 * np.pi) / (2 * np.pi)
                        img[y, x, 0] = int(spiral * 255)  # Blue
                        img[y, x, 1] = int((1 - spiral) * 255)  # Green
                        img[y, x, 2] = int(np.sin(spiral * np.pi) * 255)  # Red
            else:
                # Concentric circles
                for y in range(800):
                    for x in range(800):
                        distance = np.sqrt((x - 400)**2 + (y - 400)**2)
                        circle = int(distance) % 50
                        if circle < 25:
                            img[y, x] = [50, 150, 255]  # Light blue
                        else:
                            img[y, x] = [255, 150, 50]  # Orange
            
            # Save the image
            filename = os.path.join(image_dir, f"sample_image_{i+1}.jpg")
            cv2.imwrite(filename, img)

def create_default_css():
    """Create default CSS if it doesn't exist."""
    css_dir = os.path.join("assets", "styles")
    css_file = os.path.join(css_dir, "main.css")
    
    if not os.path.exists(css_file):
        # Create a basic CSS file
        css_content = """
        /* Main styles for Puzzle Tiles Game */

        /* Typography */
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Arial', sans-serif;
        }

        /* Game board styling */
        .stImage > img {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Button styling */
        .stButton > button {
            border-radius: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Sidebar styling */
        .css-1lcbmhc, .css-1d391kg {
            background-color: #f8f9fa;
        }

        /* Metrics styling */
        .css-50ug3q {
            font-weight: bold;
            font-size: 1.2em;
        }

        /* Game over screen */
        .game-over-container {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Tile styling */
        .tile {
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .tile:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        """
        
        with open(css_file, 'w') as f:
            f.write(css_content)

def initialize_application():
    """Initialize the application by setting up directories and assets."""
    ensure_assets_directory()
    create_sample_images()
    create_default_css()