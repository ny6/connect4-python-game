from numpy import zeros, flip
from sys import exit
from math import floor
import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARE_SIZE = 100
HALF_SQUARE_SIZE = int(SQUARE_SIZE / 2)
RADIUS = HALF_SQUARE_SIZE - 5

WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)

pygame.init()
screen = pygame.display.set_mode(SIZE)

my_font = pygame.font.SysFont("monospace", 75)


def create_board():
    return zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(b: list, r: int, c: int, piece: int) -> None:
    board[r][c] = piece


def is_valid_location(b: list, c: int) -> bool:
    return b[ROW_COUNT - 1][c] == 0


def get_next_open_row(b: list, c: int):
    for r in range(ROW_COUNT):
        if b[r][c] == 0:
            return r


def print_board(b) -> None:
    print(flip(b, 0))


def draw_circle(c: int, r: int, color: str) -> None:
    pygame.draw.circle(
        screen, color,
        (c * SQUARE_SIZE + HALF_SQUARE_SIZE, HEIGHT - (r * SQUARE_SIZE + HALF_SQUARE_SIZE)),
        RADIUS
    )


def draw_board(b):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(
                screen, BLACK, (c * SQUARE_SIZE + HALF_SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE + HALF_SQUARE_SIZE),
                RADIUS
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if b[r][c] == 1:
                draw_circle(c, r, RED)
            elif b[r][c] == 2:
                draw_circle(c, r, GREEN)

    pygame.display.update()


def winning_move(b: list, piece: int) -> bool:
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if b[r][c] == piece and b[r][c + 1] == piece and b[r][c + 2] == piece and b[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == piece and b[r + 1][c] == piece and b[r + 2][c] == piece and b[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == piece and b[r + 1][c + 1] == piece and b[r + 2][c + 2] == piece and b[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if b[r][c] == piece and b[r - 1][c + 1] == piece and b[r - 2][c + 2] == piece and b[r - 3][c + 3] == piece:
                return True

    return False


board = create_board()
draw_board(board)
game_over = False
turn = 0

pygame.display.update()

while not game_over:
    player = turn + 1
    active_color = RED if player == 1 else GREEN

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            pygame.draw.circle(screen, active_color, (posx, HALF_SQUARE_SIZE), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            col = int(floor(posx / SQUARE_SIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player)

            if winning_move(board, player):
                label = my_font.render(f"Player {player} wins!!", 1, RED)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board)
            turn += 1
            turn %= 2

        if game_over:
            pygame.time.wait(3000)
