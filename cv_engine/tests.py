import cv2

from trackers import Tracker
from loggers import Logger

class Aeroboard():
    def __init__(self, camera_idx, logfile_path):
        self.cam = None
        self.camera_idx = camera_idx
        self.logger = Logger(logfile_path)
        self.frame = None
        self.ret = None
        self.last_frame = None

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
                    self.last_frame = self.frame

                dup_frame = self.frame.copy()
                lm_points = self.cam.detectHand(self.frame, draw=False)
                
                if lm_points is not None:
                    for point in lm_points:
                        x = point[0]
                        y = point[1]
                        cv2.circle(self.frame, (x, y), 10, (0, 0, 255), 2)
                        cv2.circle(self.frame, (x, y), 8, (0, 255, 0), cv2.FILLED)
                print(lm_points)
                cv2.imshow(window_name, self.frame)

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