from collections import deque
from platform import system
import cv2
import numpy as np

from trackers import Tracker
from filters import SimpleKalmanFilter2D
from gestures import Gestures
from loggers import Logger
from AirButton import AirButton

class AeroBoard:
    def __init__(self, cam_idx: int, logfile_path: str, draw_handbox: bool, window_name: str = "AeroBoard alpha-v0.1"):
        self.cam_idx = cam_idx
        self.logfile_path = logfile_path
        self.draw_handbox = draw_handbox

        self.draw_points = deque([])
        self.current_color = (0, 0, 255)
        self.current_gesture_set = None

        self.tracker = None
        self.gestures = Gestures()
        self.logger = Logger(logfile_path)

        self.fingertip_filters = {
            4: SimpleKalmanFilter2D(),
            8: SimpleKalmanFilter2D(),
            12: SimpleKalmanFilter2D(),
            16: SimpleKalmanFilter2D(),
            20: SimpleKalmanFilter2D()
        }

        self.device = system()
        self.window_name = window_name

        self.frame = None
        self.last_frame = None
        self.ret = False
        self.blank_frame = None  

        self.clear_btn = AirButton(0, 0, 100, 40, "Clear")
        self.red_btn = AirButton(100, 0, 100, 40, "RED")
        self.blue_btn = AirButton(200, 0, 100, 40, "BLUE")
        self.green_btn = AirButton(300, 0, 100, 40, "GREEN")
        self.clear_cooldown = 0
        self.red_cooldown = 0
        self.green_cooldown = 0
        self.blue_cooldown = 0

        self.strokes = ([])
        self.current_stroke = []
        self.is_drawing = False
        self.was_drawing = False

    def start_loop(self):
        self.tracker = Tracker(self.cam_idx, self.device)
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_GUI_EXPANDED)

        while True:
            try:
                self.frame, self.ret, message = self.tracker.getFrame()
                
                if self.ret is False or self.frame is None:
                    self.logger.logData("TRACKER_ERROR", "Frame retrieval failed or returned None.")
                    if self.last_frame is not None:
                        cv2.imshow(self.window_name, self.last_frame)
                    
                    self.tracker.cap.release()
                    self.tracker = Tracker(self.cam_idx, self.device)
                    continue

                if self.blank_frame is None:
                    h, w, _ = self.frame.shape
                    self.blank_frame = np.zeros((h, w, 3), dtype=np.uint8)

                lm_points = self.tracker.detectHand(self.frame, draw=self.draw_handbox)

                fingertip_indices = [4, 8, 12, 16, 20]
                if lm_points is not None:
                    self.current_gesture_set = self.gestures.knowGesture(lm_points)
                    ti_dist = self.current_gesture_set[1]
                    current_gesture = self.current_gesture_set[0]
                    for idx in fingertip_indices:
                        raw_x = lm_points[idx][0]
                        raw_y = lm_points[idx][1]

                        smooth_x, smooth_y = self.fingertip_filters[idx].smooth(raw_x, raw_y)

                        if idx == 8 and current_gesture == "POINTER":
                            cv2.circle(self.frame, (smooth_x, smooth_y), 8, (0, 0, 255), 2)
                            cv2.circle(self.frame, (smooth_x, smooth_y), 6, (255, 0, 0), cv2.FILLED)
                        elif current_gesture == "PEN":
                            if idx == 4 or idx == 8:
                                cv2.circle(self.frame, (smooth_x, smooth_y), 8, (0, 0, 255), 2)
                                cv2.circle(self.frame, (smooth_x, smooth_y), 6, (0, 255 ,255), cv2.FILLED)

                self.clear_btn.draw((255,100,0), self.frame)
                self.red_btn.draw((0,0,255), self.frame)
                self.green_btn.draw((0,255,0), self.frame)
                self.blue_btn.draw((255,0,0), self.frame)

                if lm_points is not None and lm_points[8] is not None:
                    if self.clear_btn.check_collision(self.fingertip_filters[8].smooth(lm_points[8][0], lm_points[8][1])):
                        if self.clear_cooldown == 0:
                            self.strokes.clear()
                            self.clear_cooldown = 30
                    if self.red_btn.check_collision(self.fingertip_filters[8].smooth(lm_points[8][0], lm_points[8][1])):
                        if self.red_cooldown == 0:
                            self.current_color = (0,0,255)
                            self.red_btn.is_selected = not self.red_btn.is_selected
                            self.blue_btn.is_selected = False
                            self.green_btn.is_selected = False
                            self.red_cooldown = 30
                    if self.green_btn.check_collision(self.fingertip_filters[8].smooth(lm_points[8][0], lm_points[8][1])):
                        if self.green_cooldown == 0:
                            self.current_color = (0,255,0)
                            self.green_btn.is_selected = not self.green_btn.is_selected
                            self.red_btn.is_selected = False
                            self.blue_btn.is_selected = False
                            self.green_cooldown = 30
                    if self.blue_btn.check_collision(self.fingertip_filters[8].smooth(lm_points[8][0], lm_points[8][1])):
                        if self.blue_cooldown == 0:
                            self.current_color = (255,0,0)
                            self.blue_btn.is_selected = not self.blue_btn.is_selected
                            self.red_btn.is_selected = False
                            self.green_btn.is_selected = False
                            self.blue_cooldown = 30

                    if self.current_gesture_set[0] == "PEN":
                        self.is_drawing = True
                    else:
                        self.is_drawing = False
                    print(self.is_drawing)

                    index_x, index_y = self.fingertip_filters[8].smooth(lm_points[8][0], lm_points[8][1])

                    if self.is_drawing:
                        self.current_stroke.append((index_x, index_y))
                        self.was_drawing = True
                    else:
                        if self.was_drawing and len(self.current_stroke) > 0:
                            self.strokes.append({
                                "points": list(self.current_stroke),
                                "color": self.current_color,
                            })
                        self.current_stroke.clear()
                        self.was_drawing = False

                
                    print(self.strokes)

                    self.clear_cooldown = max(0, self.clear_cooldown - 1)
                    self.red_cooldown = max(0, self.red_cooldown - 1)
                    self.green_cooldown = max(0, self.green_cooldown - 1)
                    self.blue_cooldown = max(0, self.blue_cooldown - 1)

                for stroke in self.strokes:
                    points = stroke["points"]
                    color = stroke["color"]
                
                    if len(points) < 2:
                        continue
                
                    for i in range(1, len(points)):
                        pt1 = points[i - 1]
                        pt2 = points[i]
                        if pt1 is not None and pt2 is not None:
                            cv2.line(self.frame, pt1, pt2, color=color, thickness=2)
                
                        if len(self.current_stroke) > 1:
                            for i in range(1, len(self.current_stroke)):
                                pt1 = self.current_stroke[i - 1]
                                pt2 = self.current_stroke[i]
                                if pt1 is not None and pt2 is not None:
                                    cv2.line(
                                        self.frame,
                                        pt1,
                                        pt2,
                                        color=self.current_color,
                                        thickness=2,
                                    )

                self.last_frame = self.frame.copy()

                cv2.imshow(self.window_name, self.frame)

                key = cv2.waitKey(1) & 0xFF
                window_visible = cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE)
                
                if key == 27 or window_visible < 1:
                    break

            except Exception as e:
                self.logger.logData("PYTHON_INTERNAL_ERROR", str(e))

        self.end_loop()

    def end_loop(self):
        if self.tracker is not None and hasattr(self.tracker, 'cap') and self.tracker.cap is not None:
            self.tracker.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = AeroBoard(0, "test_logs.txt", False)
    app.start_loop()