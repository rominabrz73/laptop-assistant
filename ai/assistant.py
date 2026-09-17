import subprocess

from ai.memory import Memory
from ai.chat import Chat


class Assistant:
    def __init__(self):
        self.vision_llama = "llama-mtmd-cli"
        self.vision_model = "ggml-org/SmolVLM-500M-Instruct-GGUF"

        self.memory = Memory()
        self.chat = Chat()
        self.history = []

    def is_visual_question(self, question):
        text = question.lower()

        visual_phrases = [
            "do you see",
            "can you see",
            "what do you see",
            "in the picture",
            "in the image",
            "in my hand",
            "i am holding",
            "i'm holding",
            "what am i holding",
            "what is this",
            "what's this",
            "what is that",
            "what's that",
            "what color",
            "what colour",
            "color of this",
            "colour of this",
            "how many hands",
            "how many fingers",
            "how many phones",
            "how many mobiles",
            "how many objects",
            "how many items",
            "my hair",
            "am i wearing",
            "behind me",
            "in front of me",
        ]

        return any(phrase in text for phrase in visual_phrases)

    def get_vision(self, image_path, question):
        prompt = f"""Look carefully at the image and answer this question:

{question}

Use only what is clearly visible in the image.
Answer only the visual question.
Keep the answer very short and factual.
Do not guess.

For a counting question, return only the number.
For a colour question, return only the colour.
For an object question, return only the object.
If you cannot determine the answer, say "I am not sure"."""

        command = [
            self.vision_llama,
            "-hf",
            self.vision_model,
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

    def make_visual_answer(self, question, vision):
        question_lower = question.lower()

        vision = vision.strip()

        if not vision:
            return "I'm not sure."

        if "i am not sure" in vision.lower():
            return "I'm not sure."

        # Remove the final full stop for easier formatting
        clean_vision = vision.rstrip(".").strip()

        # Counting questions
        if "how many" in question_lower:
            return f"I can see {clean_vision}."

        # Colour questions
        if "color" in question_lower or "colour" in question_lower:
            if "hair" in question_lower:
                return f"Your hair looks {clean_vision.lower()}."

            return f"It looks {clean_vision.lower()}."

        # Object questions
        object_phrases = [
            "what am i holding",
            "what is in my hand",
            "what's in my hand",
            "what is this",
            "what's this",
            "what is that",
            "what's that",
        ]

        if any(phrase in question_lower for phrase in object_phrases):
            return f"It looks like {clean_vision.lower()}."

        return vision

    def ask(self, image_path, question):
        text = question.strip()
        lower_text = text.lower().replace(",", "")

        memory_phrases = [
            "please remember that ",
            "please remember ",
            "remember that ",
            "remember ",
        ]

        # Save explicit memories
        for phrase in memory_phrases:
            if lower_text.startswith(phrase):
                fact = text[len(phrase):].strip()

                if fact:
                    self.memory.save(fact)

                    answer = "Okay, I'll remember that."
                    self.history.append((question, answer))

                    return answer

        # Visual question
        if self.is_visual_question(question):
            vision = self.get_vision(
                image_path,
                question,
            )

            print("VISION:", repr(vision))

            answer = self.make_visual_answer(
                question,
                vision,
            )

            print("Visual answer:", repr(answer))

            self.history.append((question, answer))

            # Return visual answers directly
            return answer

        # Normal conversation
        print("VISION: not needed")

        memories = "\n".join(self.memory.get_all())

        conversation = ""

        for old_question, old_answer in self.history[-5:]:
            conversation += f"User: {old_question}\n"
            conversation += f"Assistant: {old_answer}\n"

        context = f"""Known information about the user:
{memories}

Previous conversation:
{conversation}

This is a normal conversation.
Answer the current question naturally and briefly.
Use stored memory only when it is relevant."""

        print("Sending to Chat...")

        answer = self.chat.reply(
            question,
            context,
        )

        print("Chat returned:", repr(answer))

        if answer:
            self.history.append((question, answer))

        return answer