"""
Tic Tac Toe Player
"""

import math
import copy

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
    x_counter = 0
    o_counter = 0
    for row in board:
        for item in row:
            if item == "X": x_counter += 1
            elif item == "O": o_counter += 1

    if o_counter < x_counter:
        return "O"
    return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_moves = set()
    for row in range(len(board)):
        for item in range(len(board[row])):
            if board[row][item] == EMPTY:
                available_moves.add((row, item))
    return available_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    turn = player(board)
    if result_board[action[0]][action[1]] == EMPTY:
        result_board[action[0]][action[1]] = turn
        return result_board
    raise ValueError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if (
        board[1][1] is not EMPTY
        and (
            (board[0][0] == board[1][1] and board[0][0] == board[2][2])
            or (board[0][2] == board[1][1] and board[0][2] == board[2][0])
        )
    ):
        return board[1][1]
    for row_idx in range(len(board)):
        if board[row_idx][1] is not EMPTY and len(set(board[row_idx])) == 1:
            return board[row_idx][1]
        if (
            board[1][row_idx] is not EMPTY
            and len(set([board[0][row_idx], board[1][row_idx], board[2][row_idx]])) == 1
        ):
            return board[0][row_idx]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for item in row:
            if item == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def max_value(state, alpha, beta):
        if terminal(state):
            return utility(state)
        value = -math.inf
        for action in actions(state):
            value = max(value, min_value(result(state, action), alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def min_value(state, alpha, beta):
        if terminal(state):
            return utility(state)
        value = math.inf
        for action in actions(state):
            value = min(value, max_value(result(state, action), alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    current_player = player(board)
    best_action = None

    if current_player == "X":
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action), -math.inf, math.inf)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action), -math.inf, math.inf)
            if value < best_value:
                best_value = value
                best_action = action

    return best_action