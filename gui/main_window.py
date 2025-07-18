import PySimpleGUI as sg

from game.actions import actions

class MainWindow:
    def __init__(self, game_state):
        self.game_state = game_state
        self.layout = self.create_layout()
        self.window = sg.Window("Incremental Game", self.layout)

    def create_layout(self):
        resource_layout = [
            [sg.T(f"{resource.capitalize()}: {amount}", key=f"resource_{resource}")]
            for resource, amount in self.game_state.resources.items()
        ]
        resource_layout.append([sg.T(f"Population: {int(self.game_state.resources['population'])}/{self.game_state.population_limit}", key="population")])

        action_layout = [
            [sg.B(actions[action_name].name, key=f"action_{action_name}")]
            for action_name in self.game_state.unlocked_actions
        ]

        building_layout = [
            [
                sg.Text(f"{building.name} (Level {building.level})", key=f"building_{name}_level"),
                sg.Button(f"Build ({', '.join([f'{v} {k}' for k, v in building.get_cost().items()])})", key=f"build_{name}"),
            ]
            for name, building in self.game_state.buildings.items()
            if name in self.game_state.unlocked_buildings
        ]

        research_layout = [
            [
                sg.Text(f"{research.name}"),
                sg.Button(f"Research ({', '.join([f'{v} {k}' for k, v in research.cost.items()])})", key=f"research_{name}"),
            ]
            for name, research in self.game_state.research_tree.items()
            if not research.is_researched
        ]

        upgrade_layout = [
            [
                sg.Text(f"{upgrade.name}"),
                sg.Button(f"Purchase ({', '.join([f'{v} {k}' for k, v in upgrade.cost.items()])})", key=f"upgrade_{name}"),
            ]
            for name, upgrade in self.game_state.upgrades.items()
            if not upgrade.is_purchased
        ]

        event_log_layout = [
            [sg.Text(message)] for message in self.game_state.event_log[-5:] # Display last 5 events
        ]

        layout = [
            [sg.Frame("Resources", resource_layout)],
            [sg.Frame("Actions", action_layout)],
            [sg.Frame("Buildings", building_layout)],
            [sg.Frame("Research", research_layout)],
            [sg.Frame("Upgrades", upgrade_layout)],
            [sg.Frame("Event Log", event_log_layout, key="event_log")],
        ]
        return layout

    def update(self):
        for resource, amount in self.game_state.resources.items():
            self.window[f"resource_{resource}"].update(
                f"{resource.capitalize()}: {int(amount)}"
            )
        self.window["population"].update(f"Population: {int(self.game_state.resources['population'])}/{self.game_state.population_limit}")
        if self.game_state.event_log:
            self.remake_layout()

    def remake_layout(self):
        self.layout = self.create_layout()
        new_window = sg.Window("Incremental Game", self.layout)
        self.window.close()
        self.window = new_window

    def run(self):
        self.game_state.unlocked_actions.add("unlock_stone_gathering")
        self.remake_layout()
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break

            if event.startswith("action_"):
                action_name = event.split("_")[1]
                action = actions[action_name]
                if action.execute(self.game_state):
                    if "unlock" in action_name:
                        self.game_state.unlocked_actions.remove(action_name)
                        unlock_action(self.game_state, action_name)
                        if action_name == "unlock_stone_gathering":
                            self.game_state.unlocked_actions.add("unlock_iron_mining")
                        elif action_name == "unlock_iron_mining":
                            self.game_state.unlocked_actions.add("unlock_gold_panning")
                        self.remake_layout()

            if event.startswith("build_"):
                building_name = event.split("_")[1]
                building = self.game_state.buildings[building_name]
                if building.build(self.game_state):
                    self.remake_layout()

            if event.startswith("research_"):
                research_name = event.split("_")[1]
                research = self.game_state.research_tree[research_name]
                if research.research(self.game_state):
                    self.remake_layout()

            if event.startswith("upgrade_"):
                upgrade_name = event.split("_")[1]
                upgrade = self.game_state.upgrades[upgrade_name]
                if upgrade.purchase(self.game_state):
                    self.remake_layout()

            self.game_state.update()
            self.update()

        self.window.close()
