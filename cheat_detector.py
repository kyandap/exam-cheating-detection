class CheatDetector:
    def __init__(self):
        self.warning_count = 0
        self.cheat_frame_count = 0
        self.frame_threshold = 60
        self.already_warned = False

    def check(self, yaw, pitch, face_count, eye_x, eye_y):
        cheating = False
        reason = "NORMAL"

        if face_count == 0:
            cheating = True
            reason = "NO FACE"

        elif face_count > 1:
            cheating = True
            reason = "MULTIPLE FACES"

        # HEAD POSE
        elif abs(yaw) > 40:
            cheating = True
            reason = "LOOKING SIDE (HEAD)"

        elif pitch > 15:
            cheating = True
            reason = "LOOKING DOWN (HEAD)"

        # EYE GAZE 
        elif eye_x < 0.42:
            cheating = True
            reason = "EYES LEFT"

        elif eye_x > 0.65:
            cheating = True
            reason = "EYES RIGHT"

        elif eye_y > 0.6:
            cheating = True
            reason = "EYES DOWN"

        if cheating:
            self.cheat_frame_count += 1

            if self.cheat_frame_count >= self.frame_threshold and not self.already_warned:
                self.warning_count += 1
                self.already_warned = True
        else:
            self.cheat_frame_count = 0
            self.already_warned = False

        return cheating, reason, self.warning_count
