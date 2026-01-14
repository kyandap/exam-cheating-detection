import cv2

FONT = cv2.FONT_HERSHEY_DUPLEX

def draw_status(frame, text, color, x=20, y=40, scale=0.9):
    # shadow
    cv2.putText(frame, text, (x+2, y+2), FONT, scale, (0,0,0), 3, cv2.LINE_AA)
    # main text
    cv2.putText(frame, text, (x, y), FONT, scale, color, 2, cv2.LINE_AA)

def draw_top_bar(frame, text, color):
    h, w, _ = frame.shape
    cv2.rectangle(frame, (0, 0), (w, 45), (0, 0, 0), -1)
    cv2.putText(
        frame,
        text,
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2,
        cv2.LINE_AA
    )


