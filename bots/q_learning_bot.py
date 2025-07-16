import chess
import random
import json
from filelock import FileLock

class Bot:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1, q_table_path="q_table.json"):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table_path = q_table_path
        self.load_q_table()

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

    def save_q_table(self):
        lock = FileLock(self.q_table_path + ".lock")
        with lock:
            with open(self.q_table_path, 'w') as f:
                json.dump({f"{k[0]}||{k[1]}": v for k, v in self.q_table.items()}, f)

    def load_q_table(self):
        lock = FileLock(self.q_table_path + ".lock")
        with lock:
            try:
                with open(self.q_table_path, 'r') as f:
                    data = json.load(f)
                    self.q_table = {tuple(k.split('||')): v for k, v in data.items()}
            except (FileNotFoundError, json.JSONDecodeError):
                self.q_table = {}
