import chess
import random

class Bot:
    def choose_action(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        return random.choice(legal_moves)
