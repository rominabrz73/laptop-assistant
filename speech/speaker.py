import pyttsx3


class Speaker:
    def say(self, text):
        if not text.strip():
            return

        engine = pyttsx3.init("sapi5")
        engine.setProperty("volume", 1.0)
        engine.setProperty("rate", 160)

        engine.say(text)
        engine.runAndWait()
        engine.stop()