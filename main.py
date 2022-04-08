import random
import sys
import math
import numpy as np
import pygame
from Node import *
from minimax import next_move
# from variables import *
from functions import *


# Create empty board to start the game
def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))  # create 2D array
    return board


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
                    row = get_row(board, col)
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
        # col = pick_best_move(board)
        is_aplha_beta = True
        my_depth = 3
        col = next_move(board, my_depth, is_aplha_beta)

        # col, score = minimax(board, 3, True)
        print("----------------------")
        # col, score = minimax_alpha_beta(board, 4, -math.inf, math.inf, True)
        if is_valid(board, col):
            pygame.time.wait(100)
            row = get_row(board, col)
            add_tile(board, row, col, turn)
            draw_board(board)
            if check_win(board, row, col, turn):
                label = myfont.render("AI wins", True, YELLOW)
                screen.blit(label, (40, 10))
                pygame.display.update()
                game_over = True
            turn = PLAYER
    # print(board)
    if game_over:
        pygame.time.wait(3000)
