import cv2

class AirButton():
    def __init__(self, x, y, w, h, label):
        self.rect = (x, y, w, h)
        self.label = label
        self.is_selected = False

    def check_collision(self, fingertip_pos):
        if fingertip_pos is None:
            return False

        fx, fy = fingertip_pos
        x, y, w, h = self.rect

        if x <= fx <= x + w and y <= fy <= y + h:
            return True

        return False

    def draw(self, bg_color:tuple, frame):
        x, y, w, h = self.rect

        border_color = (0, 255, 255) if self.is_selected else (0, 0, 0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), bg_color, -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(self.label, font, 0.5, 1)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2

        cv2.putText(frame, self.label, (text_x, text_y), font, 0.6, (255, 255, 255), 1)