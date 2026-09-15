import cv2

from camera.webcam import Webcam
from speech.listener import Listener
from speech.speaker import Speaker
from ai.assistant import Assistant


camera = Webcam()
listener = Listener()
assistant = Assistant()
speaker = Speaker()

print("Camera is ready.")
print("Press SPACE to ask a question.")
print("Press ESC to quit.")

while True:
    frame = camera.capture()
    cv2.imshow("Laptop Assistant", frame)

    key = cv2.waitKey(1)

    if key == 32:  # Space
        frame = camera.capture()
        cv2.imwrite("capture.jpg", frame)
        print("Image captured.")

        question = listener.listen()
        print("You:", question)
        if not question.strip():
            print("I didn't hear anything.")
            continue

        print("Thinking...")
        answer = assistant.ask("capture.jpg", question)

        print("Assistant:", answer)
        speaker.say(answer)

    if key == 27:  # ESC
        break

camera.close()
cv2.destroyAllWindows()