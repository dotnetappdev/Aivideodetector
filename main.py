#!/usr/bin/env python3
"""
AI Video Detector - Command Line Interface
Main entry point for processing videos with AI analysis.
"""

import argparse
import sys
import os
from video_analyzer import VideoAnalyzer


def main():
    """Main function to run the video analyzer."""
    parser = argparse.ArgumentParser(
        description='AI Video Detector - Analyze videos for human attributes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a video with real-time display
  python main.py input_video.mp4
  
  # Process and save output video
  python main.py input_video.mkv -o output_video.mp4
  
  # Process without real-time display
  python main.py large_video.mp4 --no-display -o analyzed.mp4
  
Supported formats: MP4, MKV, AVI, MOV, and most common video formats
        """
    )
    
    parser.add_argument(
        'video_path',
        type=str,
        help='Path to the input video file (MP4, MKV, AVI, etc.)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Path to save the processed video with overlays'
    )
    
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Disable real-time video display (useful for large files)'
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
        print(f"Error: Video file not found: {args.video_path}")
        sys.exit(1)
    
    # Create output directory if needed
    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    print("=" * 60)
    print("AI Video Detector")
    print("=" * 60)
    print(f"Input video: {args.video_path}")
    if args.output:
        print(f"Output video: {args.output}")
    print(f"Real-time display: {'No' if args.no_display else 'Yes'}")
    print("=" * 60)
    print()
    
    # Initialize analyzer
    print("Initializing AI models...")
    analyzer = VideoAnalyzer()
    analyzer.reference_height_cm = args.reference_height
    print("Models loaded successfully!")
    print()
    
    # Process video
    try:
        results = analyzer.process_video(
            video_path=args.video_path,
            output_path=args.output,
            display_realtime=not args.no_display
        )
        
        # Print summary
        print()
        print("=" * 60)
        print("Analysis Summary")
        print("=" * 60)
        
        # Calculate statistics
        detected_frames = [r for r in results if r['person_detected']]
        if detected_frames:
            avg_height = sum(r['height_cm'] for r in detected_frames) / len(detected_frames)
            
            # Most common attributes
            hair_colors = [r['hair_color'] for r in detected_frames]
            eye_colors = [r['eye_color'] for r in detected_frames]
            
            most_common_hair = max(set(hair_colors), key=hair_colors.count)
            most_common_eyes = max(set(eye_colors), key=eye_colors.count)
            
            print(f"Total frames processed: {len(results)}")
            print(f"Frames with person detected: {len(detected_frames)}")
            print(f"Average estimated height: {avg_height:.1f} cm")
            print(f"Most common hair color: {most_common_hair}")
            print(f"Most common eye color: {most_common_eyes}")
        else:
            print("No person detected in the video.")
        
        print("=" * 60)
        print("Processing complete!")
        
        if args.output:
            print(f"Processed video saved to: {args.output}")
        
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
