BOARD_SIZE = 8

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def create_board():
    board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'

    return board


def print_board(board):
    print("\n  0 1 2 3 4 5 6 7")

    for i in range(8):
        print(i, end=" ")
        print(" ".join(board[i]))

    print()


def is_valid_move(board, row, col, player):

    if not (0 <= row < 8 and 0 <= col < 8):
        return False

    if board[row][col] != '.':
        return False

    opponent = 'W' if player == 'B' else 'B'

    for dr, dc in directions:

        r = row + dr
        c = col + dc

        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8:

            if board[r][c] == opponent:
                found_opponent = True

            elif board[r][c] == player:

                if found_opponent:
                    return True

                break

            else:
                break

            r += dr
            c += dc

    return False


def get_valid_moves(board, player):

    moves = []

    for r in range(8):
        for c in range(8):

            if is_valid_move(board, r, c, player):
                moves.append((r, c))

    return moves


def make_move(board, row, col, player):

    opponent = 'W' if player == 'B' else 'B'

    board[row][col] = player

    for dr, dc in directions:

        r = row + dr
        c = col + dc

        pieces_to_flip = []

        while 0 <= r < 8 and 0 <= c < 8:

            if board[r][c] == opponent:

                pieces_to_flip.append((r, c))

            elif board[r][c] == player:

                for fr, fc in pieces_to_flip:
                    board[fr][fc] = player

                break

            else:
                break

            r += dr
            c += dc


def calculate_score(board):

    black = 0
    white = 0

    for row in board:
        black += row.count('B')
        white += row.count('W')

    return black, white


def copy_board(board):
    return [row[:] for row in board]


def simulate_move(board, move, player):

    new_board = copy_board(board)

    make_move(new_board, move[0], move[1], player)

    return new_board


WEIGHTS = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]


def evaluate_board(board):

    score = 0

    for r in range(8):
        for c in range(8):

            if board[r][c] == 'B':
                score += WEIGHTS[r][c]

            elif board[r][c] == 'W':
                score -= WEIGHTS[r][c]

    return score


def minimax(board, depth, maximizing):

    if depth == 0:
        return evaluate_board(board)

    player = 'B' if maximizing else 'W'

    moves = get_valid_moves(board, player)

    if not moves:
        return evaluate_board(board)

    if maximizing:

        best = float('-inf')

        for move in moves:

            temp = simulate_move(board, move, player)

            value = minimax(temp, depth - 1, False)

            best = max(best, value)

        return best

    else:

        best = float('inf')

        for move in moves:

            temp = simulate_move(board, move, player)

            value = minimax(temp, depth - 1, True)

            best = min(best, value)

        return best


def best_minimax_move(board, player, depth):

    moves = get_valid_moves(board, player)

    if not moves:
        return None

    best_move = None

    if player == 'B':

        best_score = float('-inf')

        for move in moves:

            temp = simulate_move(board, move, player)

            score = minimax(temp, depth - 1, False)

            if score > best_score:
                best_score = score
                best_move = move

    else:

        best_score = float('inf')

        for move in moves:

            temp = simulate_move(board, move, player)

            score = minimax(temp, depth - 1, True)

            if score < best_score:
                best_score = score
                best_move = move

    return best_move


def game_over(board):

    return (
        len(get_valid_moves(board, 'B')) == 0 and
        len(get_valid_moves(board, 'W')) == 0
    )


def play_game():

    board = create_board()

    print("OTHELLO WITH MINIMAX AI")
    print("You are Black (B)")
    print("AI is White (W)")

    while not game_over(board):

        print_board(board)

        black, white = calculate_score(board)

        print("Black:", black, "| White:", white)

        player_moves = get_valid_moves(board, 'B')

        if player_moves:

            print("Valid Moves:", player_moves)

            try:

                row = int(input("Enter row: "))
                col = int(input("Enter col: "))

                if (row, col) not in player_moves:
                    print("Invalid Move")
                    continue

                make_move(board, row, col, 'B')

            except ValueError:
                print("Enter numbers only")
                continue

        ai_moves = get_valid_moves(board, 'W')

        if ai_moves:

            ai_move = best_minimax_move(board, 'W', 3)

            print("\nAI plays:", ai_move)

            make_move(board, ai_move[0], ai_move[1], 'W')

    print("\nFINAL BOARD")
    print_board(board)

    black, white = calculate_score(board)

    print("Final Score")
    print("Black:", black)
    print("White:", white)

    if black > white:
        print("Winner: Black")
    elif white > black:
        print("Winner: White")
    else:
        print("Match Draw")


if __name__ == "__main__":
    play_game()