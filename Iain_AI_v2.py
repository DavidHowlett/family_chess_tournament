""""
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
"""
import copy
import random
PIECE_MOVE_DIRECTION = {
    'K': ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)),
    'k': ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
    'Q': ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)),
    'q': ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
    'R': ((1, 0), (0, 1), (-1, 0), (0, -1)),
    'r': ((1, 0), (0, 1), (-1, 0), (0, -1)),
    'B': ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    'b': ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    'N': ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)),
    'n': ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)),
}
PIECE_VALUE = {
    '.': 0,
    'K': 200, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1,
    'k': -200, 'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -1
}


def score(board):
    points = 0
    for row in board:
        for piece in row:
            points += PIECE_VALUE[piece]
    return points


def moves(board, white_turn):
    legal_moves = []
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if white_turn:
                if piece == 'N':
                    for y_move_direction, x_move_direction in PIECE_MOVE_DIRECTION[piece]:
                        new_y = y + y_move_direction
                        new_x = x + x_move_direction
                        if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                            if board[new_y][new_x] == '.' or board[new_y][new_x].islower():
                                new_board = copy.deepcopy(board)
                                new_board[y][x] = '.'
                                new_board[new_y][new_x] = 'N'
                                legal_moves.append(new_board)
                if piece == 'P' and y <= 6:
                    if board[y+1][x] == '.':
                        new_board = copy.deepcopy(board)
                        new_board[y][x] = '.'
                        new_board[y+1][x] = 'P'
                        legal_moves.append(new_board)
            else:
                if piece == 'n':
                    for y_move_direction, x_move_direction in PIECE_MOVE_DIRECTION[piece]:
                        new_y = y + y_move_direction
                        new_x = x + x_move_direction
                        if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                            if board[new_y][new_x] == '.' or board[new_y][new_x].isupper():
                                new_board = copy.deepcopy(board)
                                new_board[y][x] = '.'
                                new_board[new_y][new_x] = 'n'
                                legal_moves.append(new_board)
                if piece == 'p' and y >= 1:
                    if board[y-1][x] == '.':
                        new_board = copy.deepcopy(board)
                        new_board[y][x] = '.'
                        new_board[y-1][x] = 'p'
                        legal_moves.append(new_board)
    return legal_moves


def main(history, white_time, black_time):
    if len(history) % 2 == 1:
        white_turn = True
    else:
        white_turn = False
    current_board = history[-1]
    return moves(current_board, white_turn)[0]
    if len(history) % 4 == 2:
        current_board[7][6] = '.'
        current_board[5][7] = 'n'
    else:
        current_board[5][7] = '.'
        current_board[7][6] = 'n'
    '''print('current score is:')
    print(score(current_board))'''
    return current_board
