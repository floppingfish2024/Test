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

        action_layout = [
            [sg.B(actions[action_name].name, key=f"action_{action_name}")]
            for action_name in self.game_state.unlocked_actions
        ]

        layout = [
            [sg.Frame("Resources", resource_layout)],
            [sg.Frame("Actions", action_layout)],
        ]
        return layout

    def update(self):
        for resource, amount in self.game_state.resources.items():
            self.window[f"resource_{resource}"].update(
                f"{resource.capitalize()}: {int(amount)}"
            )

    def run(self):
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break

            if event.startswith("action_"):
                action_name = event.split("_")[1]
                action = actions[action_name]
                action.execute(self.game_state)

            self.game_state.update()
            self.update()

        self.window.close()
