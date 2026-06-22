import tkinter as tk
from tkinter import messagebox
import copy

# ---------------- GAME LOGIC ---------------- #

def create_board():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    return board


DIRECTIONS = [(-1,-1), (-1,0), (-1,1),
              (0,-1),         (0,1),
              (1,-1), (1,0), (1,1)]


def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def opponent(player):
    return 'W' if player == 'B' else 'B'


def get_flips(board, r, c, player):
    if board[r][c] != '.':
        return []

    opp = opponent(player)
    flips = []

    for dr, dc in DIRECTIONS:
        rr, cc = r + dr, c + dc
        temp = []

        while in_bounds(rr, cc) and board[rr][cc] == opp:
            temp.append((rr, cc))
            rr += dr
            cc += dc

        if in_bounds(rr, cc) and board[rr][cc] == player and temp:
            flips.extend(temp)

    return flips


def is_valid_move(board, r, c, player):
    return len(get_flips(board, r, c, player)) > 0


def get_valid_moves(board, player):
    return [(r, c) for r in range(8) for c in range(8)
            if is_valid_move(board, r, c, player)]


def make_move(board, r, c, player):
    flips = get_flips(board, r, c, player)
    if not flips:
        return False

    board[r][c] = player
    for rr, cc in flips:
        board[rr][cc] = player
    return True


def calculate_score(board):
    black = sum(row.count('B') for row in board)
    white = sum(row.count('W') for row in board)
    return black, white


def game_over(board):
    return not get_valid_moves(board, 'B') and not get_valid_moves(board, 'W')


# ---------------- MINIMAX AI ---------------- #

def evaluate(board):
    b, w = calculate_score(board)
    return w - b   # AI = White


def minimax(board, depth, maximizing):
    if depth == 0 or game_over(board):
        return evaluate(board), None

    player = 'W' if maximizing else 'B'
    moves = get_valid_moves(board, player)

    if not moves:
        return evaluate(board), None

    best_move = None

    if maximizing:
        best_score = -9999
        for r, c in moves:
            temp = copy.deepcopy(board)
            make_move(temp, r, c, player)
            score, _ = minimax(temp, depth - 1, False)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_score, best_move

    else:
        best_score = 9999
        for r, c in moves:
            temp = copy.deepcopy(board)
            make_move(temp, r, c, player)
            score, _ = minimax(temp, depth - 1, True)

            if score < best_score:
                best_score = score
                best_move = (r, c)

        return best_score, best_move


def best_minimax_move(board, player, depth):
    _, move = minimax(board, depth, player == 'W')
    return move


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Othello with Minimax AI")
root.geometry("900x900+100+50")

board = create_board()
buttons = []

# Title
tk.Label(root, text="OTHELLO WITH MINIMAX AI",
         font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=8, pady=10)

black_label = tk.Label(root, text="Black: 2", font=("Arial", 14))
black_label.grid(row=9, column=0, columnspan=4)

white_label = tk.Label(root, text="White: 2", font=("Arial", 14))
white_label.grid(row=9, column=4, columnspan=4)

status_label = tk.Label(root, text="Your Turn (Black)",
                        font=("Arial", 14, "bold"))
status_label.grid(row=10, column=0, columnspan=8)


def update_score():
    b, w = calculate_score(board)
    black_label.config(text=f"Black: {b}")
    white_label.config(text=f"White: {w}")


def update_board():
    valid_moves = get_valid_moves(board, 'B')
    print("Valid moves:", valid_moves)

    for r in range(8):
        for c in range(8):

            if board[r][c] == 'B':
                buttons[r][c].config(text='B', bg='green', fg='white')

            elif board[r][c] == 'W':
                buttons[r][c].config(text='W', bg='green', fg='white')

            elif (r, c) in valid_moves:
                buttons[r][c].config(text='', bg='light green')

            else:
                buttons[r][c].config(text='', bg='green')

    update_score()

    if game_over(board):
        b, w = calculate_score(board)
        msg = "Black Wins!" if b > w else "White Wins!" if w > b else "Draw!"
        messagebox.showinfo("Game Over", f"Black: {b}\nWhite: {w}\n\n{msg}")


def ai_turn():
    move = best_minimax_move(board, 'W', 3)

    if not move:
        status_label.config(text="Your Turn (Black)")
        return

    make_move(board, move[0], move[1], 'W')
    update_board()
    status_label.config(text="Your Turn (Black)")


def player_move(r, c):
    if not is_valid_move(board, r, c, 'B'):
        messagebox.showwarning("Invalid Move", "Choose highlighted square")
        return

    make_move(board, r, c, 'B')
    update_board()

    status_label.config(text="AI Thinking...")
    root.after(400, ai_turn)


def restart_game():
    global board
    board = create_board()
    update_board()
    status_label.config(text="Your Turn (Black)")


# Create board UI
for r in range(8):
    row = []
    for c in range(8):
        btn = tk.Button(root, width=3, height=1,
                        font=('Arial', 18, 'bold'),
                        bg='green',
                        command=lambda r=r, c=c: player_move(r, c))
        btn.grid(row=r+1, column=c+1)
        row.append(btn)
    buttons.append(row)


tk.Button(root, text="Restart Game",
          font=("Arial", 12),
          command=restart_game).grid(row=11, column=0, columnspan=8, pady=10)

update_board()
root.mainloop()