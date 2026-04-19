import cv2
import numpy as np

try:
    from mediapipe.python.solutions import drawing_utils as mp_drawing
    from mediapipe.python.solutions import hands as mp_hands
except ImportError as exc:
    raise RuntimeError(
        "This project needs the legacy MediaPipe Solutions API.\n"
        "Use Python 3.11 or 3.12 in a virtual environment and install:\n"
        "pip install -r requirements.txt\n"
        "Your current MediaPipe build does not include hand-tracking solutions."
    ) from exc


class VirtualAirWriter:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.mp_hands = mp_hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.drawer = mp_drawing

        self.canvas = None
        self.prev_point = None
        self.brush_color = (255, 0, 255)
        self.brush_thickness = 8
        self.eraser_thickness = 40

    def fingers_up(self, landmarks):
        tips = [4, 8, 12, 16, 20]
        fingers = []

        fingers.append(1 if landmarks[tips[0]].x < landmarks[tips[0] - 1].x else 0)

        for tip in tips[1:]:
            fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)

        return fingers

    def draw_header(self, frame, mode):
        color_box = (40, 40, 320, 120)
        cv2.rectangle(frame, (color_box[0], color_box[1]), (color_box[2], color_box[3]), (30, 30, 30), -1)

        colors = [
            ((255, 0, 255), (60, 60, 110, 110)),
            ((255, 0, 0), (120, 60, 170, 110)),
            ((0, 255, 0), (180, 60, 230, 110)),
            ((0, 255, 255), (240, 60, 290, 110)),
        ]

        for color, (x1, y1, x2, y2) in colors:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
            if self.brush_color == color:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        cv2.rectangle(frame, (350, 60), (460, 110), (80, 80, 80), -1)
        cv2.putText(frame, "ERASE", (365, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.rectangle(frame, (490, 60), (600, 110), (0, 0, 180), -1)
        cv2.putText(frame, "CLEAR", (505, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(
            frame,
            mode,
            (40, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
        )

    def handle_selection(self, x, y):
        if 60 <= x <= 110 and 60 <= y <= 110:
            self.brush_color = (255, 0, 255)
        elif 120 <= x <= 170 and 60 <= y <= 110:
            self.brush_color = (255, 0, 0)
        elif 180 <= x <= 230 and 60 <= y <= 110:
            self.brush_color = (0, 255, 0)
        elif 240 <= x <= 290 and 60 <= y <= 110:
            self.brush_color = (0, 255, 255)
        elif 350 <= x <= 460 and 60 <= y <= 110:
            self.brush_color = (0, 0, 0)
        elif 490 <= x <= 600 and 60 <= y <= 110 and self.canvas is not None:
            self.canvas[:] = 0

    def run(self):
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam.")

        while True:
            success, frame = self.cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)

            if self.canvas is None:
                self.canvas = np.zeros_like(frame)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)
            mode = "Show index finger to draw | Show index + middle fingers to select"

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.drawer.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark
                h, w, _ = frame.shape

                index_x, index_y = int(landmarks[8].x * w), int(landmarks[8].y * h)
                middle_x, middle_y = int(landmarks[12].x * w), int(landmarks[12].y * h)

                fingers = self.fingers_up(landmarks)

                if fingers[1] and fingers[2]:
                    self.prev_point = None
                    mode = "Selection mode"
                    cv2.rectangle(frame, (index_x, index_y - 25), (middle_x, middle_y + 25), self.brush_color, 2)
                    self.handle_selection(index_x, index_y)

                elif fingers[1] and not fingers[2]:
                    mode = "Drawing mode"
                    thickness = self.eraser_thickness if self.brush_color == (0, 0, 0) else self.brush_thickness

                    cv2.circle(
                        frame,
                        (index_x, index_y),
                        12,
                        (0, 0, 0) if self.brush_color == (0, 0, 0) else self.brush_color,
                        -1,
                    )

                    if self.prev_point is None:
                        self.prev_point = (index_x, index_y)

                    cv2.line(self.canvas, self.prev_point, (index_x, index_y), self.brush_color, thickness)
                    self.prev_point = (index_x, index_y)
                else:
                    self.prev_point = None
            else:
                self.prev_point = None

            gray_canvas = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
            canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
            output = cv2.add(frame_bg, canvas_fg)

            self.draw_header(output, mode)

            cv2.putText(output, "Press Q to quit", (980, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow("Virtual Air Writing", output)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = VirtualAirWriter()
    app.run()
