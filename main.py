import cv2
import asyncio

from cv_engine.trackers import CamManager

cam = CamManager(0, "production")
async def camera():
    while True:
        frame = cam.StartCam()
        cv2.imshow("frame", frame)
        if (cv2.waitKey(1) & 0xFF) == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(camera())