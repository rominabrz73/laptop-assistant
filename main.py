import cv2

from camera.webcam import Webcam


camera = Webcam()

print("Camera is running. Press ESC to quit.")

while True:
    frame = camera.capture()
    cv2.imshow("Laptop Assistant", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

camera.close()
cv2.destroyAllWindows()