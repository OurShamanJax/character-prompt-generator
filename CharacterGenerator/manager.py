import json
import os
from character import Character

DATA_FILE = "data.json"

class CharacterManager:
    """
    Handles persistence and retrieval of characters.
    """

    def __init__(self):
        self.characters = []
        self.load()

    def add_character(self, character):
        self.characters.append(character)
        self.save()

    def remove_character(self, character_id):
        self.characters = [c for c in self.characters if c.id != character_id]
        self.save()

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.characters], f, indent=4)

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.characters = [Character.from_dict(d) for d in data]
        else:
            self.characters = []

    def get_all_prompts(self):
        return "\n\n".join(c.format_prompt() for c in self.characters)
