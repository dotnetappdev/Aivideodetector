# Quick Reference Guide

## Installation
```bash
pip install -r requirements.txt
python download_models.py  # Download MediaPipe model
```

## Basic Commands

### Analyze a video
```bash
python main.py video.mp4
```

### Save output
```bash
python main.py input.mp4 -o output.mp4
```

### Process without display (faster)
```bash
python main.py video.mp4 --no-display -o output.mp4
```

### Custom height calibration
```bash
python main.py video.mp4 --reference-height 180
```

## What It Detects

- 📏 **Height**: Estimated in centimeters
- 💇 **Hair Color**: Black, Brown, Blonde, Red/Auburn, Gray, White
- 👁️ **Eye Color**: Brown, Blue, Green/Hazel
- 👔 **Clothing**: Top 2 dominant colors

## Supported Formats

MP4, MKV, AVI, MOV, WMV, FLV, WEBM

## Key Features

✅ Real-time video overlay
✅ Save processed videos
✅ Large file support
✅ Multiple format support
✅ Pose skeleton visualization
✅ Color detection and classification

## Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `video_path` | Input video file (required) | `video.mp4` |
| `-o, --output` | Save processed video | `-o output.mp4` |
| `--no-display` | Disable real-time display | `--no-display` |
| `--reference-height` | Height calibration (cm) | `--reference-height 175` |
| `-h, --help` | Show help message | `-h` |

## Output Information

### Terminal Output
- Processing progress (%)
- Frames with person detected
- Average height
- Most common colors

### Video Output
- Green pose skeleton
- Red landmark dots
- Text overlays with attributes
- Real-time analysis results

## Performance Tips

🚀 Use `--no-display` for faster batch processing
🚀 Lower video resolution for speed
🚀 Close other applications
🚀 Process shorter clips first to test

## Common Issues

| Issue | Solution |
|-------|----------|
| Model not found | Run `python download_models.py` |
| Import errors | `pip install -r requirements.txt --upgrade` |
| Slow processing | Use `--no-display` flag |
| Display errors | Use `--no-display` flag |
| No person detected | Ensure person is clearly visible |

## Quick Links

- [SETUP.md](SETUP.md) - Installation guide
- [DOCUMENTATION.md](DOCUMENTATION.md) - Full documentation
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Usage examples
- [examples.py](examples.py) - Code examples

## Python API Quick Start

```python
from video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer()
results = analyzer.process_video("video.mp4")

# Access per-frame results
for result in results:
    print(result['height_cm'])
    print(result['hair_color'])
    print(result['eye_color'])
    print(result['clothing_colors'])
```

## Minimum Requirements

- Python 3.8+
- 4GB RAM
- Multi-core CPU
- Disk space for videos

## Recommended

- Python 3.10+
- 8GB+ RAM
- Modern CPU (4+ cores)
- GPU support (optional)

---

**Need help?** See full documentation in [DOCUMENTATION.md](DOCUMENTATION.md)
