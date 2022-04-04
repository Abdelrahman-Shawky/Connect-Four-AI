import sys

import numpy as np
import pygame

ROW_COUNT = 6
COL_COUNT = 7
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0 ,0 )


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


def add_tile(board, row, col, tile):
    board[row][col] = tile


def check_win(board, row, col, tile):
    count = 0
    # Check horizontal
    temp_col = col
    temp_row = row
    while temp_col >= 0 and board[temp_row][temp_col] == tile:
        count += 1
        temp_col -= 1
    temp_col = col
    while temp_col < COL_COUNT and board[temp_row][temp_col] == tile:
        count += 1
        temp_col += 1
    if count > 3:
        return True
    count = 0
    temp_col = col

    # Check Vertical
    while temp_row >= 0 and board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
    temp_row = row
    while temp_row < ROW_COUNT and board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
    if count > 3:
        return True
    count = 0

    # Check Diagonal
    temp_col = col
    temp_row = row
    while temp_col >= 0 and temp_row >= 0 and board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
        temp_col -= 1
    temp_col = col
    temp_row = row
    while temp_col < COL_COUNT and temp_row < ROW_COUNT and board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
        temp_col += 1
    if count > 3:
        return True
    return False


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
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (c * SQUARESIZE + SQUARESIZE / 2, height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   int(SQUARESIZE / 2 - 5))
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (c * SQUARESIZE + SQUARESIZE / 2, height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   int(SQUARESIZE / 2 - 5))
    pygame.display.update()


board = create_board()  # create the empty board
game_over = False  # start game with false
turn = 1  # specify which player turn is it

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
            if turn == 1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), int(SQUARESIZE / 2 - 5))
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), int(SQUARESIZE / 2 - 5))
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == 1:
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
                turn = 2
            else:
                col = event.pos[0] // SQUARESIZE
                if is_valid(board, col):
                    row = current_location(board, col)
                    add_tile(board, row, col, turn)
                    draw_board(board)
                    if check_win(board, row, col, turn):
                        label = myfont.render("Player 2 wins", True, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                turn = 1
        print(board)
        if game_over:
            pygame.time.wait(3000)
