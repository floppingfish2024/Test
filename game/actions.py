class Action:
    def __init__(self, name, cost, rewards):
        self.name = name
        self.cost = cost
        self.rewards = rewards

    def execute(self, game_state):
        if self.can_execute(game_state):
            for resource, amount in self.cost.items():
                game_state.resources[resource] -= amount
            for resource, amount in self.rewards.items():
                game_state.resources[resource] += amount
            return True
        return False

    def can_execute(self, game_state):
        for resource, amount in self.cost.items():
            if game_state.resources.get(resource, 0) < amount:
                return False
        return True


actions = {
    "gather_wood": Action(
        name="Gather Wood",
        cost={},
        rewards={"wood": 1},
    ),
    "gather_stone": Action(
        name="Gather Stone",
        cost={"wood": 10},
        rewards={"stone": 1},
    ),
}


def unlock_action(game_state, action_name):
    if game_state.can_unlock(action_name):
        game_state.unlocked_actions.add(action_name)
