# Exam Cheating Detection System

A real-time online exam proctoring system built with computer vision to detect suspicious behaviors such as abnormal head movement, eye gaze deviation, and face absence using a webcam.

## Features
- Real-time face detection
- Head pose (yaw & pitch) estimation
- Eye gaze tracking
- Rule-based cheating detection with delay validation
- Warning escalation system
- Audio alerts for confirmed cheating
- Automatic screenshot evidence capture
- Clean proctoring-style UI overlay

## Tech Stack
- Python
- OpenCV
- MediaPipe
- Pygame

## How It Works
1. The system captures webcam input in real time.
2. Head pose and eye gaze are analyzed per frame.
3. Suspicious behavior is validated with a time delay.
4. Warnings are escalated and evidence is recorded.

## Run
