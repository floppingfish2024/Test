import chess
import random
import json
from filelock import FileLock

class ChessBot:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        if random.random() < self.exploration_rate:
            return random.choice(legal_moves)
        else:
            q_values = [self.get_q_value(board.fen(), move.uci()) for move in legal_moves]
            max_q_value = max(q_values)
            best_moves = [legal_moves[i] for i, q in enumerate(q_values) if q == max_q_value]
            return random.choice(best_moves)

    def update_q_value(self, state, action, reward, next_state):
        old_q_value = self.get_q_value(state, action)

        next_board = chess.Board(next_state)
        next_legal_moves = list(next_board.legal_moves)
        if not next_legal_moves:
            future_q_value = 0.0
        else:
            future_q_values = [self.get_q_value(next_state, move.uci()) for move in next_legal_moves]
            future_q_value = max(future_q_values)

        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * future_q_value - old_q_value)
        self.q_table[(state, action)] = new_q_value

    def save_q_table(self, file_path):
        lock = FileLock(file_path + ".lock")
        with lock:
            with open(file_path, 'w') as f:
                # The state string can contain underscores, so we need a different separator.
                json.dump({f"{k[0]}||{k[1]}": v for k, v in self.q_table.items()}, f)

    def load_q_table(self, file_path):
        lock = FileLock(file_path + ".lock")
        with lock:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # The state string can contain underscores, so we need a different separator.
                    self.q_table = {tuple(k.split('||')): v for k, v in data.items()}
            except (FileNotFoundError, json.JSONDecodeError):
                self.q_table = {}

def play_game(bot1, bot2, q_table_path="q_table.json"):
    board = chess.Board()

    # Load the Q-table at the beginning of the game
    bot1.load_q_table(q_table_path)
    bot2.load_q_table(q_table_path)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            action = bot1.choose_action(board)
        else:
            action = bot2.choose_action(board)

        if action is None:
            break

        state = board.fen()
        board.push(action)
        next_state = board.fen()

        result = board.result()
        if result != "*":
            if result == "1-0":
                reward1 = 1
                reward2 = -1
            elif result == "0-1":
                reward1 = -1
                reward2 = 1
            else:
                reward1 = 0.5
                reward2 = 0.5

            if board.turn == chess.BLACK: #Last move was by white
                bot1.update_q_value(state, action.uci(), reward1, next_state)
            else: #Last move was by black
                 bot2.update_q_value(state, action.uci(), reward2, next_state)
        else:
            if board.turn == chess.BLACK: #Last move was by white
                bot1.update_q_value(state, action.uci(), 0, next_state)
            else: #Last move was by black
                bot2.update_q_value(state, action.uci(), 0, next_state)

    # Save the Q-table at the end of the game
    bot1.save_q_table(q_table_path)
    bot2.save_q_table(q_table_path)

    return board.result()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "compete":
        # In compete mode, the bot plays against another instance of itself.
        # This is to demonstrate the multi-instance learning.
        bot1 = ChessBot(exploration_rate=0) # More deterministic
        bot2 = ChessBot(exploration_rate=0) # More deterministic

        # The bots will load the same Q-table, play a game, and then save the updated Q-table.
        # This simulates two different instances of the bot learning from the same game.
        result = play_game(bot1, bot2, "q_table.json")
        print(f"Game result: {result}")
    else:
        # In normal mode, the bot plays against itself to learn.
        bot = ChessBot()

        # Play 100 games to learn
        for i in range(100):
            print(f"Playing game {i+1}")
            result = play_game(bot, bot, "q_table.json")
            print(f"Game {i+1} result: {result}")

        print("Q-table saved.")
