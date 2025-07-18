import time
from game.actions import actions
from game.buildings import buildings
from game.research import research_tree
from game.upgrades import upgrades
from game.events import get_random_event

class GameState:
    def __init__(self):
        self.resources = {"wood": 0, "stone": 0, "iron": 0, "gold": 0, "population": 0}
        self.population_limit = 5
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

        self.event_timer += delta
        if self.event_timer >= 60: # Trigger event every 60 seconds
            self.event_timer = 0
            event = get_random_event()
            message = event.trigger(self)
            self.event_log.append(message)

    def can_unlock(self, action_name):
        # Placeholder for unlock conditions
        return True
