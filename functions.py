from variables import *
import random

# global AI_ODD
AI_ODD = False


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
    if count - 1 >= num:
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
    if count - 1 >= num:
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
    if count - 1 >= num:
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
    if count - 1 >= num:
        return True

    return False


# Check if column is  valid for insertion
def is_valid(board, c):
    if board[ROW_COUNT - 1][c] == 0:
        return True
    else:
        return False


# Get row of insertion
def get_row(board, c):
    r = 0  # point at bottom row
    while board[r][c] != 0:
        r += 1
    return r


def add_tile(my_board, r, c, tile):
    my_board[r][c] = tile


def remove_tile(copy_board, r, c):
    copy_board[r][c] = 0


def scoring(window, tile):
    score = 0
    if tile == AI:
        opp = PLAYER
    else:
        opp = AI
    if window.count(tile) == 4:  # redundant
        score += 100
    elif window.count(tile) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(tile) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 30
    elif window.count(opp) == 2 and window.count(0) == 2:
        score -= 20
    return score


def horizontal_scoring(window, tile, row):
    score = 0
    print(AI_ODD)
    if tile == AI:
        opp = PLAYER
    else:
        opp = AI
    if window.count(tile) == 4:  # redundant
        score += 100
    elif window.count(tile) == 3 and window.count(0) == 1:
        if (AI_ODD and tile == AI) or (not AI_ODD and tile == PLAYER):
            if row == 1 or row == 3:
                score += 8
            elif row == 5:
                score += 7
            elif row == 2:
                score += 6
            else:
                score += 5
        elif (not AI_ODD and tile == AI) or (AI_ODD and tile == PLAYER):
            if row == 1 or row == 2:
                score += 8
            elif row == 4:
                score += 7
            elif row == 6 or row == 3:
                score += 6
            else:
                score += 5
    elif window.count(tile) == 2 and window.count(0) == 2:
        if (AI_ODD and tile == AI) or (not AI_ODD and tile == PLAYER):
            if row == 1 or row == 3:
                score += 4
            elif row == 5 or row == 2:
                score += 3
            else:
                score += 2
        elif (not AI_ODD and tile == AI) or (AI_ODD and tile == PLAYER):
            if row == 1 or row == 2:
                score += 4
            elif row == 4 or row == 3:
                score += 3
            else:
                score += 2
    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 30
    elif window.count(opp) == 2 and window.count(0) == 2:
        score -= 20
    return score


def vertical_scoring(window, tile, col):
    score = 0
    if tile == AI:
        opp = PLAYER
    else:
        opp = AI
    if window.count(tile) == 4:  # redundant
        score += 100
    elif window.count(tile) == 3 and window.count(0) == 1:
        if col == 4:
            score += 8
        elif col == 3 or col == 5:
            score += 7
        elif col == 2 or col == 6:
            score += 6
        else:
            score += 5
    elif window.count(tile) == 2 and window.count(0) == 2:
        if col == 4:
            score += 4
        elif col == 3 or col == 5:
            score += 3
        else:
            score += 2
    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 30
    elif window.count(opp) == 2 and window.count(0) == 2:
        score -= 20
    return score


def get_score(board, tile):
    score = 0
    # Center
    center = [int(i) for i in list(board[:, COL_COUNT // 2])]
    count = center.count(tile)
    score += count * 3

    # Horizontal
    for r in range(ROW_COUNT):
        current_row = [int(i) for i in list(board[r, :])]
        for c in range(COL_COUNT - 3):
            window = current_row[c:c + 4]
            score += horizontal_scoring(window, tile, r)

    # Vertical
    for c in range(COL_COUNT):
        current_col = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = current_col[r:r + 4]
            score += vertical_scoring(window, tile, c)

    # Positive Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += horizontal_scoring(window, tile, r)

    # Negative Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += horizontal_scoring(window, tile, r)

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
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == tile and board[r][c + 1] == tile and board[r][c + 2] == tile and board[r][c + 3] == tile:
                return True

    # Check vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == tile and board[r + 1][c] == tile and board[r + 2][c] == tile and board[r + 3][c] == tile:
                return True

    # Check positively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == tile and board[r + 1][c + 1] == tile and board[r + 2][c + 2] == tile and board[r + 3][
                c + 3] == tile:
                return True

    # Check negatively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == tile and board[r - 1][c + 1] == tile and board[r - 2][c + 2] == tile and board[r - 3][
                c + 3] == tile:
                return True


def is_terminal(board):
    return winning_move(board, AI) or winning_move(board, PLAYER) or len(valid_locations(board)) == 0


def valid_locations(board):
    valid = []
    for c in range(COL_COUNT):
        if is_valid(board, c):
            valid.append(c)
    return valid
