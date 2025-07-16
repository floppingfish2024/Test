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
    import threading

    def play_games_threaded(num_games, num_threads):
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=play_games, args=(num_games // num_threads,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def play_games(num_games):
        bot = QLearningBot()
        for i in range(num_games):
            print(f"Playing game {i+1}")
            result = play_game(bot, bot, "q_table.json")
            print(f"Game {i+1} result: {result}")

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
        num_games = 100
        num_threads = 4
        if len(sys.argv) > 1:
            try:
                num_games = int(sys.argv[1])
            except ValueError:
                pass
        if len(sys.argv) > 2:
            try:
                num_threads = int(sys.argv[2])
            except ValueError:
                pass

        play_games_threaded(num_games, num_threads)
        print("Q-table saved.")
