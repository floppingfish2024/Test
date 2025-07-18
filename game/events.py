import random

class Event:
    def __init__(self, name, message, effects):
        self.name = name
        self.message = message
        self.effects = effects

    def trigger(self, game_state):
        for effect_type, effect_value in self.effects.items():
            if effect_type == "resource_gain":
                for resource, amount in effect_value.items():
                    game_state.resources[resource] += amount
            elif effect_type == "resource_loss":
                for resource, amount in effect_value.items():
                    game_state.resources[resource] = max(0, game_state.resources[resource] - amount)
        return self.message


events = [
    Event(
        name="Good Harvest",
        message="A surprisingly good harvest brings in extra wood!",
        effects={"resource_gain": {"wood": 50}},
    ),
    Event(
        name="Storm",
        message="A bad storm damages some of your wood supplies.",
        effects={"resource_loss": {"wood": 25}},
    ),
    Event(
        name="Baby Boom",
        message="A baby boom increases your population!",
        effects={"resource_gain": {"population": 10}},
    ),
]


def get_random_event():
    return random.choice(events)
