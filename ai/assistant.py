import subprocess


class Assistant:
    def __init__(self):
        self.llama = "llama-mtmd-cli"
        self.model = "ggml-org/SmolVLM-256M-Instruct-GGUF:Q8_0"
        self.history = []

    def ask(self, image_path, question):
        conversation = ""

        for old_question, old_answer in self.history[-5:]:
            conversation += f"User: {old_question}\n"
            conversation += f"Assistant: {old_answer}\n"

        prompt = f"""You are a voice assistant running locally on a laptop.

Use the webcam image to understand what the user can currently see.
Use the previous conversation to understand follow-up questions.

Keep your answers short and natural.
Do not guess visual details that are not clearly visible.

Previous conversation:
{conversation}

User: {question}
Assistant:"""

        command = [
            self.llama,
            "-hf",
            self.model,
            "--image",
            image_path,
            "-p",
            prompt,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        answer = result.stdout.strip()

        if answer:
            self.history.append((question, answer))

        return answer