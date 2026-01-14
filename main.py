import cv2
import os
import pygame
import time

from face_detector import FaceDetector
from head_pose import HeadPoseEstimator
from eye_gaze import EyeGazeDetector
from cheat_detector import CheatDetector
from utils import draw_status, draw_top_bar

# =====================
# SETUP PATH
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================
# SAVE EVIDENCE
# =====================
def save_cheating_evidence(frame, reason, count):
    evidence_dir = os.path.join(BASE_DIR, "evidence", "cheating")
    os.makedirs(evidence_dir, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    filename = f"cheat_{count}_{int(time.time())}.jpg"
    path = os.path.join(evidence_dir, filename)

    img = frame.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(img, "CHEATING DETECTED", (20, 40),
                font, 1.0, (0, 0, 255), 3)

    cv2.putText(img, f"Reason: {reason}", (20, 80),
                font, 0.8, (0, 0, 255), 2)

    cv2.putText(img, f"Warning Count: {count}", (20, 115),
                font, 0.8, (0, 0, 255), 2)

    cv2.putText(img, f"Time: {timestamp}", (20, 150),
                font, 0.7, (255, 255, 255), 2)

    cv2.imwrite(path, img)

# =====================
# SOUND
# =====================
pygame.mixer.init()
sound_path = os.path.join(BASE_DIR, "sounds", "warning.wav")
warning_sound = pygame.mixer.Sound(sound_path)

def warning_beep():
    warning_sound.play()

# =====================
# CAMERA & MODELS
# =====================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    exit()

face_detector = FaceDetector(max_faces=1)
pose_estimator = HeadPoseEstimator()
eye_gaze = EyeGazeDetector()
cheat_detector = CheatDetector()

# =====================
# STATE VARIABLES
# =====================
last_warning_count = 0
cheat_start_time = None
CHEAT_DELAY = 2.0  # detik sebelum cheating dianggap valid

# =====================
# MAIN LOOP
# =====================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    faces = face_detector.detect(frame)

    if faces:
        face = faces[0]

        pitch, yaw, roll = pose_estimator.estimate(
            face.landmark, frame.shape
        )

        x_ratio, y_ratio = eye_gaze.detect(
            face.landmark, frame.shape
        )

        raw_cheating, reason, count = cheat_detector.check(
            yaw, pitch, len(faces), x_ratio, y_ratio
        )

        # =====================
        # CHEAT DELAY LOGIC
        # =====================
        cheating = False
        if raw_cheating:
            if cheat_start_time is None:
                cheat_start_time = time.time()
            elif time.time() - cheat_start_time >= CHEAT_DELAY:
                cheating = True
        else:
            cheat_start_time = None

        # =====================
        # TOP STATUS BAR
        # =====================
        if cheating:
            draw_top_bar(frame, "STATUS: CHEATING DETECTED", (0, 0, 255))
        else:
            draw_top_bar(frame, "STATUS: MONITORING", (0, 255, 0))

        # =====================
        # HIGHLIGHT AREA
        # =====================
        if cheating:
            if "EYE" in reason:
                cv2.rectangle(frame, (200, 180), (440, 300), (0, 0, 255), 2)
            elif "HEAD" in reason:
                cv2.rectangle(frame, (180, 120), (460, 360), (0, 0, 255), 2)

        # =====================
        # EXAM STATUS
        # =====================
        if count >= 5:
            exam_status = "EXAM FLAGGED"
            exam_color = (0, 0, 255)
        elif count >= 3:
            exam_status = "SERIOUS WARNING"
            exam_color = (0, 165, 255)
        else:
            exam_status = "WARNING"
            exam_color = (0, 255, 255)
