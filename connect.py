from numpy import zeros, flip

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    return zeros((6, 7))


def drop_piece(b: list, r: int, c: int, piece: int) -> None:
    board[r][c] = piece


def is_valid_location(b: list, c: int) -> bool:
    return b[5][c] == 0


def get_next_open_row(b: list, c: int):
    for r in range(ROW_COUNT):
        if b[r][c] == 0:
            return r


def print_board(b) -> None:
    print(flip(b, 0))


board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    # Ask for player 1 input
    if turn == 0:
        col = int(input("Player 1 make your selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
    # Ask for player 2 input
    else:
        col = int(input("Player 2 make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

    print_board(board)

    turn += 1
    turn %= 2
