import cv2
import threading
import time


class Webcam:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            raise RuntimeError("Could not open webcam")

        self.frame = None
        self.running = True
        self.lock = threading.Lock()

        self.capture_thread = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )
        self.capture_thread.start()

    def _capture_loop(self):
        while self.running:
            success, frame = self.camera.read()

            if success:
                with self.lock:
                    self.frame = frame

            time.sleep(0.01)

    def capture(self):
        with self.lock:
            if self.frame is None:
                return None

            return self.frame.copy()

    def close(self):
        self.running = False
        self.capture_thread.join(timeout=1)
        self.camera.release()