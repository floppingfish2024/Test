from flask import Flask, render_template, request, jsonify
import chess
import os
import importlib

app = Flask(__name__)

# Load the bots from the bots folder
bots = {}
for filename in os.listdir('bots'):
    if filename.endswith('.py') and filename != '__init__.py':
        bot_name = filename[:-3]
        bots[bot_name] = importlib.import_module(f'bots.{bot_name}').Bot()

@app.route('/')
def index():
    return render_template('index.html', bots=bots.keys())

@app.route('/move', methods=['POST'])
def move():
    bot_name = request.json['bot']
    fen = request.json['fen']

    board = chess.Board(fen)
    bot = bots[bot_name]

    move = bot.choose_action(board)

    if move is not None:
        board.push(move)

    return jsonify({
        'fen': board.fen(),
        'game_over': board.is_game_over(),
        'result': board.result()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
