import cv2
import time

class Tracker:
    def __init__(self, camera_idx:int = 0):
        self.camera_idx = camera_idx
        self.frame = None
        self.cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)

        self.prev_time = time.time()
        self.smoothed_fps = 0

        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
        #self.cap.set(cv2.CAP_PROP_SETTINGS, 1)

    def showFrames(self): #for demo/tests
        window_name = "Original Frame"
        cv2.namedWindow(window_name)

        try:
            while True:
                ret, self.frame = self.cap.read()
                
                if not ret:
                    return None, "Unable to read camera."
                
                self.frame = cv2.flip(self.frame, 1)
                key = (cv2.waitKey(1) & 0xFF)

                self.frame = self.processHands(self.frame)
                cv2.imshow(window_name, self.frame)
                
                if key == 27:
                    break
                
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
            cv2.destroyAllWindows()
            self.cap.release()

        except Exception as e:
            return f"An error occured: {e}"

    def getFrame(self):
        try:
            ret, self.frame = self.cap.read()
            
            if not ret or self.frame is None or self.frame.size == 0:
                return None, False, "Failed to get valid frame."

            self.frame = cv2.flip(self.frame, 1)
            return self.frame, ret, "success"

        except Exception as e:
            return None, f"An error occured: {e}"

    def addFps(self, frame):
        try:
            curr_time = time.time()
            time_diff = curr_time - self.prev_time
            self.prev_time = curr_time
            
            if time_diff > 0:
                instant_fps = 1 / time_diff
                self.smoothed_fps = (self.smoothed_fps * 0.9) + (instant_fps * 0.1)

            fps_text = f"FPS: {int(self.smoothed_fps)}"
            cv2.putText(
                frame,
                fps_text,
                (20, 50),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (255, 0, 0),
                2
            )
            return frame
        except Exception as e:
            return "Unable to put FPS."