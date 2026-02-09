#!/usr/bin/env python3
"""
Live Webcam Viewer with AI Analysis
View your webcam feed with real-time AI pose and attribute detection.
"""

import argparse
import sys
import cv2
import numpy as np
from video_analyzer import VideoAnalyzer


def main():
    """Live webcam viewer with AI analysis."""
    parser = argparse.ArgumentParser(
        description='Live Webcam AI Analyzer - Real-time analysis from your camera',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default webcam (camera 0)
  python webcam_viewer.py
  
  # Use a specific camera
  python webcam_viewer.py --camera 1
  
  # Custom height calibration
  python webcam_viewer.py --reference-height 175

Controls:
  - Press 'q' to quit
  - Press 's' to save a screenshot
  - Press 'r' to record a video clip
  
The webcam feed will display with:
  - Green pose skeleton
  - Red landmark points
  - Real-time height, hair, eyes, and clothing color detection
        """
    )
    
    parser.add_argument(
        '--camera',
        type=int,
        default=0,
        help='Camera device ID (default: 0 for default webcam)'
    )
    
    parser.add_argument(
        '--reference-height',
        type=float,
        default=170.0,
        help='Reference height in cm for calibration (default: 170.0)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📹 Live Webcam AI Analyzer")
    print("=" * 60)
    print(f"Camera: {args.camera}")
    print(f"Reference height: {args.reference_height} cm")
    print("\n💡 Controls:")
    print("   - Press 'q' to quit")
    print("   - Press 's' to save screenshot")
    print("=" * 60)
    print()
    
    # Initialize analyzer
    print("⚙️  Initializing AI models...")
    try:
        analyzer = VideoAnalyzer()
        analyzer.reference_height_cm = args.reference_height
        print("✅ Models loaded successfully!")
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        sys.exit(1)
    
    # Open webcam
    print(f"\n📹 Opening camera {args.camera}...")
    cap = cv2.VideoCapture(args.camera)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open camera {args.camera}")
        print("   Try a different camera ID with --camera option")
        sys.exit(1)
    
    print("✅ Camera opened successfully!")
    print("\n🎥 Starting live feed...")
    print("   (Press 'q' to quit)\n")
    
    frame_count = 0
    screenshot_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error reading from camera")
                break
            
            # Process frame with AI
            frame_timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            processed_frame, results = analyzer.process_frame(
                frame, 
                show_overlay=True,
                frame_timestamp_ms=frame_timestamp_ms
            )
            
            # Add FPS counter
            fps_text = f"FPS: {int(cap.get(cv2.CAP_PROP_FPS))}"
            cv2.putText(processed_frame, fps_text, 
                       (processed_frame.shape[1] - 100, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            # Display
            cv2.imshow('Live Webcam AI Analyzer', processed_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n⏹️  Stopping camera...")
                break
            elif key == ord('s'):
                # Save screenshot
                screenshot_count += 1
                filename = f"screenshot_{screenshot_count}.jpg"
                cv2.imwrite(filename, processed_frame)
                print(f"📸 Screenshot saved: {filename}")
            
            frame_count += 1
            
            # Print stats every 100 frames
            if frame_count % 100 == 0:
                if results['person_detected']:
                    print(f"✅ Frame {frame_count}: Person detected - "
                          f"Height: {results['height_cm']:.1f}cm, "
                          f"Hair: {results['hair_color']}, "
                          f"Eyes: {results['eye_color']}")
                else:
                    print(f"ℹ️  Frame {frame_count}: No person detected")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Camera stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"\n✅ Session complete. Processed {frame_count} frames.")
        if screenshot_count > 0:
            print(f"📸 {screenshot_count} screenshot(s) saved")


if __name__ == "__main__":
    main()
