# Left Arm Bicep Curl Counter (AI Pose Estimation)

## Overview
This project is a computer vision-based fitness tracker that counts **left-arm bicep curls** using pose estimation. It uses MediaPipe-based pose detection (via a custom PoseModule) to track key body joints and calculate elbow angles in real time.

The system detects workout motion, computes joint angles, and counts repetitions using a stable state-machine approach with smoothing for noise reduction.

---

## Features
- Left arm bicep curl counting
- Real-time pose detection
- Elbow angle calculation
- Smooth angle filtering (noise reduction)
- Robust rep counting using state machine logic
- Progress bar visualization
- FPS display for performance monitoring
- Works with webcam or video file input

---

## Tech Stack
- Python
- OpenCV
- NumPy
- MediaPipe (via PoseModule)

---

## How It Works
1. Captures video input from webcam or file
2. Detects human pose using PoseModule
3. Extracts left shoulder, elbow, and wrist landmarks
4. Calculates elbow angle using geometric method
5. Converts angle into movement percentage
6. Uses a state machine to detect full curl motion:
   - Arm down → Arm up → Arm down = 1 rep
7. Displays live feedback including:
   - Repetition count
   - Angle value
   - Progress bar
   - FPS

---

## Key Landmarks Used
Left Arm:
- Shoulder → 11
- Elbow → 13
- Wrist → 15

---

## Installation

Install dependencies:

```bash
pip install opencv-python numpy mediapipe
