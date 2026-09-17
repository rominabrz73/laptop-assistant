import json
import os


class Memory:
    def __init__(self):
        project_folder = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.file_path = os.path.join(project_folder, "memory.json")
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        return []

    def save(self, text):
        if text not in self.data:
            self.data.append(text)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

        print("Saved file:", self.file_path)
        print("Memory:", self.data)

    def get_all(self):
        return self.data