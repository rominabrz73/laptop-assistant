# Laptop Assistant

A lightweight local assistant that uses the laptop's webcam, microphone and speaker for voice and visual interaction.

The user can show an object to the webcam, press Space and ask a question. The system captures the current camera view, converts the spoken question to text, processes the image and question locally, and gives a spoken response.

## How it works

The project uses:

- OpenCV for webcam input
- faster-whisper for speech recognition
- SmolVLM-256M for image understanding
- llama.cpp for local model inference
- pyttsx3 for voice output

The current flow is:

```text
Webcam + Microphone
        ↓
Image + Spoken Question
        ↓
faster-whisper
        ↓
SmolVLM-256M
        ↓
Answer
        ↓
Laptop Speaker
```

## Local Model

The prototype is designed to run on a CPU-only laptop with limited memory.

SmolVLM-256M is used as a lightweight vision-language model and runs in quantised GGUF format through llama.cpp. A larger vision model was also tested during development, but inference was too slow on the available CPU hardware.

vLLM is not used in the current version because the development machine does not have a suitable NVIDIA GPU. llama.cpp provides a more practical option for local CPU inference.

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Install llama.cpp:

```powershell
winget install llama.cpp
```

The vision model used is:

```text
ggml-org/SmolVLM-256M-Instruct-GGUF:Q8_0
```

The model is downloaded automatically on first use.

## Run

```powershell
python main.py
```

When the camera opens:

- Press `Space` to capture the current view.
- Ask a question when the system starts listening.
- The answer will appear in the terminal and be spoken through the laptop speaker.
- Press `Space` again for another question.
- Press `ESC` to exit.

Example questions:

```text
What am I holding?
What can you see?
What is in front of the camera?
What is this?
What color is this?
```

## Limitations

SmolVLM-256M was selected to keep local inference practical on limited hardware. Because it is a small model, it can make mistakes when recognising fine visual details or reading small text.