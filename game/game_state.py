import time

class GameState:
    def __init__(self):
        self.resources = {"wood": 0, "stone": 0}
        self.unlocked_actions = {"gather_wood"}
        self.last_update = time.time()

    def update(self):
        now = time.time()
        delta = now - self.last_update
        self.last_update = now
        # Passive resource generation can be added here
        pass

    def can_unlock(self, action_name):
        # Placeholder for unlock conditions
        return True
