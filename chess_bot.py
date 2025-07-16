import chess
from bots.q_learning_bot import Bot as QLearningBot

def play_game(bot1, bot2, q_table_path="q_table.json"):
    board = chess.Board()

    # Load the Q-table at the beginning of the game
    if isinstance(bot1, QLearningBot):
        bot1.load_q_table()
    if isinstance(bot2, QLearningBot):
        bot2.load_q_table()

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
                if isinstance(bot1, QLearningBot):
                    bot1.update_q_value(state, action.uci(), reward1, next_state)
            else: #Last move was by black
                if isinstance(bot2, QLearningBot):
                    bot2.update_q_value(state, action.uci(), reward2, next_state)
        else:
            if board.turn == chess.BLACK: #Last move was by white
                if isinstance(bot1, QLearningBot):
                    bot1.update_q_value(state, action.uci(), 0, next_state)
            else: #Last move was by black
                if isinstance(bot2, QLearningBot):
                    bot2.update_q_value(state, action.uci(), 0, next_state)

    # Save the Q-table at the end of the game
    if isinstance(bot1, QLearningBot):
        bot1.save_q_table()
    if isinstance(bot2, QLearningBot):
        bot2.save_q_table()

    return board.result()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "compete":
        # In compete mode, the bot plays against another instance of itself.
        # This is to demonstrate the multi-instance learning.
        bot1 = QLearningBot(exploration_rate=0) # More deterministic
        bot2 = QLearningBot(exploration_rate=0) # More deterministic

        # The bots will load the same Q-table, play a game, and then save the updated Q-table.
        # This simulates two different instances of the bot learning from the same game.
        result = play_game(bot1, bot2, "q_table.json")
        print(f"Game result: {result}")
    else:
        # In normal mode, the bot plays against itself to learn.
        bot = QLearningBot()

        # Play 100 games to learn
        for i in range(100):
            print(f"Playing game {i+1}")
            result = play_game(bot, bot, "q_table.json")
            print(f"Game {i+1} result: {result}")

        print("Q-table saved.")
