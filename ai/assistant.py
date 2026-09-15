import subprocess


class Assistant:
    def __init__(self):
        self.llama = "llama-mtmd-cli"
        self.model = "ggml-org/SmolVLM-256M-Instruct-GGUF:Q8_0"

    def ask(self, image_path, question):
        prompt = f"""Answer the user's question using only what is clearly visible in the image.
Keep the answer short.
Do not guess details that you cannot see clearly.
If you are unsure, say that you are not sure.

Question: {question}"""

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

        return result.stdout.strip()