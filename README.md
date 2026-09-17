# Laptop Assistant

A lightweight local voice and vision assistant that treats a laptop as a simple smart embodiment:

- **Webcam** as eyes
- **Microphone** as ears
- **Speaker** as voice

The assistant can listen to spoken questions, answer general questions, use the webcam for simple visual questions, remember explicitly provided information, and reply through the laptop speaker.

## How It Works

The interaction flow is:

```text
Microphone → Speech-to-Text → Assistant → Response → Speaker
                                  │
                         ┌────────┴────────┐
                         │                 │
                    Visual question   General question
                         │                 │
                      Webcam          Llama 3.2 1B
                         │
                    SmolVLM-500M
```

The assistant uses lightweight phrase-based routing to distinguish simple visual questions from general conversation.

For visual questions, the current webcam frame and the question are passed to SmolVLM-500M. General questions are handled by Llama 3.2 1B.

This lightweight approach keeps response time practical on the CPU-based development hardware.

## Models and Tools

- **Speech recognition:** faster-whisper (`small.en`)
- **Vision:** SmolVLM-500M-Instruct-GGUF
- **Conversation:** Llama 3.2 1B Instruct GGUF
- **Local inference:** llama.cpp
- **Camera:** OpenCV
- **Speech output:** pyttsx3

The models are downloaded on first use. After the required models are available locally, inference does not require a cloud AI service.

llama.cpp is used because the prototype was developed and tested on a CPU-only Windows laptop with limited memory.

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/rominabrz73/laptop-assistant.git
cd laptop-assistant
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the Python dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install llama.cpp

On Windows:

```powershell
winget install llama.cpp
```

The first run may take longer while the required models are downloaded.

## Run

```powershell
python main.py
```

When the camera window opens:

- Press **Space** to talk.
- Ask a question.
- The assistant will display and speak its response.
- Press **Space** again for another question.
- Press **ESC** to exit.

Example questions:

```text
What is Python?
What is in my hand?
What colour is this?
How many objects can you see?
```

You can also store simple information:

```text
Remember that my name is Alex.
```

The assistant keeps a short conversation history and can use saved information when relevant.

## Project Structure

```text
laptop-assistant/
├── ai/
│   ├── assistant.py
│   ├── chat.py
│   └── memory.py
├── camera/
│   └── webcam.py
├── speech/
│   ├── listener.py
│   └── speaker.py
├── main.py
├── requirements.txt
└── README.md
```

## Limitations

This is a lightweight prototype designed for local CPU execution.

Visual understanding is currently intended for simple questions about clearly visible objects, colours, quantities, and basic scene information. Speech and visual accuracy can vary depending on microphone quality, lighting, camera view, and available hardware.
