import random
import sys
import math
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
def get_row(board, col):
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
    open_bottom = True
    open_top = True
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
    open_4 = True

    # Check Vertical
    while temp_row >= 0 and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row -= 1
    # bottom = temp_row
    # if bottom == -1 or temp_board[bottom][temp_col] == PLAYER:
    #     open_bottom = False
    temp_row = r
    while temp_row < ROW_COUNT and temp_board[temp_row][temp_col] == tile:
        count += 1
        temp_row += 1
    top = temp_row
    if top == ROW_COUNT or temp_board[top][temp_col] == PLAYER:
        open_4 = False
    if count - 1 == num:
        if open_4:
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
            r = get_row(copy_board, c)
            add_tile(copy_board, r, c, AI)
            # Offensive
            scores[c] = check_move(copy_board, r, c, 2) * 2 + scores.get(c, 0)
            scores[c] = check_move(copy_board, r, c, 3) * 4 + scores.get(c, 0)
            if check_win(copy_board, r, c, AI):
                scores[c] = 1000 + scores.get(c, 0)
                return c
            remove_tile(copy_board, r, c)
    return max(scores, key=scores.get)


def scoring(window, tile):
    score = 0
    if tile == AI:
        opp = PLAYER
    else:
        opp = AI
    if window.count(tile) == 4:
        score += 100
    elif window.count(tile) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(tile) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 4
    return score


def get_score(board, tile):
    score = 0
    # Center
    center = [int(i) for i in list(board[:, COL_COUNT//2])]
    count = center.count(tile)
    score += count*3

    # Horizontal
    for r in range(ROW_COUNT):
        current_row = [int(i) for i in list(board[r, :])]
        for c in range(COL_COUNT - 3):
            window = current_row[c:c + 4]
            score += scoring(window, tile)

    # Vertical
    for c in range(COL_COUNT):
        current_col = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = current_col[r:r + 4]
            score += scoring(window, tile)

    # Positive Diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += scoring(window, tile)

    # Negative Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += scoring(window, tile)

    return score


def pick_best_move(board, tile):
    valid = valid_locations(board)
    best = 0
    best_col = random.choice(valid)
    for c in valid:
        r = get_row(board, c)
        temp_board = board.copy()
        add_tile(temp_board, r, c, tile)
        score = get_score(temp_board, tile)
        if score > best:
            best = score
            best_col = c
    return best_col


def winning_move(board, tile):
    # Check horizontal locations for win
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == tile and board[r][c + 1] == tile and board[r][c + 2] == tile and board[r][c + 3] == tile:
                return True

    # Check vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == tile and board[r + 1][c] == tile and board[r + 2][c] == tile and board[r + 3][c] == tile:
                return True

    # Check positively sloped diagonals
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == tile and board[r + 1][c + 1] == tile and board[r + 2][c + 2] == tile and board[r + 3][c + 3] == tile:
                return True

    # Check negatively sloped diagonals
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == tile and board[r - 1][c + 1] == tile and board[r - 2][c + 2] == tile and board[r - 3][c + 3] == tile:
                return True


def is_terminal(board):
    return winning_move(board, AI) or winning_move(board, PLAYER) or len(valid_locations(board)) == 0


def minimax(board, depth, maximizing_player):
    valid = valid_locations(board)
    if depth == 0 or is_terminal(board):
        if is_terminal(board):
            if winning_move(board, AI):
                return None, 1000000
            elif winning_move(board, PLAYER):
                return None, -1000000
            else:
                return None, 0
        else:
            return None, get_score(board, AI)
    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid)
        for c in valid:
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, AI)
            new_score = minimax(temp_board, depth-1, False)[1]
            if new_score > value:
                value = new_score
                best_col = c
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid)
        for c in valid:
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, PLAYER)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                best_col = c
        return best_col, value


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    valid = valid_locations(board)
    if depth == 0 or is_terminal(board):
        if is_terminal(board):
            if winning_move(board, AI):
                return None, 10000000000
            elif winning_move(board, PLAYER):
                return None, -1000000000
            else:
                return None, 0
        else:
            return None, get_score(board, AI)
    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid)
        for c in valid:
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, AI)
            new_score = minimax_alpha_beta(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = c
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid)
        for c in valid:
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, PLAYER)
            new_score = minimax_alpha_beta(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = c
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def valid_locations(board):
    valid = []
    for c in range(COL_COUNT):
        if is_valid(board, c):
            valid.append(c)
    return valid


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
        # score, col = minimax(board, 3, True)
        col, score = minimax_alpha_beta(board, 4, -math.inf, math.inf, True)
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
