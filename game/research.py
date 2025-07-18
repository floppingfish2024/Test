class Research:
    def __init__(self, name, cost, unlocks):
        self.name = name
        self.cost = cost
        self.unlocks = unlocks
        self.is_researched = False

    def can_research(self, game_state):
        if self.is_researched:
            return False
        for resource, amount in self.cost.items():
            if game_state.resources.get(resource, 0) < amount:
                return False
        return True

    def research(self, game_state):
        if self.can_research(game_state):
            for resource, amount in self.cost.items():
                game_state.resources[resource] -= amount
            self.is_researched = True
            for unlock_type, unlock_name in self.unlocks.items():
                if unlock_type == "building":
                    game_state.unlocked_buildings.add(unlock_name)
            return True
        return False


research_tree = {
    "unlock_quarry": Research(
        name="Unlock Quarry",
        cost={"wood": 100, "stone": 100},
        unlocks={"building": "quarry"},
    ),
    "unlock_housing": Research(
        name="Unlock Housing",
        cost={"wood": 200},
        unlocks={"building": "house"},
    ),
}
