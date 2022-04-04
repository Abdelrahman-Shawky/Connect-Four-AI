import numpy as np
ROW_COUNT = 6
COL_COUNT = 7

# Create empty board to start the game
def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT)) #create 2D array
    return board

# Check if column is  valid for insertion
def is_valid(board, col):
    if board[ROW_COUNT-1][col] == 0:
        return True
    else:
        return False

# Get row of insertion
def current_location(board,col):
    row = 0 #point at bottom row
    while board[row][col] != 0:
        row += 1
    return row

def add_tile(board, row, col, tile):
    board[row][col] = tile

def check_win(board,row, col, tile):
    count = 0
    # Check horizontal
    temp_col = col
    temp_row = row
    while temp_col>=0 and board[temp_row][temp_col]==tile:
        count += 1
        temp_col -=1
    temp_col=col
    while temp_col<COL_COUNT and board[temp_row][temp_col]==tile:
        count += 1
        temp_col += 1
    if count>3:
        return True
    count = 0
    temp_col = col

    # Check Vertical
    while temp_row>=0 and board[temp_row][temp_col]==tile:
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
    while temp_col>=0 and temp_row>=0 and board[temp_row][temp_col]==tile:
        count += 1
        temp_row -= 1
        temp_col -= 1
    temp_col = col
    temp_row = row
    while temp_col<COL_COUNT and temp_row<ROW_COUNT and board[temp_row][temp_col]==tile:
        count += 1
        temp_row += 1
        temp_col += 1
    if count > 3:
        return True
    return False

board = create_board()  #create the empty board
game_over = False  #start game with false
turn = 1 #specify which player turn is it
while not game_over:
    if turn == 1:
        col = int(input("Player 1: "))
        if is_valid(board, col):
            row = current_location(board, col)
            add_tile(board, row, col, turn)
            if check_win(board,row, col, turn):
                print("Player 1 Winss")
        turn = 2
    else:
        col = int(input("Player 2: "))
        if is_valid(board, col):
            row = current_location(board, col)
            add_tile(board, row, col, turn)
        turn = 1
    print(board)


