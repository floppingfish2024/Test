import time
from game.actions import actions
from game.buildings import buildings
from game.research import research_tree
from game.upgrades import upgrades
from game.events import get_random_event

class GameState:
    def __init__(self):
        self.resources = {"wood": 0, "stone": 0, "iron": 0, "gold": 0, "population": 0, "food": 0}
        self.population_limit = 5
        self.workers = {"wood": 0, "stone": 0, "iron": 0, "gold": 0, "food": 0}
        self.event_log = []
        self.event_timer = 0
        self.unlocked_actions = {"gather_wood"}
        self.unlocked_buildings = {"lumber_mill"}
        self.actions = actions
        self.buildings = buildings
        self.research_tree = research_tree
        self.upgrades = upgrades
        self.last_update = time.time()

    def update(self):
        now = time.time()
        delta = now - self.last_update
        self.last_update = now
        for building in self.buildings.values():
            for resource, amount in building.get_production().items():
                self.resources[resource] += amount * delta

        for resource, num_workers in self.workers.items():
            if num_workers > 0:
                self.resources[resource] += num_workers * 0.1 * delta # Each worker produces 0.1 resource per second

        self.event_timer += delta
        if self.event_timer >= 60: # Trigger event every 60 seconds
            self.event_timer = 0
            event = get_random_event()
            message = event.trigger(self)
            self.event_log.append(message)

        # Population consumption
        food_consumed = self.resources["population"] * 0.1 * delta # Each person consumes 0.1 food per second
        self.resources["food"] -= food_consumed
        if self.resources["food"] < 0:
            self.resources["food"] = 0
            self.resources["population"] -= 0.05 * delta # Population decreases if there is no food
            if self.resources["population"] < 0:
                self.resources["population"] = 0

    def can_unlock(self, action_name):
        # Placeholder for unlock conditions
        return True
