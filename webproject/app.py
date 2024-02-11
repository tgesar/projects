from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [''] * 9
current_player = 'X'

def check_winner():
    # Check rows, columns, and diagonals for a winner
    for i in range(0, 3):
        if board[i] == board[i + 3] == board[i + 6] != '':
            return board[i]
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != '':
            return board[i * 3]
    if board[0] == board[4] == board[8] != '':
        return board[0]
    if board[2] == board[4] == board[6] != '':
        return board[2]
    return None

def check_tie():
    return '' not in board

@app.route('/')
def home():
    return render_template('index.html', board=board, current_player=current_player)

@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player
    position = int(request.form['position'])
    if board[position] == '' and not check_winner() and not check_tie():
        board[position] = current_player
        winner = check_winner()
        if winner:
            return jsonify(board=board, winner=winner, tie=False, current_player=current_player)
        elif check_tie():
            return jsonify(board=board, winner=None, tie=True, current_player=current_player)
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            return jsonify(board=board, winner=None, tie=False, current_player=current_player)
    else:
        return jsonify(board=board, winner=None, tie=False, current_player=current_player)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global board, current_player
    board = [''] * 9
    current_player = 'X'
    return jsonify(board=board, current_player=current_player)

if __name__ == '__main__':
    app.run(debug=True)
