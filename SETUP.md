# Setup Instructions for AI Video Detector

This guide will help you set up the AI Video Detector on your system.

## Step 1: Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- git (for cloning the repository)

Check your Python version:
```bash
python --version
# or
python3 --version
```

## Step 2: Clone the Repository

```bash
git clone https://github.com/dotnetappdev/Aivideodetector.git
cd Aivideodetector
```

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you need to install for your user only:
```bash
pip install --user -r requirements.txt
```

## Step 4: Download the MediaPipe Model

The application requires a MediaPipe Pose Landmarker model file. This model enables the detection and tracking of human poses in videos.

### Option A: Automatic Download (Try this first)

Run the download script:
```bash
python download_models.py
```

### Option B: Manual Download (If automatic fails)

If the automatic download doesn't work due to network restrictions:

1. **Open your web browser** and navigate to:
   ```
   https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task
   ```

2. **Save the file** that downloads (it should be around 3-7 MB)

3. **Create a models directory** in the project root:
   ```bash
   mkdir models
   ```

4. **Move the downloaded file** to the models directory and rename it:
   ```bash
   # On Windows:
   move Downloads\pose_landmarker_lite.task models\pose_landmarker_lite.task
   
   # On Mac/Linux:
   mv ~/Downloads/pose_landmarker_lite.task models/pose_landmarker_lite.task
   ```

### Option C: Alternative Model URL

If the above URL doesn't work, try these alternative models:

- **Heavy model** (more accurate, slower):
  https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task

- **Full model** (balanced):
  https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task

Place any of these in the `models/` directory with the filename `pose_landmarker_lite.task`.

## Step 5: Verify Installation

Test that everything is set up correctly:

```bash
python test_analyzer.py
```

If you see "All tests passed! ✓", you're ready to go!

## Step 6: Run the Application

### Process a video file:

```bash
python main.py your_video.mp4
```

### See all options:

```bash
python main.py --help
```

### Process and save output:

```bash
python main.py input.mp4 -o output_analyzed.mp4
```

## Troubleshooting

### Model Download Fails

If automatic download fails:
- Check your internet connection
- Try manual download (Option B above)
- Some corporate/school networks block certain downloads
- Try downloading from a different network or using a VPN

### Import Errors

If you get "ModuleNotFoundError":
```bash
pip install -r requirements.txt --upgrade
```

### OpenCV Display Issues

If you get display errors:
- Use `--no-display` flag to process without showing video:
  ```bash
  python main.py video.mp4 --no-display -o output.mp4
  ```

### Video Won't Open

- Ensure the video file path is correct
- Check that the video format is supported (MP4, MKV, AVI, MOV, etc.)
- Try converting the video to MP4 using a tool like ffmpeg:
  ```bash
  ffmpeg -i input_video.mkv output_video.mp4
  ```

### Slow Processing

For better performance:
- Use `--no-display` flag
- Close other applications
- Process shorter video clips first to test
- Use a smaller resolution video

## Getting Help

For more information, see:
- [README.md](README.md) - Quick start guide
- [DOCUMENTATION.md](DOCUMENTATION.md) - Complete documentation
- [examples.py](examples.py) - Code examples

## System Requirements

- **OS**: Windows, Linux, or macOS
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core processor recommended
- **Storage**: Sufficient space for video files (input + output)
- **Python**: 3.8 or higher
