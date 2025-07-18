import tkinter as tk
from tkinter import ttk

from game.actions import actions, unlock_action
from game.buildings import buildings
from game.research import research_tree
from game.upgrades import upgrades

class MainWindow:
    def __init__(self, game_state):
        self.game_state = game_state
        self.root = tk.Tk()
        self.root.title("Incremental Game")

        self.resource_labels = {}
        self.worker_labels = {}
        self.create_layout()

    def create_layout(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_columnconfigure(0, weight=1)

        # Resources
        resource_frame = ttk.LabelFrame(self.root, text="Resources")
        resource_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        for i, (resource, amount) in enumerate(self.game_state.resources.items()):
            label = ttk.Label(resource_frame, text=f"{resource.capitalize()}: {int(amount)}")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.resource_labels[resource] = label

        # Actions
        action_frame = ttk.LabelFrame(self.root, text="Actions")
        action_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        for i, action_name in enumerate(sorted(list(self.game_state.unlocked_actions))):
            action = actions[action_name]
            button = ttk.Button(action_frame, text=action.name, command=lambda a=action, an=action_name: self.execute_action(a, an))
            button.grid(row=i, column=0, padx=5, pady=5, sticky="w")

        # Buildings
        building_frame = ttk.LabelFrame(self.root, text="Buildings")
        building_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        for i, (name, building) in enumerate(self.game_state.buildings.items()):
             if name in self.game_state.unlocked_buildings:
                label = ttk.Label(building_frame, text=f"{building.name} (Level {building.level})")
                label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                button = ttk.Button(building_frame, text=f"Build ({', '.join([f'{v} {k}' for k, v in building.get_cost().items()])})", command=lambda b=building: self.build(b))
                button.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        # Research
        research_frame = ttk.LabelFrame(self.root, text="Research")
        research_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        for i, (name, research) in enumerate(self.game_state.research_tree.items()):
            if not research.is_researched:
                label = ttk.Label(research_frame, text=research.name)
                label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                button = ttk.Button(research_frame, text=f"Research ({', '.join([f'{v} {k}' for k, v in research.cost.items()])})", command=lambda r=research: self.research(r))
                button.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        # Upgrades
        upgrade_frame = ttk.LabelFrame(self.root, text="Upgrades")
        upgrade_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        for i, (name, upgrade) in enumerate(self.game_state.upgrades.items()):
            if not upgrade.is_purchased:
                label = ttk.Label(upgrade_frame, text=upgrade.name)
                label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                button = ttk.Button(upgrade_frame, text=f"Purchase ({', '.join([f'{v} {k}' for k, v in upgrade.cost.items()])})", command=lambda u=upgrade: self.purchase_upgrade(u))
                button.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        # Worker Allocation
        worker_frame = ttk.LabelFrame(self.root, text="Worker Allocation")
        worker_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        for i, resource in enumerate(self.game_state.workers):
            label = ttk.Label(worker_frame, text=f"{resource.capitalize()}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            dec_button = ttk.Button(worker_frame, text="-", command=lambda r=resource: self.dec_worker(r))
            dec_button.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            worker_label = ttk.Label(worker_frame, text=str(self.game_state.workers[resource]))
            worker_label.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            self.worker_labels[resource] = worker_label
            inc_button = ttk.Button(worker_frame, text="+", command=lambda r=resource: self.inc_worker(r))
            inc_button.grid(row=i, column=3, padx=5, pady=5, sticky="w")

        # Event Log
        event_frame = ttk.LabelFrame(self.root, text="Event Log")
        event_frame.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        for i, message in enumerate(self.game_state.event_log[-5:]):
            label = ttk.Label(event_frame, text=message)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

        self.root.after(100, self.update)

    def execute_action(self, action, action_name):
        if action.execute(self.game_state):
            if "unlock" in action_name:
                self.game_state.unlocked_actions.remove(action_name)
                unlock_action(self.game_state, action_name)
                if action_name == "unlock_stone_gathering":
                    self.game_state.unlocked_actions.add("unlock_iron_mining")
                elif action_name == "unlock_iron_mining":
                    self.game_state.unlocked_actions.add("unlock_gold_panning")
                self.create_layout()

    def build(self, building):
        if building.build(self.game_state):
            self.create_layout()

    def research(self, research):
        if research.research(self.game_state):
            self.create_layout()

    def purchase_upgrade(self, upgrade):
        if upgrade.purchase(self.game_state):
            self.create_layout()

    def inc_worker(self, resource):
        if sum(self.game_state.workers.values()) < self.game_state.resources["population"]:
            self.game_state.workers[resource] += 1
            self.worker_labels[resource].config(text=str(self.game_state.workers[resource]))


    def dec_worker(self, resource):
        if self.game_state.workers[resource] > 0:
            self.game_state.workers[resource] -= 1
            self.worker_labels[resource].config(text=str(self.game_state.workers[resource]))


    def update(self):
        for resource, amount in self.game_state.resources.items():
            self.resource_labels[resource].config(text=f"{resource.capitalize()}: {int(amount)}")
        self.game_state.update()
        if self.game_state.event_log:
            self.create_layout()
        self.root.after(100, self.update)

    def run(self):
        self.game_state.unlocked_actions.add("unlock_stone_gathering")
        self.create_layout()
        self.root.mainloop()
