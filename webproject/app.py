from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [''] * 9
current_player = 'X'

def check_winner():
    # Check rows, columns, and diagonals for a winner
    for i in range(0, 3):
        if board[i] == board[i + 3] == board[i + 6] != '':
            return True
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != '':
            return True
    if board[0] == board[4] == board[8] != '':
        return True
    if board[2] == board[4] == board[6] != '':
        return True
    return False

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
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'
    return jsonify(board=board, winner=check_winner(), tie=check_tie())

if __name__ == '__main__':
    app.run(debug=True)
