import random
import uuid

# Trait categories
positive_social = ["friendly", "charismatic", "cooperative"]
positive_intellectual = ["curious", "strategic", "innovative"]
positive_physical = ["brave", "adventurous", "athletic"]
negative_social = ["shy", "aggressive", "aloof"]
negative_intellectual = ["cunning", "forgetful", "impatient"]
negative_physical = ["lazy", "clumsy", "timid"]

all_positive = positive_social + positive_intellectual + positive_physical
all_negative = negative_social + negative_intellectual + negative_physical

# Expanded mutually exclusive traits
conflicting_traits = [
    ("brave", "shy"),
    ("friendly", "aggressive"),
    ("optimistic", "pessimistic"),
    ("cooperative", "aloof"),
    ("curious", "impatient"),
    ("athletic", "lazy")
]

# Trait influence on goals, emotions, and needs
trait_influence = {
    "brave": {"goals": ["explore the world", "master a skill"], "emotions": ["confident", "excited"], "needs": ["adventure"]},
    "shy": {"goals": ["find companionship"], "emotions": ["anxious", "lonely"], "needs": ["companionship"]},
    "friendly": {"goals": ["make friends"], "emotions": ["happy"], "needs": ["companionship"]},
    "aggressive": {"goals": ["gain power"], "emotions": ["angry"], "needs": ["challenge"]},
    "curious": {"goals": ["learn knowledge"], "emotions": ["curious"], "needs": ["knowledge"]},
    "lazy": {"goals": ["relax"], "emotions": ["bored"], "needs": ["rest"]}
}

class Character:
    def __init__(self, gender=None, name=None, age=None, traits=None,
                 backstory=None, goals=None, needs=None, emotions=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.gender = gender or random.choice(["male", "female"])
        self.name = name or self.generate_name()
        self.age = age or random.randint(18, 50)
        self.backstory, weight = self.generate_backstory()
        self.traits = traits or self.generate_traits(weight)
        self.goals = goals or self.generate_goals()
        self.needs = needs or self.generate_needs()
        self.emotions = emotions or self.generate_emotions()

    def generate_name(self):
        male_names = ["John", "Alex", "Marcus", "Leo", "Ethan", "Liam", "Noah", "Oliver"]
        female_names = ["Sophia", "Luna", "Emma", "Ava", "Isla", "Olivia", "Amelia", "Mia"]
        return random.choice(male_names if self.gender == "male" else female_names)

    def generate_backstory(self):
        backstories = {
            "grew up in a small village": 4,
            "grew up in a bustling city": 3,
            "grew up in a medieval kingdom": 2,
            "grew up in a futuristic colony": 5
        }
        backstory, weight = random.choice(list(backstories.items()))
        return backstory, weight

    def generate_traits(self, weight, num_traits=3):
        traits = []
        pos_chance = min(max(weight / 5, 0), 1)
        neg_chance = 1 - pos_chance
        all_traits_list = all_positive + all_negative

        while len(traits) < num_traits:
            trait = random.choice(all_traits_list)
            if trait in traits:
                continue
            chance = pos_chance if trait in all_positive else neg_chance
            if random.random() < chance:
                traits.append(trait)
                # Remove conflicting traits
                for t1, t2 in conflicting_traits:
                    if trait == t1 and t2 in traits:
                        traits.remove(t2)
                    elif trait == t2 and t1 in traits:
                        traits.remove(t1)
        return traits

    def generate_goals(self):
        goals_list = ["find true love", "become wealthy", "explore the world", "master a skill"]
        # Influence from traits
        influenced = []
        for t in self.traits:
            if t in trait_influence:
                influenced += trait_influence[t].get("goals", [])
        return random.choice(influenced) if influenced else random.choice(goals_list)

    def generate_needs(self):
        needs_list = ["food", "companionship", "adventure", "knowledge"]
        influenced = []
        for t in self.traits:
            if t in trait_influence:
                influenced += trait_influence[t].get("needs", [])
        return random.choice(influenced) if influenced else random.choice(needs_list)

    def generate_emotions(self):
        emotions_list = ["happy", "anxious", "curious", "lonely", "excited"]
        influenced = []
        for t in self.traits:
            if t in trait_influence:
                influenced += trait_influence[t].get("emotions", [])
        return random.choice(influenced) if influenced else random.choice(emotions_list)

    def format_prompt(self):
        return (f"You are {self.name}, a {self.age}-year-old {self.gender}. "
                f"Personality traits: {', '.join(self.traits)}. "
                f"Backstory: {self.backstory}. "
                f"Goals: {self.goals}. "
                f"Current feelings: {self.emotions}. "
                f"Needs: {self.needs}. "
                f"Always behave as if you are real.")

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
            "emotions": self.emotions
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
            id=data.get("id")
        )
