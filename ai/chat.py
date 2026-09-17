import subprocess


class Chat:
    def __init__(self):
        self.llama = "llama-cli"
        self.model = "bartowski/Llama-3.2-1B-Instruct-GGUF:Q4_K_M"

    def reply(self, question, context=""):
        prompt = f"""You are a voice assistant.
Always reply in English.
Even if the user's speech contains an unclear or foreign-looking word, reply in English.

Use the provided visual observation exactly as evidence.
Never add an object that is not mentioned in the visual observation.
If the visual observation says the user is holding an object, answer with that object.
Do not assume that the laptop itself is visible.
Ignore stored memory unless the current question specifically requires it.
Never mention the user's name or personal information unless the user asks about it.

Information:
{context}

CURRENT QUESTION: {question}

ANSWER:"""

        command = [
            self.llama,
            "-hf",
            self.model,
            "-p",
            prompt,
            "-n",
            "20",
            "--single-turn",
            "--no-display-prompt",
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
        )

        output = result.stdout

        # Remove llama.cpp statistics
        if "[ Prompt:" in output:
            clean_output = output.split("[ Prompt:", 1)[0]
        else:
            clean_output = output

        # Get the generated answer
        if "... (truncated)" in clean_output:
            answer = clean_output.rsplit(
                "... (truncated)", 1
            )[1].strip()
        else:
            lines = [
                line.strip()
                for line in clean_output.splitlines()
                if line.strip()
            ]

            if not lines:
                return ""

            answer = lines[-1]

        # Stop unwanted extra conversation
        if "\nUser:" in answer:
            answer = answer.split("\nUser:", 1)[0].strip()

        return answer