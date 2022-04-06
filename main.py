import random
import sys

import numpy as np
import pygame

ROW_COUNT = 6
COL_COUNT = 7
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PLAYER = 1
AI = 2


# Create empty board to start the game
def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))  # create 2D array
    return board


# Check if column is  valid for insertion
def is_valid(board, col):
    if board[ROW_COUNT - 1][col] == 0:
        return True
    else:
        return False


# Get row of insertion
def current_location(board, col):
    row = 0  # point at bottom row
    while board[row][col] != 0:
        row += 1
    return row


def add_tile(my_board, r, c, tile):
    my_board[r][c] = tile


def remove_tile(copy_board, r, c):
    copy_board[r][c] = 0


def check_win(temp_board, r, c, tile, num=4):
    count = 0
    # Check horizontal
    temp_col = c
    temp_row = r
    while temp_col >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_col -= 1
    temp_col = c
    while temp_col < COL_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_col += 1
    if count - 1 == num:
        return True
    count = 0
    temp_col = c

    # Check Vertical
    while temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
    temp_row = r
    while temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
    if count - 1 == num:
        return True
    count = 0

    # Check Positive Diagonal
    temp_col = c
    temp_row = r
    while temp_col >= 0 and temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
        temp_col -= 1
    temp_col = c
    temp_row = r
    while temp_col < COL_COUNT and temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
        temp_col += 1
    if count - 1 == num:
        return True
    count = 0

    # Check Negative Diagonal
    temp_col = c
    temp_row = r
    while temp_col >= 0 and temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
        temp_col -= 1
    temp_col = c
    temp_row = r
    while temp_col < COL_COUNT and temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
        temp_col += 1
    if count - 1 == num:
        return True

    return False


def check_move(temp_board, r, c, num, tile=AI):
    count = 0
    # Check horizontal
    temp_col = c
    temp_row = r
    multiples = 0
    open_4 = True  # check if four is possible
    open_right = True  # check if right is open
    open_left = True  # check if left is open
    while temp_col >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_col -= 1
    left = temp_col
    if left == -1 or temp_board[temp_row][left] == PLAYER:
        open_left = False
    temp_col = c
    while temp_col < COL_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_col += 1
    right = temp_col
    if right == COL_COUNT or temp_board[temp_row][right] == PLAYER:
        open_right = False
    if count - 1 == num:
        if num == 2:
            if not open_left and open_right:
                if temp_board[temp_row][right + 1] != 0 and temp_board[temp_row][right + 2] != 0:
                    open_4 = False
            elif open_left and not open_right:
                if temp_board[temp_row][left - 1] != 0 and temp_board[temp_row][left - 2] != 0:
                    open_4 = False
            elif not open_left and not open_right:
                open_4 = False
        elif num == 3:
            if not open_left and not open_right:
                open_4 = False
        if open_4:
            multiples += 1
    count = 0
    temp_col = c

    # Check Vertical
    while temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
    temp_row = r
    while temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
    if count - 1 == num:
        multiples += 1
    count = 0

    # Check Positive Diagonal
    temp_col = c
    temp_row = r
    while temp_col >= 0 and temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
        temp_col -= 1
    temp_col = c
    temp_row = r
    while temp_col < COL_COUNT and temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
        temp_col += 1
    if count - 1 == num:
        multiples += 1

    # Check Negative Diagonal
    count = 0
    temp_col = c
    temp_row = r
    while temp_col >= 0 and temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
        temp_col -= 1
    temp_col = c
    temp_row = r
    while temp_col < COL_COUNT and temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
        temp_col += 1
    if count - 1 == num:
        multiples += 1

    return multiples


def score_position(board):
    copy_board = board.copy()  # to simulate another board
    best_score = 0
    scores = {}
    # Horizontal
    for c in range(COL_COUNT):
        if is_valid(copy_board, c):
            r = current_location(copy_board, c)
            add_tile(copy_board, r, c, AI)
            # if c in scores:
            scores[c] = check_move(copy_board, r, c, 2) * 2 + scores.get(c, 0)
            scores[c] = check_move(copy_board, r, c, 3) * 4 + scores.get(c, 0)
            if check_win(copy_board, r, c, AI):
                scores[c] = 1000 + scores.get(c, 0)
                return c
            remove_tile(copy_board, r, c)
    return max(scores, key=scores.get)


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # if board[r][c] == 0:
            pygame.draw.circle(screen, BLACK, (
                c * SQUARESIZE + SQUARESIZE / 2, int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                               int(SQUARESIZE / 2 - 5))
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED,
                                   (c * SQUARESIZE + SQUARESIZE / 2, height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   int(SQUARESIZE / 2 - 5))
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW,
                                   (c * SQUARESIZE + SQUARESIZE / 2, height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   int(SQUARESIZE / 2 - 5))
    pygame.display.update()


board = create_board()  # create the empty board
game_over = False  # start game with false
turn = random.randint(PLAYER, AI)  # specify which player turn is it

pygame.init()
pygame.display.set_caption('Connect Four')
SQUARESIZE = 100
width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
myfont = pygame.font.SysFont("monospace", 60)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), int(SQUARESIZE / 2 - 5))
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), int(SQUARESIZE / 2 - 5))
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                col = event.pos[0] // SQUARESIZE
                if is_valid(board, col):
                    row = current_location(board, col)
                    add_tile(board, row, col, turn)
                    draw_board(board)
                    if check_win(board, row, col, turn):
                        label = myfont.render("Player 1 wins", True, RED)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                    turn = AI
    if turn == AI and not game_over:
        # col = random.randint(0, COL_COUNT-1)
        col = score_position(board)
        if is_valid(board, col):
            pygame.time.wait(500)
            row = current_location(board, col)
            add_tile(board, row, col, turn)
            draw_board(board)
            if check_win(board, row, col, turn):
                label = myfont.render("AI wins", True, YELLOW)
                screen.blit(label, (40, 10))
                pygame.display.update()
                game_over = True
            turn = PLAYER
    print(board)
    if game_over:
        pygame.time.wait(3000)
