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
    "unlock_stone_gathering": Action(
        name="Unlock Stone Gathering",
        cost={"wood": 10},
        rewards={},
    ),
    "gather_stone": Action(
        name="Gather Stone",
        cost={},
        rewards={"stone": 1},
    ),
    "unlock_iron_mining": Action(
        name="Unlock Iron Mining",
        cost={"stone": 25},
        rewards={},
    ),
    "gather_iron": Action(
        name="Gather Iron",
        cost={},
        rewards={"iron": 1},
    ),
    "unlock_gold_panning": Action(
        name="Unlock Gold Panning",
        cost={"iron": 50},
        rewards={},
    ),
    "gather_gold": Action(
        name="Gather Gold",
        cost={},
        rewards={"gold": 1},
    ),
}


def unlock_action(game_state, action_name):
    if action_name == "unlock_stone_gathering":
        game_state.unlocked_actions.add("gather_stone")
    elif action_name == "unlock_iron_mining":
        game_state.unlocked_actions.add("gather_iron")
    elif action_name == "unlock_gold_panning":
        game_state.unlocked_actions.add("gather_gold")
    else:
        if game_state.can_unlock(action_name):
            game_state.unlocked_actions.add(action_name)
