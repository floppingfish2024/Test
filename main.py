from game.game_state import GameState
from gui.main_window import MainWindow

def main():
    game_state = GameState()
    main_window = MainWindow(game_state)
    main_window.run()

if __name__ == "__main__":
    main()
