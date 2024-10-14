"""
Tic Tac Toe Player
"""

import math
from util import Node, StackFrontier, QueueFrontier

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cnt_X = 0
    cnt_O = 0
    for sublist in board:
        for cell in sublist:
            if cell == X:
                cnt_X += 1
            elif cell == O:
                cnt_O += 1
    if cnt_X <= cnt_O or cnt_X == 0:
        return X
    return O
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] != X and board[i][j] != O:
                moves.add((i, j))
    return moves
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise ValueError
    to_play = player(board)
    result_board = []
    for sublist in board:
        l = []
        for cell in sublist:
            l.append(cell)
        result_board.append(l)
    if result_board[action[0]][action[1]] == X or result_board[action[0]][action[1]] == O:
        raise ValueError

    result_board[action[0]][action[1]] = to_play
    return result_board
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #check for diagnoses:
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    #check for rows and columns:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    if not actions(board):
        return True
    return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0
    #raise NotImplementedError

def max_play(board, min_rec):
    if terminal(board):
        return utility(board)
    moves = actions(board)
    v = -1
    for move in moves:
        v = max(v, min_play(result(board, move), v))
        if v == 1:
            return 1
        if v < min_rec:
            min_rec = v
    return v

def min_play(board, max_rec):
    if terminal(board):
        return utility(board)
    moves = actions(board)
    v = 1
    for move in moves:
        v = min(v, max_play(result(board, move), v))
        if v == -1:
            return -1
        if v > max_rec:
            max_rec = v
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board)):
        return None
    to_play = player(board)
    moves = actions(board)
    action : tuple
    if to_play == X:
        point = -1
        for move in moves:
            move_utility = min_play(result(board, move), point)
            if point < move_utility:
                point = move_utility
                action = move
            if point == 1:
                break
    else:
        point = int(1)
        for move in moves:
            move_utility = max_play(result(board, move), point)
            if point > move_utility:
                point = move_utility
                action = move
            if point == -1:
                break
    return action
