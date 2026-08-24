import cv2

from trackers import Tracker
from loggers import Logger
from filters import SimpleKalmanFilter2D
from gestures import Gestures

class Aeroboard():
    def __init__(self, camera_idx, logfile_path):
        self.cam = None
        self.camera_idx = camera_idx
        self.logger = Logger(logfile_path)
        self.frame = None
        self.ret = None
        self.last_frame = None

        self.fingertip_filters = {
            4: SimpleKalmanFilter2D(),
            8: SimpleKalmanFilter2D(),
            12: SimpleKalmanFilter2D(),
            16: SimpleKalmanFilter2D(),
            20: SimpleKalmanFilter2D()
        }

        self.gestures = Gestures()

    def start_loop(self):
        self.cam = Tracker(self.camera_idx)
        window_name = "Original feed"
        window = cv2.namedWindow(window_name)
        while True:
            try:
                self.frame, self.ret, message = self.cam.getFrame()

                if not self.ret:
                    cv2.imshow(window_name, self.last_frame)
                    self.logger.logData("RET_NOT", "Return value from camera was false.")
                    self.cam.cap.release()
                    self.cam = Tracker(self.camera_idx)
                    continue
                elif self.frame is None:
                    cv2.imshow(window_name, self.last_frame)
                    self.logger.logData("FRAME_NONE", "Value of frame is None.")
                    self.cam.cap.release()
                    self.cam = Tracker(self.camera_idx)
                    continue
                elif self.frame.size == 0:
                    cv2.imshow(window_name, self.last_frame)
                    self.logger.logData("FRAME_0x0", "Frame size is 0x0")
                    self.cam.cap.release()
                    self.cam = Tracker(self.camera_idx)
                    continue
                else:
                    self.last_frame = self.frame.copy()

                dup_frame = self.frame.copy()
                lm_points = self.cam.detectHand(self.frame, draw=True)
                
                fingertip_indices = [4, 8, 12, 16, 20]
                if lm_points is not None:
                    print(self.gestures.knowGesture(lm_points))
                    for idx in fingertip_indices:
                        raw_x = lm_points[idx][0]
                        raw_y = lm_points[idx][1]

                        smooth_x, smooth_y = self.fingertip_filters[idx].smooth(raw_x, raw_y)

                        cv2.circle(self.frame, (smooth_x, smooth_y), 10, (0,0,225), 3)
                        cv2.circle(self.frame, (smooth_x, smooth_y), 6, cv2.FILLED)

                        cv2.circle(dup_frame, (raw_x, raw_y), 10, (0,0,225), 3)
                        cv2.circle(dup_frame, (raw_x, raw_y), 6, cv2.FILLED)

                #print(lm_points)
                cv2.imshow(window_name, self.frame)
                cv2.imshow("Duplicate feed(NO FILTER)", dup_frame)

                key = (cv2.waitKey(1) & 0xFF)
                if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break

            except Exception as e:
                self.logger.logData("PYTHON_INTERNAL_EXCEPTION", f"{e.args}")
                cv2.imshow(window_name, self.last_frame)

        cv2.destroyAllWindows()
        self.cam.cap.release()

    def end_loop(self):
        self.cam.cap.release()
        cv2.destroyAllWindows()


ab = Aeroboard(0, "test_logfile.txt")
if __name__ == "__main__":
    ab.start_loop()