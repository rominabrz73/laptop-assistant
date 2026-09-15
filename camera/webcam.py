import cv2


class Webcam:
    def __init__(self):
        # Use the default webcam
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            raise RuntimeError("Could not open webcam")

    def capture(self):
        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("Could not capture image")

        return frame

    def close(self):
        self.camera.release()