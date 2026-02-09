#!/usr/bin/env python3
"""
Example script demonstrating how to use the VideoAnalyzer API.
This shows various ways to use the video analysis functionality.
"""

import cv2
from video_analyzer import VideoAnalyzer


def example_1_process_single_frame():
    """Example 1: Process a single frame from an image."""
    print("=" * 60)
    print("Example 1: Process a single frame")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = VideoAnalyzer()
    
    # Read an image (you can use a video frame here)
    # For this example, we'll create a dummy frame
    # In practice, you would use: frame = cv2.imread('person.jpg')
    print("Note: This example requires an image file.")
    print("Usage: frame = cv2.imread('person.jpg')")
    print("       processed_frame, results = analyzer.process_frame(frame)")
    print()


def example_2_process_video_basic():
    """Example 2: Basic video processing."""
    print("=" * 60)
    print("Example 2: Basic video processing")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = VideoAnalyzer()
    
    # Process video with default settings
    video_path = "sample_video.mp4"  # Replace with your video
    
    print(f"To process a video: analyzer.process_video('{video_path}')")
    print("This will display the video in real-time with overlays.")
    print()


def example_3_process_and_save():
    """Example 3: Process video and save output."""
    print("=" * 60)
    print("Example 3: Process and save output video")
    print("=" * 60)
    
    analyzer = VideoAnalyzer()
    
    video_path = "input.mkv"
    output_path = "output.mp4"
    
    print(f"analyzer.process_video(")
    print(f"    video_path='{video_path}',")
    print(f"    output_path='{output_path}',")
    print(f"    display_realtime=True")
    print(f")")
    print()


def example_4_custom_processing():
    """Example 4: Custom frame-by-frame processing."""
    print("=" * 60)
    print("Example 4: Custom frame-by-frame processing")
    print("=" * 60)
    
    print("""
# Initialize analyzer
analyzer = VideoAnalyzer()

# Open video
cap = analyzer.open_video('video.mp4')

# Process each frame with custom logic
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process the frame
    processed_frame, results = analyzer.process_frame(frame)
    
    # Your custom logic here
    if results['person_detected']:
        print(f"Height: {results['height_cm']:.1f} cm")
        print(f"Hair: {results['hair_color']}")
        print(f"Eyes: {results['eye_color']}")
        print(f"Clothing: {results['clothing_colors']}")
    
    # Display or save frame
    cv2.imshow('Custom Processing', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    """)
    print()


def example_5_analyze_specific_attributes():
    """Example 5: Extract specific attributes only."""
    print("=" * 60)
    print("Example 5: Extract specific attributes")
    print("=" * 60)
    
    print("""
# Initialize analyzer
analyzer = VideoAnalyzer()

# Read a frame
frame = cv2.imread('person.jpg')
image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Get pose landmarks
pose_results = analyzer.pose.process(image_rgb)

if pose_results.pose_landmarks:
    # Get only the attributes you need
    height = analyzer.estimate_height(
        pose_results.pose_landmarks, 
        frame.shape[0]
    )
    
    hair_color = analyzer.detect_hair_color(
        frame, 
        pose_results.pose_landmarks
    )
    
    eye_color = analyzer.detect_eye_color(
        frame, 
        pose_results.pose_landmarks
    )
    
    clothing_colors = analyzer.detect_clothing_colors(
        frame, 
        pose_results.pose_landmarks
    )
    
    print(f"Height: {height:.1f} cm")
    print(f"Hair: {hair_color}")
    print(f"Eyes: {eye_color}")
    print(f"Clothing: {clothing_colors}")
    """)
    print()


def example_6_batch_processing():
    """Example 6: Batch process multiple videos."""
    print("=" * 60)
    print("Example 6: Batch process multiple videos")
    print("=" * 60)
    
    print("""
import os
from video_analyzer import VideoAnalyzer

# Initialize analyzer once
analyzer = VideoAnalyzer()

# List of videos to process
video_files = [
    'video1.mp4',
    'video2.mkv',
    'video3.avi'
]

# Process each video
for video_path in video_files:
    print(f"Processing {video_path}...")
    
    output_path = f"analyzed_{os.path.basename(video_path)}"
    
    results = analyzer.process_video(
        video_path=video_path,
        output_path=output_path,
        display_realtime=False  # Disable display for batch processing
    )
    
    # Calculate statistics
    detected_frames = [r for r in results if r['person_detected']]
    if detected_frames:
        avg_height = sum(r['height_cm'] for r in detected_frames) / len(detected_frames)
        print(f"  Average height: {avg_height:.1f} cm")
    
    print(f"  Saved to: {output_path}")
    """)
    print()


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("AI Video Detector - API Usage Examples")
    print("*" * 60)
    print("\n")
    
    example_1_process_single_frame()
    example_2_process_video_basic()
    example_3_process_and_save()
    example_4_custom_processing()
    example_5_analyze_specific_attributes()
    example_6_batch_processing()
    
    print("=" * 60)
    print("For more information, see DOCUMENTATION.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
