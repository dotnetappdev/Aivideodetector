# Aivideodetector

AI-powered video analysis system for detecting and analyzing human subjects in video files.

## 🎯 Features

- 📏 **Height Estimation**: Automatically estimates subject height from video frames
- 💇 **Hair Color Detection**: Identifies hair colors (Black, Brown, Blonde, Red, etc.)
- 👁️ **Eye Color Detection**: Detects eye colors (Brown, Blue, Green/Hazel)
- 👔 **Clothing Color Analysis**: Identifies dominant clothing colors
- 🎥 **Multi-format Support**: Works with MP4, MKV, AVI, and other video formats
- 🎨 **Real-time Overlay**: Displays analysis results directly on video in real-time

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dotnetappdev/Aivideodetector.git
cd Aivideodetector

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Process a video with real-time display
python main.py your_video.mp4

# Process and save output
python main.py input.mkv -o output.mp4

# Process large files without display
python main.py large_video.mp4 --no-display -o analyzed.mp4
```

## 📖 Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

## 🛠️ Requirements

- Python 3.8+
- OpenCV
- MediaPipe
- NumPy
- SciPy

See `requirements.txt` for complete list.

## 🎬 How It Works

The system uses:
- **MediaPipe** for pose detection and body landmark identification
- **OpenCV** for video processing and visualization
- **Computer Vision algorithms** for color analysis and height estimation

## 📝 Example Output

When processing a video, the system displays:
- Subject height in centimeters
- Hair color
- Eye color
- Clothing colors
- Pose landmarks overlaid on the video

## ⚡ Performance Tips

- Use `--no-display` for faster processing of large files
- Adjust `--reference-height` for more accurate height estimates
- Ensure good lighting in videos for better color detection

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is provided as-is for educational and research purposes.