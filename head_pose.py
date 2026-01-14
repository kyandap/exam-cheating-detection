import numpy as np
from collections import deque

class HeadPoseEstimator:
    def __init__(self, smooth_window=7):
        self.yaw_buffer = deque(maxlen=smooth_window)
        self.pitch_buffer = deque(maxlen=smooth_window)

    def estimate(self, landmarks, frame_shape):
        h, w = frame_shape[:2]

        nose = landmarks[1]
        forehead = landmarks[10]
        chin = landmarks[152]
        left_cheek = landmarks[234]
        right_cheek = landmarks[454]

        nose_x = nose.x * w
        nose_y = nose.y * h

        left_x = left_cheek.x * w
        right_x = right_cheek.x * w

        forehead_y = forehead.y * h
        chin_y = chin.y * h

        face_width = right_x - left_x
        face_center_x = left_x + face_width / 2

        raw_yaw = ((nose_x - face_center_x) / face_width) * 100

        face_height = chin_y - forehead_y
        face_center_y = forehead_y + face_height / 2

        raw_pitch = ((nose_y - face_center_y) / face_height) * 100

        self.yaw_buffer.append(raw_yaw)
        self.pitch_buffer.append(raw_pitch)

        yaw = np.mean(self.yaw_buffer)
        pitch = np.mean(self.pitch_buffer)

        roll = 0
        return pitch, yaw, roll
