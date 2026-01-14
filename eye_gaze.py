import numpy as np

class EyeGazeDetector:
    def __init__(self):
        pass

    def _eye_ratio(self, iris, eye_left, eye_right, eye_top, eye_bottom):
        # horizontal ratio
        eye_width = eye_right[0] - eye_left[0]
        iris_x = iris[0] - eye_left[0]
        x_ratio = iris_x / eye_width if eye_width != 0 else 0.5

        # vertical ratio
        eye_height = eye_bottom[1] - eye_top[1]
        iris_y = iris[1] - eye_top[1]
        y_ratio = iris_y / eye_height if eye_height != 0 else 0.5

        return x_ratio, y_ratio

    def detect(self, landmarks, frame_shape):
        h, w = frame_shape[:2]

        # Left eye
        left_eye_left   = landmarks[33]
        left_eye_right  = landmarks[133]
        left_eye_top    = landmarks[159]
        left_eye_bottom = landmarks[145]
        left_iris       = landmarks[468]

        # Right eye
        right_eye_left   = landmarks[362]
        right_eye_right  = landmarks[263]
        right_eye_top    = landmarks[386]
        right_eye_bottom = landmarks[374]
        right_iris       = landmarks[473]

        # Convert to pixel
        def to_pixel(lm):
            return np.array([lm.x * w, lm.y * h])

        lx_ratio, ly_ratio = self._eye_ratio(
            to_pixel(left_iris),
            to_pixel(left_eye_left),
            to_pixel(left_eye_right),
            to_pixel(left_eye_top),
            to_pixel(left_eye_bottom)
        )

        rx_ratio, ry_ratio = self._eye_ratio(
            to_pixel(right_iris),
            to_pixel(right_eye_left),
            to_pixel(right_eye_right),
            to_pixel(right_eye_top),
            to_pixel(right_eye_bottom)
        )

        # Average both eyes
        x_ratio = (lx_ratio + rx_ratio) / 2
        y_ratio = (ly_ratio + ry_ratio) / 2

        return x_ratio, y_ratio
