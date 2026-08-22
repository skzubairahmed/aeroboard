import cv2
import numpy as np

class SimpleKalmanFilter2D():
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array(
            [[1,0,0,0], [0,1,0,0]], np.float32
        )
        self.kf.transitionMatrix = np.array(
            [[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]], np.float32
        )

        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.5

        self.initialized = False

    def smooth(self, x, y):
        measurement = np.array([np.float32(x), np.float32(y)], np.float32)

        if not self.initialized:
            self.kf.statePre = np.array(
                [[np.float32(x)], [np.float32(y)], [0], [0]], np.float32
            )

            self.initialized = True