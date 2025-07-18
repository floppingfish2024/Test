class Building:
    def __init__(self, name, cost, production):
        self.name = name
        self.cost = cost
        self.production = production
        self.level = 0

    def get_cost(self):
        return {resource: amount * (self.level + 1) for resource, amount in self.cost.items()}

    def can_build(self, game_state):
        for resource, amount in self.get_cost().items():
            if game_state.resources.get(resource, 0) < amount:
                return False
        return True

    def build(self, game_state):
        if self.can_build(game_state):
            for resource, amount in self.get_cost().items():
                game_state.resources[resource] -= amount
            self.level += 1
            if self.name == "House":
                game_state.population_limit += 5
            return True
        return False

    def get_production(self):
        return {resource: amount * self.level for resource, amount in self.production.items()}


buildings = {
    "lumber_mill": Building(
        name="Lumber Mill",
        cost={"wood": 50, "stone": 25},
        production={"wood": 1},
    ),
    "quarry": Building(
        name="Quarry",
        cost={"wood": 100, "stone": 50},
        production={"stone": 1},
    ),
    "house": Building(
        name="House",
        cost={"wood": 50},
        production={},
    ),
}
