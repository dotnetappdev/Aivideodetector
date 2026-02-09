# AI Video Detector

An advanced video analysis system that uses computer vision and AI to detect and analyze human subjects in video files. The system can estimate height, detect hair color, eye color, and clothing colors, displaying the results in real-time overlays on the video.

## Features

- 🎥 **Multi-format Support**: Process MP4, MKV, AVI, MOV, and other common video formats
- 📏 **Height Estimation**: Estimates the height of subjects in the video frames
- 💇 **Hair Color Detection**: Identifies dominant hair colors (Black, Brown, Blonde, Red/Auburn, etc.)
- 👁️ **Eye Color Detection**: Detects eye colors (Brown, Blue, Green/Hazel)
- 👔 **Clothing Color Analysis**: Identifies dominant clothing colors
- 🎨 **Real-time Overlay**: Displays analysis results directly on the video in real-time
- 💾 **Video Export**: Save processed videos with overlays for later review
- ⚡ **Large File Support**: Efficiently handles large video files

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- A webcam or video files for testing

### Install Dependencies

1. Clone the repository:
```bash
git clone https://github.com/dotnetappdev/Aivideodetector.git
cd Aivideodetector
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. **Download the MediaPipe Pose Landmarker model:**

The application requires a MediaPipe pose landmarker model file. You have two options:

**Option A - Auto-download (recommended):**
```bash
python download_models.py
```

**Option B - Manual download:**
1. Download the model from: [MediaPipe Pose Landmarker](https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task)
2. Create a `models` directory in the project root
3. Place the downloaded file as `models/pose_landmarker_lite.task`

**Option C - Use wget:**
```bash
mkdir -p models
wget -O models/pose_landmarker_lite.task "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
```

**Note:** If you encounter download issues, you may need to use a browser to download the model file manually.

## Usage

### Basic Usage

Process a video with real-time display:
```bash
python main.py video.mp4
```

### Save Processed Video

Process a video and save the output with overlays:
```bash
python main.py input_video.mkv -o output_video.mp4
```

### Process Large Files Without Display

For large files, disable real-time display to improve performance:
```bash
python main.py large_video.mp4 --no-display -o analyzed.mp4
```

### Custom Height Calibration

Adjust the reference height for better height estimation:
```bash
python main.py video.mp4 --reference-height 175.0
```

### Command Line Options

```
positional arguments:
  video_path            Path to the input video file (MP4, MKV, AVI, etc.)

optional arguments:
  -h, --help           Show this help message and exit
  -o OUTPUT, --output OUTPUT
                       Path to save the processed video with overlays
  --no-display         Disable real-time video display (useful for large files)
  --reference-height REFERENCE_HEIGHT
                       Reference height in cm for calibration (default: 170.0)
```

## How It Works

### Architecture

The AI Video Detector uses the following technologies:

1. **OpenCV**: For video I/O, frame processing, and visualization
2. **MediaPipe**: Google's ML solution for pose detection and tracking
3. **Computer Vision Algorithms**: For color detection and analysis

### Processing Pipeline

1. **Video Loading**: Opens video file using OpenCV
2. **Pose Detection**: MediaPipe detects human poses in each frame
3. **Height Estimation**: Calculates height based on body landmarks
4. **Color Analysis**:
   - Hair: Analyzes region above the head
   - Eyes: Samples eye regions from facial landmarks
   - Clothing: Analyzes torso region using K-means clustering
5. **Overlay Generation**: Draws pose landmarks and text annotations
6. **Output**: Displays real-time and/or saves processed video

### Detection Methods

#### Height Estimation

Height is estimated using the following approach:
- Detects key body landmarks (nose, ankles)
- Calculates pixel distance from head to feet
- Applies calibration factor based on reference height
- Returns estimated height in centimeters

**Limitations**: 
- Accuracy depends on camera angle and distance
- Works best when subject is standing upright
- May require calibration for different camera setups

#### Hair Color Detection

Hair color is detected by:
- Identifying head region from pose landmarks
- Sampling pixels from the area above the head
- Converting to HSV color space for classification
- Categorizing into common hair colors

**Detected Colors**: Black, Brown, Blonde, Red/Auburn, Gray, White

#### Eye Color Detection

Eye color is detected by:
- Locating eye positions from facial landmarks
- Sampling small regions around each eye
- Averaging color values
- Classifying into eye color categories

**Detected Colors**: Brown, Blue, Green/Hazel

#### Clothing Color Detection

Clothing colors are detected by:
- Identifying torso region (shoulders to hips)
- Using K-means clustering to find dominant colors
- Classifying colors into named categories

**Detected Colors**: Red, Orange, Yellow, Green, Blue, Purple, Pink, Black, White, Gray

## API Usage

You can also use the VideoAnalyzer class in your own Python scripts:

```python
from video_analyzer import VideoAnalyzer

# Initialize the analyzer
analyzer = VideoAnalyzer()

# Process a single frame
frame = cv2.imread('image.jpg')
processed_frame, results = analyzer.process_frame(frame)

print(f"Height: {results['height_cm']} cm")
print(f"Hair: {results['hair_color']}")
print(f"Eyes: {results['eye_color']}")
print(f"Clothing: {results['clothing_colors']}")

# Process entire video
results_list = analyzer.process_video(
    video_path='video.mp4',
    output_path='output.mp4',
    display_realtime=True
)
```

## Examples

### Example 1: Quick Analysis

```bash
python main.py sample_video.mp4
```

This will:
- Open the video
- Process each frame
- Display results in real-time
- Show analysis summary at the end

### Example 2: Batch Processing

```bash
python main.py interview.mkv --no-display -o analyzed_interview.mp4
```

This will:
- Process the video without display (faster)
- Save the analyzed video with overlays
- Print progress updates and summary

### Example 3: Custom Calibration

```bash
python main.py sports_video.mp4 --reference-height 180.0 -o sports_analyzed.mp4
```

This will:
- Use 180cm as reference height for better accuracy
- Process and display in real-time
- Save the output video

## Supported Video Formats

The system supports all video formats that OpenCV can read, including:
- MP4 (H.264, H.265)
- MKV (Matroska)
- AVI
- MOV
- WMV
- FLV
- WEBM

## Performance Considerations

### For Large Files

When processing large video files (>1GB):
1. Use `--no-display` to disable real-time display
2. Ensure sufficient disk space for output
3. Consider processing on a machine with GPU support
4. Monitor memory usage during processing

### For Real-time Performance

To improve real-time processing speed:
1. Use smaller resolution videos
2. Reduce MediaPipe model complexity (modify `video_analyzer.py`)
3. Skip frames if needed (modify the processing loop)
4. Use GPU acceleration if available

## Troubleshooting

### Video Won't Open

- Ensure the video file path is correct
- Check that the video format is supported
- Verify the file is not corrupted

### Slow Processing

- Disable real-time display with `--no-display`
- Use a smaller resolution video
- Close other applications to free up resources

### Poor Detection Quality

- Ensure good lighting in the video
- Subject should be clearly visible
- Try adjusting the reference height for better calibration
- Check that the subject is facing the camera

### Missing Dependencies

If you get import errors:
```bash
pip install -r requirements.txt --upgrade
```

## Technical Details

### Dependencies

- **opencv-python**: Video I/O and image processing
- **mediapipe**: Pose detection and tracking
- **numpy**: Numerical computations
- **scipy**: K-means clustering for color analysis
- **pillow**: Image format support

### System Requirements

- **OS**: Windows, Linux, or macOS
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core processor recommended
- **GPU**: Optional, but improves performance
- **Disk**: Sufficient space for input/output videos

## Limitations

- Height estimation is approximate and depends on camera calibration
- Color detection works best with good lighting conditions
- Multiple people in frame: currently processes the first detected person
- Occluded subjects may not be detected accurately
- Real-time display may lag on slower systems

## Future Improvements

Potential enhancements for future versions:
- Support for multiple people in the same frame
- More accurate height estimation with camera calibration
- Additional attributes (age estimation, gender detection)
- GPU acceleration for faster processing
- Web interface for easier usage
- Video analytics dashboard
- Support for live camera feeds

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

- MediaPipe by Google for pose detection
- OpenCV community for computer vision tools
- Contributors and users of this project
