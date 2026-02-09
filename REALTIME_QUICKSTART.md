# Real-Time Viewing Quick Start Card

## 🎬 Three Ways to View Videos in Real-Time

### 1️⃣ Standard Viewer
```bash
python main.py video.mp4
```
- Default option
- Full processing + statistics
- Real-time display enabled

### 2️⃣ Enhanced Viewer ⭐ RECOMMENDED
```bash
python realtime_viewer.py video.mp4
```
- Better user experience
- Clear instructions
- Emoji feedback
- Summary stats

### 3️⃣ Live Webcam 📹
```bash
python webcam_viewer.py
```
- Live camera feed
- Real-time AI analysis
- Screenshot capture

---

## ⌨️ Keyboard Controls

| Key | What It Does |
|-----|--------------|
| **Q** | Quit playback |
| **P** | Pause/Resume (video only) |
| **S** | Screenshot (webcam only) |

---

## 💡 What You'll See

```
┌────────────────────────────┐
│ Height: 172.5 cm          │ ← AI Analysis
│ Hair: Brown               │
│ Eyes: Blue                │
│ Clothing: Blue, White     │
│                           │
│   [Person with green      │ ← Pose Skeleton
│    skeleton overlaid]     │   + Red Dots
│                           │
└────────────────────────────┘
```

---

## 📖 Need More Help?

Read: [REALTIME_VIEWING.md](REALTIME_VIEWING.md)

---

## 🎯 Common Commands

```bash
# View any video
python realtime_viewer.py my_video.mp4

# View and save analyzed video
python realtime_viewer.py input.mp4 --save output.mp4

# Use webcam
python webcam_viewer.py

# Use external camera
python webcam_viewer.py --camera 1

# Custom height calibration
python realtime_viewer.py video.mp4 --reference-height 180
```

---

## ⚡ Quick Tips

- Video window appears automatically
- Press keys while window is focused
- Close other apps for better performance
- Use good lighting for best results

---

**That's it! Real-time viewing made easy!** 🚀
