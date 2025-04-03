import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from game.game_logic import check_tile_placement, update_game_state

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # States for dragging
        self.dragging = False
        self.selected_tile_index = None
        self.pinch_threshold = 0.05  # Distance threshold for pinch detection

    def process_frame(self, frame):
        """Process a camera frame and detect hand gestures."""
        if frame is None:
            return frame
            
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe Hands
        results = self.hands.process(rgb_frame)
        
        # Draw hand landmarks on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Get index finger and thumb coordinates
                index_finger_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]
                
                # Calculate distance between index finger and thumb
                distance = self.calculate_distance(index_finger_tip, thumb_tip)
                
                # Draw circle at index finger tip
                h, w, c = frame.shape
                index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
                
                # Check if fingers are pinched (close together)
                if distance < self.pinch_threshold:
                    # Pinch detected
                    cv2.putText(frame, "Pinch Detected", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Handle selection and dragging
                    self.handle_pinch_gesture(index_x, index_y)
                else:
                    # Release detected
                    if self.dragging:
                        # Handle tile placement
                        self.handle_tile_placement(index_x, index_y)
                        self.dragging = False
                        self.selected_tile_index = None
        
        return frame
    
    def calculate_distance(self, point1, point2):
        """Calculate normalized distance between two points."""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def handle_pinch_gesture(self, x, y):
        """Handle pinch gesture to select and drag tiles."""
        # If not already dragging, check if a tile is selected
        if not self.dragging:
            # Convert screen coordinates to normalized coordinates (0-1)
            norm_x = x / 640  # Assuming camera width is 640
            norm_y = y / 480  # Assuming camera height is 480
            
            # Check if the pinch is on a tile
            self.selected_tile_index = self.check_tile_selection(norm_x, norm_y)
            
            if self.selected_tile_index is not None:
                self.dragging = True
                st.session_state.selected_tile = self.selected_tile_index
    
    def check_tile_selection(self, norm_x, norm_y):
        """Check if a tile is selected based on normalized coordinates."""
        # This is a simplified version - in a real app, you'd map the
        # coordinates to the specific UI elements in Streamlit
        
        # For demonstration, let's assume tiles are in the right 30% of the screen
        # and evenly distributed vertically
        if norm_x > 0.7:
            if st.session_state.shuffled_tiles:
                visible_tiles = [i for i, tile in enumerate(st.session_state.shuffled_tiles) 
                               if tile['visible']]
                
                if visible_tiles:
                    # Divide the right area into sections based on number of visible tiles
                    section_height = 1.0 / len(visible_tiles)
                    
                    for i, tile_idx in enumerate(visible_tiles):
                        section_start = i * section_height
                        section_end = (i + 1) * section_height
                        
                        if section_start <= norm_y < section_end:
                            return tile_idx
        
        return None
    
    def handle_tile_placement(self, x, y):
        """Handle tile placement when pinch is released."""
        if self.selected_tile_index is not None:
            # Convert screen coordinates to normalized coordinates
            norm_x = x / 640
            norm_y = y / 480
            
            # Check which puzzle position this corresponds to
            position = self.check_puzzle_position(norm_x, norm_y)
            
            if position is not None and position in st.session_state.missing_positions:
                # Check if tile placement is correct
                correct = check_tile_placement(self.selected_tile_index, position)
                
                # Update game state
                update_game_state(self.selected_tile_index, position, correct)
    
    def check_puzzle_position(self, norm_x, norm_y):
        """Check which puzzle position corresponds to the given coordinates."""
        # Assuming puzzle is in the left 70% of the screen
        if norm_x < 0.7:
            grid_size = int(st.session_state.game_mode.split('x')[0])
            
            # Calculate grid cell
            grid_width = 0.7 / grid_size  # Width of each grid cell
            grid_height = 1.0 / grid_size  # Height of each grid cell
            
            # Calculate grid position
            grid_x = int(norm_x / grid_width)
            grid_y = int(norm_y / grid_height)
            
            # Convert to linear position
            position = grid_y * grid_size + grid_x
            
            # Make sure it's a valid position
            if 0 <= position < grid_size * grid_size:
                return position
        
        return None

def start_camera():
    """Initialize and start the camera for hand tracking."""
    # Create a placeholder for the camera feed
    camera_placeholder = st.empty()
    
    # Initialize hand tracker
    tracker = HandTracker()
    
    # Start webcam
    cap = cv2.VideoCapture(0)
    
    # Make sure the camera is opened correctly
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # If game is still active, process frames
    if not st.session_state.game_over:
        try:
            # Read a frame to ensure camera is working
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Could not read from webcam.")
                cap.release()
                return
                
            # Process the frame with hand tracker
            processed_frame = tracker.process_frame(frame)
            
            # Display the frame
            camera_placeholder.image(processed_frame, channels="BGR", use_column_width=True)
            
        except Exception as e:
            st.error(f"Error processing webcam feed: {e}")
            cap.release()