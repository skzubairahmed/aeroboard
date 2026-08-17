import cv2

class Tracker:
    def __init__(self, camera_idx:int = 0):
        self.camera_idx = camera_idx
        self.frame = None
        self.cap = cv2.VideoCapture(camera_idx, )

    def showFrames(self): #for demo/tests
        window_name = "Original Frame"
        cv2.namedWindow(window_name)

        try:
            while True:
                ret, self.frame = self.cap.read()
                
                if not ret:
                    return "Unable to read camera."
                
                self.frame = cv2.flip(self.frame, 1)
                key = (cv2.waitKey(1) & 0xFF)
                
                cv2.imshow(window_name, self.frame)
                
                if key == 27:
                    break
                
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
            cv2.destroyAllWindows()
            self.cap.release()

        except Exception as e:
            return f"An error occured: {e}"


            

        