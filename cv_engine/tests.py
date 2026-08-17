import cv2
from trackers import Tracker

cam = Tracker(0)
# cam.showFrames()

while True:
    frame, ret, message = cam.getFrame()
    if not ret:
        print("Received empty frame, skipping...")
        continue

    if frame.size == 0:
        print("Received frame of size 0x0, skipping...")
        continue
    cam.addFps(frame)
    cv2.imshow("original frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()