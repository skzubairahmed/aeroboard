import cv2

class Tracker:
    def __init__(self, camera_idx:int = 0):
        self.camera_idx = camera_idx
        self.frame = None

    self.