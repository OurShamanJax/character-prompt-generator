import random
import uuid

class Character:
    """
    Core data model for a character.
    Both dumb mode and smart mode MUST produce this structure.
    """

    def __init__(
        self,
        gender=None,
        name=None,
        age=None,
        traits=None,
        backstory=None,
        goals=None,
        needs=None,
        emotions=None,
        reasoning=None,
        id=None
    ):
        self.id = id or str(uuid.uuid4())
        self.gender = gender or random.choice(["male", "female"])
        self.name = name or self.generate_name()
        self.age = age or random.randint(18, 50)
        self.backstory = backstory or self.generate_backstory()
        self.traits = traits or self.generate_traits()
        self.goals = goals or self.generate_goals()
        self.needs = needs or self.generate_needs()
        self.emotions = emotions or self.generate_emotions()
        self.reasoning = reasoning or {}

    # ---------- Dumb Mode Generators ----------

    def generate_name(self):
        male = ["John", "Alex", "Marcus", "Leo", "Ethan"]
        female = ["Sophia", "Emma", "Luna", "Ava", "Isla"]
        return random.choice(male if self.gender == "male" else female)

    def generate_backstory(self):
        return random.choice([
            "Grew up in a small rural town",
            "Raised in a crowded megacity",
            "Survived a harsh frontier upbringing",
            "Educated in elite academic institutions"
        ])

    def generate_traits(self):
        return random.sample([
            "brave", "curious", "analytical", "guarded",
            "empathetic", "ambitious", "cautious"
        ], 3)

    def generate_goals(self):
        return random.choice([
            "seek truth",
            "gain independence",
            "protect others",
            "achieve mastery"
        ])

    def generate_needs(self):
        return random.choice([
            "security", "freedom", "connection", "recognition"
        ])

    def generate_emotions(self):
        return random.choice([
            "focused", "anxious", "hopeful", "conflicted"
        ])

    # ---------- Prompt Formatting ----------

    def format_prompt(self):
        return (
            f"You are {self.name}, a {self.age}-year-old {self.gender}.\n"
            f"Personality traits: {', '.join(self.traits)}.\n"
            f"Backstory: {self.backstory}.\n"
            f"Goals: {self.goals}.\n"
            f"Current feelings: {self.emotions}.\n"
            f"Needs: {self.needs}.\n"
            f"Always behave as if you are real."
        )

    # ---------- Persistence ----------

    def to_dict(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "name": self.name,
            "age": self.age,
            "traits": self.traits,
            "backstory": self.backstory,
            "goals": self.goals,
            "needs": self.needs,
            "emotions": self.emotions,
            "reasoning": self.reasoning
        }

    @staticmethod
    def from_dict(data):
        return Character(
            gender=data.get("gender"),
            name=data.get("name"),
            age=data.get("age"),
            traits=data.get("traits"),
            backstory=data.get("backstory"),
            goals=data.get("goals"),
            needs=data.get("needs"),
            emotions=data.get("emotions"),
            reasoning=data.get("reasoning"),
            id=data.get("id")
        )
