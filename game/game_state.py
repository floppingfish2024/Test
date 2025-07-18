import time
from game.actions import actions
from game.buildings import buildings
from game.research import research_tree
from game.upgrades import upgrades

class GameState:
    def __init__(self):
        self.resources = {"wood": 0, "stone": 0, "iron": 0, "gold": 0}
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

    def can_unlock(self, action_name):
        # Placeholder for unlock conditions
        return True
