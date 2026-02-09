# Real-Time Viewing Guide

This guide explains how to view videos and live camera feeds in real-time with AI analysis.

## Quick Start

### View a Video File in Real-Time

**Option 1: Using main.py (default)**
```bash
python main.py your_video.mp4
```

**Option 2: Using dedicated real-time viewer**
```bash
python realtime_viewer.py your_video.mp4
```

**Option 3: Live webcam feed**
```bash
python webcam_viewer.py
```

## Three Ways to View in Real-Time

### 1. Main Application (main.py)

The standard way to process videos. Real-time display is **enabled by default**.

```bash
# View with real-time display
python main.py video.mp4

# View and save analyzed video
python main.py video.mp4 -o analyzed.mp4

# Disable display for faster processing
python main.py video.mp4 --no-display -o output.mp4
```

**Features:**
- Full video processing with statistics
- Real-time overlay display
- Optional video saving
- Progress tracking

**Controls:**
- Press **'q'** to quit
- Press **'p'** to pause/resume

### 2. Real-Time Viewer (realtime_viewer.py)

Dedicated script focused on viewing experience with clearer output.

```bash
# Basic viewing
python realtime_viewer.py video.mp4

# View with custom height calibration
python realtime_viewer.py video.mp4 --reference-height 175

# View and save
python realtime_viewer.py video.mp4 --save output.mp4
```

**Features:**
- Enhanced user interface
- Clear instructions and emoji feedback
- Focused on viewing experience
- Summary statistics after playback

**Controls:**
- Press **'q'** to quit
- Press **'p'** to pause/resume

### 3. Webcam Viewer (webcam_viewer.py)

Live camera feed analysis in real-time.

```bash
# Use default webcam (camera 0)
python webcam_viewer.py

# Use specific camera
python webcam_viewer.py --camera 1

# With height calibration
python webcam_viewer.py --reference-height 175
```

**Features:**
- Live camera feed analysis
- Real-time pose detection
- Instant attribute detection
- Screenshot capture
- FPS counter

**Controls:**
- Press **'q'** to quit
- Press **'s'** to save screenshot

## What You'll See

When viewing in real-time, the video window displays:

### Visual Overlays
1. **Green Pose Skeleton** - Lines connecting body joints
2. **Red Landmark Points** - 33 body landmark positions
3. **Text Information** (top-left corner):
   - Height: [estimated height in cm]
   - Hair: [detected hair color]
   - Eyes: [detected eye color]  
   - Clothing: [dominant clothing colors]

### Example Display
```
┌─────────────────────────────────────┐
│ Height: 172.5 cm                   │
│ Hair: Brown                        │
│ Eyes: Blue                         │
│ Clothing: Blue, White              │
│                                     │
│        [Person with                │
│         pose skeleton              │
│         overlaid]                  │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

## Keyboard Controls

### During Playback

| Key | Action | Available In |
|-----|--------|--------------|
| **q** | Quit/Exit | All viewers |
| **p** | Pause/Resume | main.py, realtime_viewer.py |
| **s** | Save Screenshot | webcam_viewer.py |

### Pause Mode

When paused (press 'p'):
- Video freezes on current frame
- You can examine the current analysis
- Press 'p' again to resume
- Press 'q' to quit

## Command-Line Options

### main.py Options
```bash
python main.py VIDEO_PATH [OPTIONS]

Required:
  VIDEO_PATH              Path to video file

Options:
  -o, --output PATH       Save analyzed video
  --no-display           Disable real-time display
  --reference-height CM   Height calibration (default: 170)
  -h, --help             Show help message
```

### realtime_viewer.py Options
```bash
python realtime_viewer.py VIDEO_PATH [OPTIONS]

Required:
  VIDEO_PATH              Path to video file

Options:
  --save PATH            Save analyzed video
  --reference-height CM   Height calibration (default: 170)
  -h, --help             Show help message
```

### webcam_viewer.py Options
```bash
python webcam_viewer.py [OPTIONS]

Options:
  --camera ID            Camera device ID (default: 0)
  --reference-height CM   Height calibration (default: 170)
  -h, --help             Show help message
```

## Troubleshooting

### Video Window Doesn't Appear

**Symptoms:** The script runs but no window shows up.

**Solutions:**
1. Check if you're using `--no-display` flag (remove it)
2. On some systems, the window may appear minimized - check your taskbar
3. On headless servers, real-time display won't work (use `--no-display`)

```bash
# Ensure display is enabled
python main.py video.mp4  # Don't use --no-display
```

### Window Appears But Is Blank

**Symptoms:** Window opens but shows black screen.

**Solutions:**
1. Wait a few seconds - model initialization takes time
2. Check if video file is valid: `python -c "import cv2; print(cv2.VideoCapture('video.mp4').isOpened())"`
3. Try a different video file or format

### Webcam Not Working

**Symptoms:** Error opening camera or black webcam feed.

**Solutions:**
1. Check camera permissions (some OS require camera access approval)
2. Try a different camera ID: `python webcam_viewer.py --camera 1`
3. Test camera with: `python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`
4. Close other applications using the camera

### Slow or Laggy Playback

**Symptoms:** Video plays but is slow or choppy.

**Solutions:**
1. This is normal - AI processing is computationally intensive
2. Close other applications to free up CPU
3. For faster processing without display: `python main.py video.mp4 --no-display -o output.mp4`
4. Process a lower resolution video

### "Press 'q' to quit" Doesn't Work

**Symptoms:** Pressing 'q' doesn't exit the program.

**Solutions:**
1. Make sure the video window is in focus (click on it)
2. Try pressing 'q' multiple times
3. Use Ctrl+C in the terminal as a backup
4. On Mac, try Cmd+Q or Cmd+W to close the window

## Performance Tips

### For Better Real-Time Performance

1. **Lower video resolution** - Smaller videos process faster
2. **Close other applications** - Free up CPU resources
3. **Use SSD storage** - Faster video file reading
4. **Adequate lighting** - Improves detection accuracy
5. **Clear view of person** - Better tracking results

### Optimal Viewing Setup

- **Distance from camera:** 2-4 meters (6-12 feet)
- **Lighting:** Front-lit, avoid backlighting
- **Background:** Plain, uncluttered
- **Posture:** Standing upright facing camera
- **Clothing:** Solid colors work best

## Examples

### Example 1: Quick Video Preview
```bash
# Watch a video with AI analysis
python realtime_viewer.py sample.mp4
```

### Example 2: Analyze and Save
```bash
# View and save analyzed video
python main.py input.mp4 -o analyzed_output.mp4
```

### Example 3: Live Selfie Analysis
```bash
# Analyze yourself with webcam
python webcam_viewer.py
```

### Example 4: Custom Height Calibration
```bash
# If you know subject is 180cm tall
python realtime_viewer.py video.mp4 --reference-height 180
```

### Example 5: Multiple Camera Setup
```bash
# Use external USB camera (usually camera 1)
python webcam_viewer.py --camera 1
```

## Advanced Usage

### Save Webcam Screenshots

While using webcam viewer, press 's' repeatedly to capture multiple screenshots:

```bash
python webcam_viewer.py
# Press 's' when you want to save a screenshot
# Files saved as: screenshot_1.jpg, screenshot_2.jpg, etc.
```

### Batch Process Multiple Videos

Process several videos with real-time preview:

```bash
# Process first video
python realtime_viewer.py video1.mp4 --save analyzed1.mp4

# When done, process next
python realtime_viewer.py video2.mp4 --save analyzed2.mp4
```

### Height Calibration for Accuracy

For best height estimation accuracy:

1. Measure actual height of subject
2. Process video once to see estimated height
3. Calculate calibration factor
4. Re-process with adjusted reference height

```bash
# If actual height is 175cm but estimates 165cm
# Adjust reference height up by ~10cm
python main.py video.mp4 --reference-height 180
```

## Technical Details

### Video Window Properties

- **Title:** "AI Video Detector" or "Live Webcam AI Analyzer"
- **Size:** Matches video resolution
- **Frame Rate:** Matches source video (may be slower due to processing)
- **Format:** RGB color display

### Processing Pipeline

1. Frame capture from video/camera
2. MediaPipe pose detection
3. Attribute analysis (height, colors)
4. Overlay rendering
5. Display to window
6. Optional save to file

### Display Latency

- **Video files:** Minimal (<50ms typical)
- **Webcam:** ~100-300ms depending on system
- **Processing speed:** 5-15 FPS on modern CPU

## Related Documentation

- [README.md](README.md) - Main documentation
- [DOCUMENTATION.md](DOCUMENTATION.md) - Complete technical docs
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - More examples
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference

## Getting Help

If you're still having issues with real-time viewing:

1. Check that dependencies are installed: `pip install -r requirements.txt`
2. Verify OpenCV can display windows: `python -c "import cv2; cv2.namedWindow('test'); cv2.waitKey(1000)"`
3. Try the test script: `python test_analyzer.py`
4. Review error messages in the terminal
5. Check [SETUP.md](SETUP.md) for installation issues

---

**Note:** Real-time display requires a graphical environment. It won't work on headless servers or SSH sessions without X11 forwarding. Use `--no-display` for server environments.
