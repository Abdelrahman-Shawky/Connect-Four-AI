import sys
import pygame
import functions
from minimax import next_move
from functions import *
import numpy as np
from Button import *

pygame.init()
pygame.display.set_caption('Connect Four')
screen = pygame.display.set_mode(SIZE)
my_font = pygame.font.SysFont("monospace", 60)
BG = pygame.image.load("assets/Background.png")


def start_game(game_mode, game_type, depth=0):
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
    if turn == AI:
        functions.AI_ODD = True
    else:
        functions.AI_ODD = False

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
                        if game_mode == 0:
                            if check_win(board, row, col, turn):
                                label = my_font.render("YOU Win", True, RED)
                                screen.blit(label, (40, 10))
                                pygame.display.update()
                                game_over = True
                            if check_full(board):
                                label = my_font.render("Tie", True, YELLOW)
                                screen.blit(label, (40, 10))
                                pygame.display.update()
                                game_over = True
                        elif game_mode == 1:
                            if check_full(board):
                                player_score = count_score(board, PLAYER)
                                ai_score = count_score(board, AI)
                                if player_score > ai_score:
                                    label_string = "YOU Win Score: " + str(player_score)
                                    label = my_font.render(label_string, True, RED)
                                elif ai_score > player_score:
                                    label_string = "AI Wins Score: " + str(ai_score)
                                    label = my_font.render(label_string, True, YELLOW)
                                else:
                                    label_string = "Tie Score: " + str(ai_score)
                                    label = my_font.render(label_string, True, YELLOW)
                                screen.blit(label, (40, 10))
                                pygame.display.update()
                                game_over = True
                        turn = AI
        if turn == AI and not game_over:
            if game_type == 0:
                col = random.randint(0, COL_COUNT - 1)
            elif game_type == 1:
                col = next_move(board, depth, False, game_mode)
            else:
                col = next_move(board, depth, True, game_mode)
            print("--------------------------------------------")
            if is_valid(board, col):
                # pygame.time.wait(100)
                row = get_row(board, col)
                add_tile(board, row, col, turn)
                draw_board(board)
                if game_mode == 0:
                    if check_win(board, row, col, turn):
                        label = my_font.render("AI wins", True, YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                    if check_full(board):
                        label = my_font.render("Tie", True, YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                elif game_mode == 1:
                    if check_full(board):
                        player_score = count_score(board, PLAYER)
                        ai_score = count_score(board, AI)
                        if player_score > ai_score:
                            label_string = "YOU Win Score: " + str(player_score)
                            label = my_font.render(label_string, True, RED)
                        elif ai_score > player_score:
                            label_string = "AI Wins Score: " + str(ai_score)
                            label = my_font.render(label_string, True, YELLOW)
                        else:
                            label_string = "Tie Score: " + str(ai_score)
                            label = my_font.render(label_string, True, YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                turn = PLAYER
        if game_over:
            pygame.time.wait(4000)
            screen.fill((0, 0, 0))
            screen.blit(BG, (0, 0))


def game_menu(game_mode):
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("Select Type", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 75))

        random_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 200),
                               text_input="RANDOM", font=my_font, base_color="#d7fcd4", hovering_color="White")
        no_pruning = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 325),
                            text_input="NO PRUNING", font=my_font, base_color="#d7fcd4", hovering_color="White")
        pruning = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 450),
                         text_input="PRUNING", font=my_font, base_color="#d7fcd4", hovering_color="White")
        back_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(350, 575),
                             text_input="BACK", font=my_font, base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [random_button, no_pruning, pruning, back_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if random_button.checkForInput(MENU_MOUSE_POS):
                    start_game(game_mode, 0)
                if no_pruning.checkForInput(MENU_MOUSE_POS):
                    select_depth(game_mode, 1)
                if pruning.checkForInput(MENU_MOUSE_POS):
                    select_depth(game_mode, 2)
                if back_button.checkForInput(MENU_MOUSE_POS):
                    select_mode()

        pygame.display.update()


def select_depth(game_mode, game_type):
    user_text = ''
    screen.fill((0, 0, 0,))
    screen.blit(BG, (0, 0))
    pygame.display.update()
    input_rect = pygame.Rect(150, 200, 400, 100)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    active = False

    while True:

        depth_text = my_font.render("Select Depth", True, "#b68f40")
        depth_rect = depth_text.get_rect(center=(350, 75))
        screen.blit(depth_text, depth_rect)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 400),
                             text_input="PLAY", font=my_font, base_color="#d7fcd4", hovering_color="White")
        back_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(350, 575),
                             text_input="BACK", font=my_font, base_color="#d7fcd4", hovering_color="White")
        for button in [play_button, back_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if play_button.checkForInput(MENU_MOUSE_POS):
                    start_game(game_mode, game_type, int(user_text))
                if back_button.checkForInput(MENU_MOUSE_POS):
                    game_menu(game_mode)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = my_font.render(user_text, True, "#b68f40")
        screen.blit(text_surface, (input_rect.x + 30, input_rect.y + 15))
        input_rect.w = max(text_surface.get_width(), 400)
        pygame.display.update()


def select_mode():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("Connect Four", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 75))

        normal_mode_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 250),
                            text_input="NORMAL", font=my_font, base_color="#d7fcd4", hovering_color="White")
        full_mode_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 375),
                         text_input="FULL", font=my_font, base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(350, 500),
                             text_input="QUIT", font=my_font, base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [normal_mode_button, full_mode_button, quit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if normal_mode_button.checkForInput(MENU_MOUSE_POS):
                    game_menu(0)
                if full_mode_button.checkForInput(MENU_MOUSE_POS):
                    game_menu(1)
                if quit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


select_mode()
