import tempfile

import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


class Listener:
    def __init__(self):
        self.sample_rate = 16000
        self.model = WhisperModel("small.en", device="cpu", compute_type="int8")
        

    def listen(self, seconds=5):
        print("Listening...")

        audio = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
        )

        sd.wait()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as file:
            write(file.name, self.sample_rate, audio)
            audio_file = file.name

        segments, _ = self.model.transcribe(
            audio_file,
            language="en",
            beam_size=5,
            vad_filter=True,
        )

        text = " ".join(segment.text.strip() for segment in segments)

        return text


if __name__ == "__main__":
    listener = Listener()
    text = listener.listen()

    print("You:", text)