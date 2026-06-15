# Smart-Bicep-CurlTracker
This project is an AI-powered Fitness Trainer using Computer Vision and MediaPipe Pose Estimation to track human body movements in real-time. It detects key joints (shoulder, elbow, wrist), calculates angles, and counts bicep curls for both arms with live feedback and visualization.

## Features
- Real-time human pose detection
- Left and right arm tracking
- Automatic bicep curl counting
- Angle-based motion analysis
- Live FPS display
- Visual feedback with progress indicators
- Works with webcam or video input

## Tech Stack
- Python
- OpenCV
- MediaPipe
- NumPy

## How It Works
1. Captures video from webcam or file
2. Detects human pose using MediaPipe
3. Extracts key landmarks (shoulder, elbow, wrist)
4. Calculates elbow joint angle
5. Converts angle into movement percentage
6. Counts repetitions for both arms
7. Displays results in real time

## Project Structure
AI-Fitness-Trainer/
├── PoseModule.py     # Pose detection module
├── main.py           # Curl counting logic
├── curls.mp4         # Sample video input
└── README.md

## Installation
pip install opencv-python mediapipe numpy

## Usage
python main.py

## Key Landmarks Used
Left Arm: 11 (Shoulder), 13 (Elbow), 15 (Wrist)
Right Arm: 12 (Shoulder), 14 (Elbow), 16 (Wrist)

## Output
- Real-time curl count for both arms
- Angle visualization
- Movement progress tracking
- FPS monitoring

## Future Improvements
- Posture correction system
- Rep quality scoring
- Exercise form detection
- Mobile deployment
- Workout history tracking

## Applications
- Personal fitness tracking
- AI gym trainer systems
- Sports rehabilitation
- Human motion analysis
