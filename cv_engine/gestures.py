import numpy as np

class Gestures():
    def __init__(self):
        self.final_gesture = None

        self.gestures = {
            1:"PEN",
            2:"POINTER"
        }

    def knowGesture(self, lm_points):
        thumb_coord = lm_points[4]
        index_coord = lm_points[8]
        middle_coord = lm_points[12]
        ring_coord = lm_points[16]
        pinky_coord = lm_points[20]

        ti_dist = np.linalg.norm(np.array(thumb_coord) - np.array(index_coord))
        im_dist = np.linalg.norm(np.array(index_coord) - np.array(middle_coord))
        ir_dist = np.linalg.norm(np.array(index_coord) - np.array(ring_coord))
        ip_dist  = np.linalg.norm(np.array(index_coord) - np.array(pinky_coord))

        if ti_dist <= 25:
            self.final_gesture = self.gestures[1]
        elif ti_dist > 100 and  im_dist > 100 and ir_dist > 100 and ip_dist > 100:
            self.final_gesture = self.gestures[2]
        else:
            self.final_gesture = None

        return [self.final_gesture, ti_dist]