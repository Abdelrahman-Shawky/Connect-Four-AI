import sys
import pygame
from minimax import next_move
# from gui import *
from functions import *
import numpy as np
from Button import *

pygame.init()
pygame.display.set_caption('Connect Four')
screen = pygame.display.set_mode(SIZE)
my_font = pygame.font.SysFont("monospace", 60)
BG = pygame.image.load("assets/Background.png")


def start_game(game_type):
    # Create empty board to start the game
    def create_board():
        board = np.zeros((ROW_COUNT, COL_COUNT))  # create 2D array
        return board

    def draw_board(board):
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE,
                                 (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                # if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (
                    c * SQUARE_SIZE + SQUARE_SIZE / 2, int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   int(SQUARE_SIZE / 2 - 5))
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER:
                    pygame.draw.circle(screen, RED,
                                       (c * SQUARE_SIZE + SQUARE_SIZE / 2,
                                        HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                       int(SQUARE_SIZE / 2 - 5))
                elif board[r][c] == AI:
                    pygame.draw.circle(screen, YELLOW,
                                       (c * SQUARE_SIZE + SQUARE_SIZE / 2,
                                        HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
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
            # is_alpha_beta = True
            my_depth = 3
            if game_type == 0:
                col = random.randint(0, COL_COUNT - 1)
            elif game_type == 1:
                col = next_move(board, my_depth, False)
            else:
                col = next_move(board, my_depth, True)

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


def game_menu():
    # pygame.display.set_caption('Menu')
    while True:
        # screen.blit((0,0,255))
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("Connect Four", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 75))

        random_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 200),
                               text_input="RANDOM", font=my_font, base_color="#d7fcd4", hovering_color="White")
        no_pruning = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 325),
                            text_input="No Pruning", font=my_font, base_color="#d7fcd4", hovering_color="White")
        pruning = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 450),
                         text_input="PRUNING", font=my_font, base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(350, 575),
                             text_input="QUIT", font=my_font, base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [random_button, no_pruning, pruning, quit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if random_button.checkForInput(MENU_MOUSE_POS):
                    start_game(0)
                if no_pruning.checkForInput(MENU_MOUSE_POS):
                    start_game(1)
                if pruning.checkForInput(MENU_MOUSE_POS):
                    start_game(2)
                if quit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


game_menu()
