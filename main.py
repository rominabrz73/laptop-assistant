import cv2
import threading
import time

from camera.webcam import Webcam
from speech.listener import Listener
from speech.speaker import Speaker
from ai.assistant import Assistant


camera = Webcam()
listener = Listener()
assistant = Assistant()
speaker = Speaker()

running = True
talk_requested = False


def show_camera():
    global running, talk_requested

    while running:
        frame = camera.capture()

        if frame is not None:
            cv2.imshow("Laptop Assistant", frame)

        key = cv2.waitKey(1)

        if key == 32:  # Space
            talk_requested = True

        elif key == 27:  # ESC
            running = False

        time.sleep(0.01)

    cv2.destroyAllWindows()


camera_thread = threading.Thread(target=show_camera, daemon=True)
camera_thread.start()

print("Laptop Assistant is ready.")
print("Camera is live.")
print("Press SPACE to talk.")
print("Press ESC to quit.")


while running:
    if talk_requested:
        talk_requested = False

        question = listener.listen()
        print("You:", question)

        if not question.strip():
            print("I didn't hear anything.")
            continue

        frame = camera.capture()

        if frame is None:
            print("Could not get camera frame.")
            continue

        cv2.imwrite("capture.jpg", frame)

        print("Thinking...")
        answer = assistant.ask("capture.jpg", question)

        print("Assistant:", answer)
        speaker.say(answer)

        print("\nPress SPACE to talk again.")

    time.sleep(0.05)


running = False
camera.close()
camera_thread.join(timeout=1)