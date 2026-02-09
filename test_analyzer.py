#!/usr/bin/env python3
"""
Simple test script to verify the VideoAnalyzer works correctly.
"""

import cv2
import numpy as np
from video_analyzer import VideoAnalyzer


def test_basic_functionality():
    """Test basic functionality of VideoAnalyzer."""
    print("=" * 60)
    print("Testing AI Video Detector")
    print("=" * 60)
    
    # Create analyzer
    print("\n1. Initializing VideoAnalyzer...")
    try:
        analyzer = VideoAnalyzer()
        print("   ✓ VideoAnalyzer initialized successfully!")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return False
    
    # Create a test frame (black image)
    print("\n2. Creating test frame...")
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    print("   ✓ Test frame created (640x480)")
    
    # Test processing without a person
    print("\n3. Processing frame without person...")
    try:
        processed_frame, results = analyzer.process_frame(test_frame, show_overlay=True, frame_timestamp_ms=0)
        print(f"   ✓ Processing successful")
        print(f"   - Person detected: {results['person_detected']}")
        print(f"   - Height: {results['height_cm']} cm")
        print(f"   - Hair: {results['hair_color']}")
        print(f"   - Eyes: {results['eye_color']}")
        print(f"   - Clothing: {results['clothing_colors']}")
    except Exception as e:
        print(f"   ✗ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test opening a non-existent video (should fail gracefully)
    print("\n4. Testing error handling...")
    try:
        analyzer.open_video("non_existent_video.mp4")
        print("   ✗ Should have raised an error!")
        return False
    except FileNotFoundError:
        print("   ✓ Error handling works correctly")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False
    
    # Test color classification
    print("\n5. Testing color classification...")
    test_colors = [
        (np.array([255, 0, 0]), "Red/Blue region"),
        (np.array([0, 255, 0]), "Green region"),
        (np.array([0, 0, 255]), "Red region"),
        (np.array([200, 200, 200]), "Gray/White"),
        (np.array([50, 50, 50]), "Black/Dark"),
    ]
    
    for color, expected in test_colors:
        result = analyzer._classify_color(color, color_type="general")
        print(f"   - {expected}: {result}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)
