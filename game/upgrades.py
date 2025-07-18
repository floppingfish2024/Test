class Upgrade:
    def __init__(self, name, cost, target, multiplier):
        self.name = name
        self.cost = cost
        self.target = target
        self.multiplier = multiplier
        self.is_purchased = False

    def can_purchase(self, game_state):
        if self.is_purchased:
            return False
        for resource, amount in self.cost.items():
            if game_state.resources.get(resource, 0) < amount:
                return False
        return True

    def purchase(self, game_state):
        if self.can_purchase(game_state):
            for resource, amount in self.cost.items():
                game_state.resources[resource] -= amount
            self.is_purchased = True
            self.apply_bonus(game_state)
            return True
        return False

    def apply_bonus(self, game_state):
        if self.target in game_state.actions:
            game_state.actions[self.target].rewards = {
                res: val * self.multiplier
                for res, val in game_state.actions[self.target].rewards.items()
            }
        elif self.target in game_state.buildings:
            game_state.buildings[self.target].production = {
                res: val * self.multiplier
                for res, val in game_state.buildings[self.target].production.items()
            }


upgrades = {
    "sharper_axe": Upgrade(
        name="Sharper Axe",
        cost={"wood": 100},
        target="gather_wood",
        multiplier=2,
    ),
}
