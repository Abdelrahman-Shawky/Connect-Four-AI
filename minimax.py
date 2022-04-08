import random
import sys
import math
import numpy as np
import pygame
from Node import *
from variables import *
from functions import *
# from main import add_tile, is_valid, get_row, AI, PLAYER, COL_COUNT, ROW_COUNT


def minimax(board, depth, maximizing_player, root):
    valid = valid_locations(board)
    if depth == 0 or is_terminal(board):
        if is_terminal(board):
            if winning_move(board, AI):
                my_score = 1000000
                root.score = my_score
                return None, my_score
            elif winning_move(board, PLAYER):
                my_score = -1000000
                root.score = my_score
                return None, -my_score
            else:  # full
                return None, 0
        else:
            my_score = get_score(board, AI)
            root.score = my_score
            return None, my_score
    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid)
        for c in valid:
            childNode = Node(root, -math.inf, root.get_child_state())
            root.add_child(childNode)
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, AI)
            # print(temp_board)
            new_score = minimax(temp_board, depth-1, False, childNode)[1]
            # print("2")
            # print(new_score)
            # print(new_score)
            # print("--------------------------")
            if new_score > value:
                value = new_score
                best_col = c
        root.score = value
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid)
        for c in valid:
            childNode = Node(root, -math.inf, root.get_child_state())
            root.add_child(childNode)
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, PLAYER)
            new_score = minimax(temp_board, depth - 1, True, childNode)[1]
            if new_score < value:
                value = new_score
                best_col = c
        root.score = value
        return best_col, value


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player, root):
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
            childNode = Node(root, -math.inf, root.get_child_state())
            root.add_child(childNode)
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, AI)
            new_score = minimax_alpha_beta(temp_board, depth-1, alpha, beta, False, childNode)[1]
            if new_score > value:
                value = new_score
                best_col = c
            alpha = max(alpha, value)
            if alpha >= beta:
                root.score = str(value) + "cut off"
                break
        root.score = value
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid)
        for c in valid:
            childNode = Node(root, -math.inf, root.get_child_state())
            root.add_child(childNode)
            r = get_row(board, c)
            temp_board = board.copy()
            add_tile(temp_board, r, c, PLAYER)
            new_score = minimax_alpha_beta(temp_board, depth - 1, alpha, beta, True, childNode)[1]
            if new_score < value:
                value = new_score
                best_col = c
            beta = min(beta, value)
            if alpha >= beta:
                root.score = str(value) + "cut off"
                break
        root.score = value
        return best_col, value


def next_move(board, depth, alpha_beta):
    root = Node(None, -math.inf, True)
    if alpha_beta:
        c = minimax_alpha_beta(board, depth, -math.inf, math.inf, True, root)[0]
    else:
        c = minimax(board, depth, True, root)[0]
    root.printTree(2)
    return c