import tkinter as tk
import chess
from bots.q_learning_bot import Bot as QLearningBot
from bots.random_bot import Bot as RandomBot
import threading
import time

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess")
        self.geometry("480x480")
        self.resizable(False, False)

        self.board = chess.Board()
        self.bot = QLearningBot()

        self.canvas = tk.Canvas(self, width=480, height=480)
        self.canvas.pack()

        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_click)
        self.selected_piece = None

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(j * 60, i * 60, (j + 1) * 60, (i + 1) * 60, fill=color)

    def draw_pieces(self):
        self.canvas.delete("pieces")
        for i in range(8):
            for j in range(8):
                square = chess.square(j, 7 - i)
                piece = self.board.piece_at(square)
                if piece:
                    filename = f"images/{piece.symbol().lower()}.png"
                    if piece.color == chess.BLACK:
                        filename = f"images/{piece.symbol().upper()}d.png"
                    else:
                        filename = f"images/{piece.symbol().lower()}l.png"

                    # Fallback for pieces that don't have specific images
                    try:
                        img = tk.PhotoImage(file=filename)
                    except tk.TclError:
                        # Simple text representation if image not found
                        self.canvas.create_text(j * 60 + 30, i * 60 + 30, text=piece.symbol(), font=("Arial", 30), tags="pieces")
                        continue

                    self.canvas.create_image(j * 60, i * 60, anchor=tk.NW, image=img, tags="pieces")
                    self.piece_images.append(img)


    def on_click(self, event):
        if self.board.turn == chess.WHITE:
            col = event.x // 60
            row = event.y // 60
            square = chess.square(col, 7 - row)

            if self.selected_piece:
                move = chess.Move(self.selected_piece, square)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.draw_pieces()
                    self.selected_piece = None
                    self.after(100, self.bot_move)
                else:
                    self.selected_piece = None
            else:
                piece = self.board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    self.selected_piece = square

    def bot_move(self):
        if not self.board.is_game_over():
            move = self.bot.choose_action(self.board)
            if move:
                self.board.push(move)
                self.draw_pieces()
                if self.board.is_game_over():
                    self.game_over()

    def game_over(self):
        result = self.board.result()
        if result == "1-0":
            reward = -1
        elif result == "0-1":
            reward = 1
        else:
            reward = 0.5

        # Update Q-table for the bot's last move
        if isinstance(self.bot, QLearningBot):
            # We need to get the state before the last move
            self.board.pop()
            state = self.board.fen()
            action = self.board.peek().uci()
            self.board.push(self.board.peek()) # push it back
            next_state = self.board.fen()
            self.bot.update_q_value(state, action, reward, next_state)
            self.bot.save_q_table()

        self.canvas.create_text(240, 240, text=f"Game Over: {result}", font=("Arial", 30), fill="red")

if __name__ == "__main__":
    # Create a directory for images if it doesn't exist
    import os
    if not os.path.exists("images"):
        os.makedirs("images")

    # Download piece images (example for one piece)
    import urllib.request

    # URLs for white pieces (light)
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/wP.svg", "images/pl.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/wR.svg", "images/rl.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/wN.svg", "images/nl.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/wB.svg", "images/bl.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/wQ.svg", "images/ql.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/wK.svg", "images/kl.png")

    # URLs for black pieces (dark)
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/bP.svg", "images/pd.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/bR.svg", "images/rd.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/bN.svg", "images/nd.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/bB.svg", "images/bd.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/bQ.svg", "images/qd.png")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/lichess-org/chess-pieces/master/merida/bK.svg", "images/kd.png")


    app = ChessGUI()
    app.mainloop()
