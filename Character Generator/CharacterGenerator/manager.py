import json
import os
from character import Character

DATA_DIR = r"C:\Users\jjmun\OneDrive\Documents\Character Generator"
DATA_FILE = os.path.join(DATA_DIR, "data.json")

class CharacterManager:
    def __init__(self):
        self.characters = []
        self.load()

    def add_character(self, character):
        self.characters.append(character)
        self.save()

    def remove_character(self, character_id):
        self.characters = [c for c in self.characters if c.id != character_id]
        self.save()

    def get_all_prompts(self, selected_ids=None):
        chars = self.characters
        if selected_ids:
            chars = [c for c in self.characters if c.id in selected_ids]
        return "\n\n".join([c.format_prompt() for c in chars])

    def save(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        data = [c.to_dict() for c in self.characters]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.characters = [Character.from_dict(d) for d in data]
        else:
            self.characters = []
