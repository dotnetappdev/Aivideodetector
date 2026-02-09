#!/usr/bin/env python3
"""
Real-Time Video Viewer with AI Analysis
Simple script to view videos in real-time with AI overlays.
"""

import argparse
import sys
import os
from video_analyzer import VideoAnalyzer


def main():
    """Real-time video viewer."""
    parser = argparse.ArgumentParser(
        description='Real-Time AI Video Viewer - Watch videos with live AI analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View a video with real-time AI analysis
  python realtime_viewer.py video.mp4
  
  # View with custom height calibration
  python realtime_viewer.py video.mp4 --reference-height 175
  
  # View and save the analyzed video
  python realtime_viewer.py input.mp4 --save output.mp4

Controls while viewing:
  - Press 'q' to quit
  - Press 'p' to pause/resume
  
The video will display with:
  - Green pose skeleton
  - Red landmark points
  - Text overlay showing height, hair, eyes, and clothing colors
        """
    )
    
    parser.add_argument(
        'video_path',
        type=str,
        help='Path to the input video file'
    )
    
    parser.add_argument(
        '--save',
        type=str,
        default=None,
        help='Optional: Save the analyzed video to this path'
    )
    
    parser.add_argument(
        '--reference-height',
        type=float,
        default=170.0,
        help='Reference height in cm for calibration (default: 170.0)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.video_path):
        print(f"❌ Error: Video file not found: {args.video_path}")
        sys.exit(1)
    
    # Create output directory if needed
    if args.save:
        output_dir = os.path.dirname(args.save)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    print("=" * 60)
    print("🎬 Real-Time AI Video Viewer")
    print("=" * 60)
    print(f"Video: {args.video_path}")
    if args.save:
        print(f"Saving to: {args.save}")
    print(f"Reference height: {args.reference_height} cm")
    print("\n💡 Controls:")
    print("   - Press 'q' to quit")
    print("   - Press 'p' to pause/resume")
    print("=" * 60)
    print()
    
    # Initialize analyzer
    print("⚙️  Initializing AI models...")
    try:
        analyzer = VideoAnalyzer()
        analyzer.reference_height_cm = args.reference_height
        print("✅ Models loaded successfully!")
        print()
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        sys.exit(1)
    
    # Process video with real-time display
    try:
        print("🎥 Starting real-time playback...")
        print("   (Video window will appear shortly)\n")
        
        results = analyzer.process_video(
            video_path=args.video_path,
            output_path=args.save,
            display_realtime=True  # Always display in real-time
        )
        
        # Print summary
        print()
        print("=" * 60)
        print("📊 Analysis Summary")
        print("=" * 60)
        
        detected_frames = [r for r in results if r['person_detected']]
        if detected_frames:
            avg_height = sum(r['height_cm'] for r in detected_frames) / len(detected_frames)
            hair_colors = [r['hair_color'] for r in detected_frames]
            eye_colors = [r['eye_color'] for r in detected_frames]
            most_common_hair = max(set(hair_colors), key=hair_colors.count)
            most_common_eyes = max(set(eye_colors), key=eye_colors.count)
            
            print(f"📏 Average height: {avg_height:.1f} cm")
            print(f"💇 Hair color: {most_common_hair}")
            print(f"👁️  Eye color: {most_common_eyes}")
            print(f"📹 Frames with person: {len(detected_frames)}/{len(results)}")
        else:
            print("ℹ️  No person detected in the video")
        
        print("=" * 60)
        
        if args.save:
            print(f"✅ Analyzed video saved to: {args.save}")
        
        print("\n✅ Playback complete!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Playback interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during playback: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
