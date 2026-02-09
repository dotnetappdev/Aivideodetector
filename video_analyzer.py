"""
AI Video Detector - Video Analysis Module
Analyzes video files to detect and analyze human subjects including:
- Height estimation
- Hair color detection
- Eye color detection
- Clothing color detection
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat


class VideoAnalyzer:
    """Main class for analyzing video files and detecting human attributes."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the video analyzer with MediaPipe models.
        
        Args:
            model_path: Optional path to the pose landmarker model file.
                       If not provided, will use default location or download it.
        """
        # Get model path
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "models", "pose_landmarker_lite.task")
        
        # Check if model exists, if not download it
        if not os.path.exists(model_path):
            print(f"Model not found at {model_path}")
            print("Attempting to download model...")
            self._download_model(model_path)
        
        # Initialize MediaPipe Pose Landmarker for person detection and height estimation
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.pose_landmarker = vision.PoseLandmarker.create_from_options(options)
        
        # Store landmark connections for drawing
        self.pose_connections = vision.PoseLandmarksConnections.POSE_CONNECTIONS
        
        # Reference height for calibration (in cm)
        self.reference_height_cm = 170.0
        
        # Frame counter for video processing
        self.frame_timestamp_ms = 0
    
    def _download_model(self, model_path: str):
        """Download the pose landmarker model if it doesn't exist."""
        import urllib.request
        
        model_url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
        
        try:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            print(f"Downloading model from {model_url}...")
            urllib.request.urlretrieve(model_url, model_path)
            print(f"Model downloaded successfully to {model_path}")
        except Exception as e:
            print(f"\nError downloading model: {e}")
            print("\n" + "=" * 70)
            print("MODEL DOWNLOAD REQUIRED")
            print("=" * 70)
            print("\nThe MediaPipe Pose Landmarker model could not be downloaded automatically.")
            print("Please download it manually using one of these methods:\n")
            print("Method 1 - Download script:")
            print("  python download_models.py\n")
            print("Method 2 - Browser download:")
            print("  1. Open this URL in your browser:")
            print(f"     {model_url}")
            print("  2. Save the file as:")
            print(f"     {model_path}\n")
            print("Method 3 - Command line (if available):")
            print(f"  mkdir -p {os.path.dirname(model_path)}")
            print(f"  # Download using your browser, then move file to models/\n")
            print("=" * 70)
            raise RuntimeError(f"Failed to download model. Please download manually (see instructions above).")
        
    def open_video(self, video_path: str) -> cv2.VideoCapture:
        """
        Open a video file for processing.
        
        Args:
            video_path: Path to the video file (supports MP4, MKV, AVI, etc.)
            
        Returns:
            OpenCV VideoCapture object
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video file cannot be opened
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        return cap
    
    def estimate_height(self, pose_landmarks_list: List, image_height: int) -> float:
        """
        Estimate the height of a person from pose landmarks.
        
        Args:
            pose_landmarks_list: List of pose landmarks from MediaPipe
            image_height: Height of the image in pixels
            
        Returns:
            Estimated height in centimeters
        """
        if not pose_landmarks_list or len(pose_landmarks_list) == 0:
            return 0.0
        
        # Get first person's landmarks
        landmarks = pose_landmarks_list[0]
        
        # Get key points for height calculation
        # Use nose (0) to ankle (27, 28)
        nose = landmarks[0]  # PoseLandmark.NOSE
        left_ankle = landmarks[27]  # PoseLandmark.LEFT_ANKLE
        right_ankle = landmarks[28]  # PoseLandmark.RIGHT_ANKLE
        
        # Calculate pixel height
        head_y = nose.y * image_height
        foot_y = max(left_ankle.y, right_ankle.y) * image_height
        pixel_height = abs(foot_y - head_y)
        
        # Estimate actual height (simplified calibration)
        # Assumes average person height as reference
        estimated_height = (pixel_height / image_height) * self.reference_height_cm * 1.2
        
        return estimated_height
    
    def detect_hair_color(self, image: np.ndarray, pose_landmarks_list: List) -> str:
        """
        Detect the dominant hair color from the head region.
        
        Args:
            image: Input image
            pose_landmarks_list: List of pose landmarks from MediaPipe
            
        Returns:
            Detected hair color as string
        """
        if not pose_landmarks_list or len(pose_landmarks_list) == 0:
            return "Unknown"
        
        landmarks = pose_landmarks_list[0]
        h, w = image.shape[:2]
        
        # Get head region (nose)
        nose = landmarks[0]  # PoseLandmark.NOSE
        
        # Define region above nose for hair
        x = int(nose.x * w)
        y = int(nose.y * h)
        
        # Extract hair region (above the nose)
        hair_region_top = max(0, y - 80)
        hair_region_bottom = max(0, y - 20)
        hair_region_left = max(0, x - 40)
        hair_region_right = min(w, x + 40)
        
        if hair_region_top >= hair_region_bottom or hair_region_left >= hair_region_right:
            return "Unknown"
        
        hair_region = image[hair_region_top:hair_region_bottom, 
                           hair_region_left:hair_region_right]
        
        if hair_region.size == 0:
            return "Unknown"
        
        # Calculate average color
        avg_color = np.mean(hair_region, axis=(0, 1)).astype(int)
        
        return self._classify_color(avg_color, color_type="hair")
    
    def detect_eye_color(self, image: np.ndarray, pose_landmarks_list: List) -> str:
        """
        Detect the eye color from facial landmarks.
        
        Args:
            image: Input image
            pose_landmarks_list: List of pose landmarks from MediaPipe
            
        Returns:
            Detected eye color as string
        """
        if not pose_landmarks_list or len(pose_landmarks_list) == 0:
            return "Unknown"
        
        landmarks = pose_landmarks_list[0]
        h, w = image.shape[:2]
        
        # Get eye positions
        left_eye = landmarks[2]  # PoseLandmark.LEFT_EYE
        right_eye = landmarks[5]  # PoseLandmark.RIGHT_EYE
        
        # Extract eye regions
        eye_colors = []
        for eye in [left_eye, right_eye]:
            x = int(eye.x * w)
            y = int(eye.y * h)
            
            # Small region around eye
            eye_region_size = 10
            y1 = max(0, y - eye_region_size)
            y2 = min(h, y + eye_region_size)
            x1 = max(0, x - eye_region_size)
            x2 = min(w, x + eye_region_size)
            
            if y1 < y2 and x1 < x2:
                eye_region = image[y1:y2, x1:x2]
                if eye_region.size > 0:
                    avg_color = np.mean(eye_region, axis=(0, 1)).astype(int)
                    eye_colors.append(avg_color)
        
        if not eye_colors:
            return "Unknown"
        
        avg_eye_color = np.mean(eye_colors, axis=0).astype(int)
        return self._classify_color(avg_eye_color, color_type="eye")
    
    def detect_clothing_colors(self, image: np.ndarray, pose_landmarks_list: List) -> List[str]:
        """
        Detect the dominant clothing colors.
        
        Args:
            image: Input image
            pose_landmarks_list: List of pose landmarks from MediaPipe
            
        Returns:
            List of detected clothing colors
        """
        if not pose_landmarks_list or len(pose_landmarks_list) == 0:
            return ["Unknown"]
        
        landmarks = pose_landmarks_list[0]
        h, w = image.shape[:2]
        
        # Get torso region (shoulders to hips)
        left_shoulder = landmarks[11]  # PoseLandmark.LEFT_SHOULDER
        right_shoulder = landmarks[12]  # PoseLandmark.RIGHT_SHOULDER
        left_hip = landmarks[23]  # PoseLandmark.LEFT_HIP
        right_hip = landmarks[24]  # PoseLandmark.RIGHT_HIP
        
        # Define torso region
        x1 = int(min(left_shoulder.x, left_hip.x) * w)
        x2 = int(max(right_shoulder.x, right_hip.x) * w)
        y1 = int(left_shoulder.y * h)
        y2 = int(left_hip.y * h)
        
        # Ensure valid region
        x1 = max(0, x1)
        x2 = min(w, x2)
        y1 = max(0, y1)
        y2 = min(h, y2)
        
        if x1 >= x2 or y1 >= y2:
            return ["Unknown"]
        
        torso_region = image[y1:y2, x1:x2]
        
        if torso_region.size == 0:
            return ["Unknown"]
        
        # Find dominant colors in clothing
        colors = self._find_dominant_colors(torso_region, n_colors=2)
        return colors
    
    def _classify_color(self, bgr_color: np.ndarray, color_type: str = "general") -> str:
        """
        Classify a BGR color into a named color category.
        
        Args:
            bgr_color: BGR color array [B, G, R]
            color_type: Type of color being classified ("hair", "eye", or "general")
            
        Returns:
            Color name as string
        """
        b, g, r = bgr_color
        
        # Convert to HSV for better color classification
        bgr_pixel = np.uint8([[[b, g, r]]])
        hsv = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = hsv
        
        # Classify based on HSV values
        if v < 50:
            return "Black"
        elif v > 200 and s < 30:
            return "White"
        elif s < 30:
            return "Gray"
        
        # Color classification based on hue
        if color_type == "hair":
            if h < 15 or h > 165:
                if v < 80:
                    return "Black"
                else:
                    return "Red/Auburn"
            elif h < 30:
                if v < 100:
                    return "Brown"
                else:
                    return "Blonde"
            else:
                return "Brown"
        elif color_type == "eye":
            if h < 15 or h > 165:
                return "Brown"
            elif h < 100:
                return "Green/Hazel"
            else:
                return "Blue"
        else:
            # General color classification
            if h < 15 or h > 165:
                return "Red"
            elif h < 30:
                return "Orange"
            elif h < 50:
                return "Yellow"
            elif h < 80:
                return "Green"
            elif h < 130:
                return "Blue"
            elif h < 160:
                return "Purple"
            else:
                return "Pink"
    
    def _find_dominant_colors(self, image: np.ndarray, n_colors: int = 2) -> List[str]:
        """
        Find the dominant colors in an image region.
        
        Args:
            image: Input image region
            n_colors: Number of dominant colors to find
            
        Returns:
            List of color names
        """
        # Reshape image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Use K-means clustering to find dominant colors
        from scipy.cluster.vq import kmeans, vq
        
        try:
            # Convert to float
            pixels_float = np.float32(pixels)
            
            # Perform K-means clustering
            centroids, _ = kmeans(pixels_float, n_colors)
            
            # Classify each centroid
            colors = []
            for centroid in centroids:
                color_name = self._classify_color(centroid.astype(int))
                colors.append(color_name)
            
            return colors
        except Exception:
            # Fallback: use simple average if K-means fails
            avg_color = np.mean(pixels, axis=0).astype(int)
            return [self._classify_color(avg_color)]
    
    def process_frame(self, frame: np.ndarray, show_overlay: bool = True, frame_timestamp_ms: int = 0) -> Tuple[np.ndarray, Dict]:
        """
        Process a single video frame and extract all attributes.
        
        Args:
            frame: Input video frame
            show_overlay: Whether to draw overlays on the frame
            frame_timestamp_ms: Timestamp of the frame in milliseconds
            
        Returns:
            Tuple of (processed_frame, analysis_results)
        """
        h, w = frame.shape[:2]
        
        # Convert frame to MediaPipe Image
        mp_image = Image(image_format=ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Process with MediaPipe Pose Landmarker
        pose_results = self.pose_landmarker.detect_for_video(mp_image, frame_timestamp_ms)
        
        analysis_results = {
            "height_cm": 0.0,
            "hair_color": "Unknown",
            "eye_color": "Unknown",
            "clothing_colors": ["Unknown"],
            "person_detected": False
        }
        
        output_frame = frame.copy()
        
        if pose_results.pose_landmarks and len(pose_results.pose_landmarks) > 0:
            analysis_results["person_detected"] = True
            
            # Estimate height
            height = self.estimate_height(pose_results.pose_landmarks, h)
            analysis_results["height_cm"] = round(height, 1)
            
            # Detect colors
            analysis_results["hair_color"] = self.detect_hair_color(frame, pose_results.pose_landmarks)
            analysis_results["eye_color"] = self.detect_eye_color(frame, pose_results.pose_landmarks)
            analysis_results["clothing_colors"] = self.detect_clothing_colors(frame, pose_results.pose_landmarks)
            
            if show_overlay:
                # Draw pose landmarks
                pose_landmarks = pose_results.pose_landmarks[0]
                
                # Draw connections
                for connection in self.pose_connections:
                    start_idx = connection.start
                    end_idx = connection.end
                    
                    if start_idx < len(pose_landmarks) and end_idx < len(pose_landmarks):
                        start_landmark = pose_landmarks[start_idx]
                        end_landmark = pose_landmarks[end_idx]
                        
                        start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
                        end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
                        
                        cv2.line(output_frame, start_point, end_point, (0, 255, 0), 2)
                
                # Draw landmarks
                for landmark in pose_landmarks:
                    landmark_point = (int(landmark.x * w), int(landmark.y * h))
                    cv2.circle(output_frame, landmark_point, 3, (0, 0, 255), -1)
                
                # Draw analysis results as text overlay
                y_offset = 30
                cv2.putText(output_frame, f"Height: {analysis_results['height_cm']:.1f} cm", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                y_offset += 30
                cv2.putText(output_frame, f"Hair: {analysis_results['hair_color']}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                y_offset += 30
                cv2.putText(output_frame, f"Eyes: {analysis_results['eye_color']}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                y_offset += 30
                clothing_text = f"Clothing: {', '.join(analysis_results['clothing_colors'])}"
                cv2.putText(output_frame, clothing_text, 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return output_frame, analysis_results
    
    def process_video(self, video_path: str, output_path: Optional[str] = None, 
                     display_realtime: bool = True) -> List[Dict]:
        """
        Process an entire video file.
        
        Args:
            video_path: Path to input video file
            output_path: Optional path to save processed video
            display_realtime: Whether to display video in real-time
            
        Returns:
            List of analysis results for each frame
        """
        cap = self.open_video(video_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Processing video: {video_path}")
        print(f"Resolution: {width}x{height}, FPS: {fps}, Total frames: {total_frames}")
        if display_realtime:
            print("\n🎬 Real-time display active - Video window will appear shortly...")
            print("   Press 'q' to quit | Press 'p' to pause/resume")
        print()
        
        # Initialize video writer if output path is specified
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        all_results = []
        frame_count = 0
        frame_timestamp_ms = 0
        ms_per_frame = 1000 // fps if fps > 0 else 33  # Default to ~30fps if fps is 0
        paused = False
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process frame
                processed_frame, results = self.process_frame(frame, show_overlay=True, frame_timestamp_ms=frame_timestamp_ms)
                all_results.append(results)
                
                # Write to output video
                if writer:
                    writer.write(processed_frame)
                
                # Display in real-time
                if display_realtime:
                    cv2.imshow('AI Video Detector', processed_frame)
                    
                    # Handle keyboard input
                    key = cv2.waitKey(1 if not paused else 0) & 0xFF
                    if key == ord('q'):
                        print("\nProcessing interrupted by user")
                        break
                    elif key == ord('p'):
                        paused = not paused
                        if paused:
                            print("\n⏸️  Paused - Press 'p' to resume or 'q' to quit")
                        else:
                            print("▶️  Resumed")
                
                frame_count += 1
                frame_timestamp_ms += ms_per_frame
                
                if frame_count % 30 == 0:
                    print(f"Processed {frame_count}/{total_frames} frames ({frame_count*100//total_frames if total_frames > 0 else 0}%)")
        
        finally:
            cap.release()
            if writer:
                writer.release()
            if display_realtime:
                cv2.destroyAllWindows()
        
        print(f"Processing complete. Processed {frame_count} frames.")
        return all_results
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'pose_landmarker'):
            self.pose_landmarker.close()
