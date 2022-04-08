import sys
import pygame
from minimax import next_move
# from gui import *
from functions import *
import numpy as np

pygame.init()
pygame.display.set_caption('Connect Four')
screen = pygame.display.set_mode(SIZE)
my_font = pygame.font.SysFont("monospace", 60)


def start_game():
    # Create empty board to start the game
    def create_board():
        board = np.zeros((ROW_COUNT, COL_COUNT))  # create 2D array
        return board

    def draw_board(board):
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                # if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (
                    c * SQUARE_SIZE + SQUARE_SIZE / 2, int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   int(SQUARE_SIZE / 2 - 5))
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER:
                    pygame.draw.circle(screen, RED,
                                       (c * SQUARE_SIZE + SQUARE_SIZE / 2, HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                       int(SQUARE_SIZE / 2 - 5))
                elif board[r][c] == AI:
                    pygame.draw.circle(screen, YELLOW,
                                       (c * SQUARE_SIZE + SQUARE_SIZE / 2, HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                       int(SQUARE_SIZE / 2 - 5))
        pygame.display.update()

    board = create_board()  # create the empty board
    game_over = False  # start game with false
    turn = random.randint(PLAYER, AI)  # specify which player turn is it

    draw_board(board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), int(SQUARE_SIZE / 2 - 5))
                else:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), int(SQUARE_SIZE / 2 - 5))
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                if turn == PLAYER:
                    col = event.pos[0] // SQUARE_SIZE
                    if is_valid(board, col):
                        row = get_row(board, col)
                        add_tile(board, row, col, turn)
                        draw_board(board)
                        if check_win(board, row, col, turn):
                            label = my_font.render("Player 1 wins", True, RED)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            game_over = True
                        turn = AI
        if turn == AI and not game_over:
            # col = random.randint(0, COL_COUNT-1)
            # col = pick_best_move(board)
            is_alpha_beta = True
            my_depth = 3
            col = next_move(board, my_depth, is_alpha_beta)

            # col, score = minimax(board, 3, True)
            print("----------------------")
            # col, score = minimax_alpha_beta(board, 4, -math.inf, math.inf, True)
            if is_valid(board, col):
                pygame.time.wait(100)
                row = get_row(board, col)
                add_tile(board, row, col, turn)
                draw_board(board)
                if check_win(board, row, col, turn):
                    label = my_font.render("AI wins", True, YELLOW)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    game_over = True
                turn = PLAYER
        # print(board)
        if game_over:
            pygame.time.wait(3000)

#
# def game_menu():
#     while True:
#         screen.fill((0,0,255))
#         draw_text("main menu", my_font)


start_game()
