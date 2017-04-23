"""For fun I will try to write a player with no ability to search ahead, only an eval function"""
import David_AI_v8 as ai
from copy import copy

PIECE_MOVE_DIRECTION = {
    'R': (1, 16, -1, -16),
    'B': (1+16, 1-16, 16-1, -1-16),
    'N': (1+2*16, 1-2*16, -1+2*16, -1-2*16, 2+16, 2-16, -2+16, -2-16)}
PIECE_MOVE_DIRECTION['K'] = PIECE_MOVE_DIRECTION['R'] + PIECE_MOVE_DIRECTION['B']
PIECE_MOVE_DIRECTION['Q'] = PIECE_MOVE_DIRECTION['K']
for _piece in copy(PIECE_MOVE_DIRECTION):
    PIECE_MOVE_DIRECTION[_piece.lower()] = PIECE_MOVE_DIRECTION[_piece]
PIECE_VALUE = {
    '.': 0,
    'K': 20000, 'Q': 975, 'R': 500, 'B': 335, 'N': 325, 'P': 100,
    'k': -20000, 'q': -975, 'r': -500, 'b': -335, 'n': -325, 'p': -100
}
POSITION_VALUE_READABLE = {
    'P': [
        [0,   0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,   5, 10, 25, 25, 10,  5,  5],
        [0,   0,  0,  2,  2,  0,  0,  0],
        [5,  -5,-10,  0,  0,-10, -5,  5],
        [5,  10, 10,-20,-20, 10, 10,  5],
        [0,   0,  0,  0,  0,  0,  0,  0]],
    # [[5*(x - (x * x / 7))+(0.02 * (y+2)**4)-10 for x in range(8)] for y in range(7, -1, -1)],
    # print('\n'.join(' '.join('{}'.format(int(PAWN_POSITION_VALUE[y][x]))
    #   for x in range(8))for y in range(8))+'\n')
    'N': [
        [-8,  -8, -8, -8, -8, -8, -8, -8],
        [-8,   0, 0, 0, 0, 0, 0, -8],
        [-8,   0, 4, 6, 6, 4, 0, -8],
        [-8,   0, 6, 8, 8, 6, 0, -8],
        [-8,   0, 6, 8, 8, 6, 0, -8],
        [-8,   0, 4, 6, 6, 4, 0, -8],
        [-8,   0, 1, 2, 2, 1, 0, -8],
        [-16,-12, -8, -8, -8, -8, -12, -16]],
    'B': [
        [-4, -4, -4, -4, -4, -4, -4, -4],
        [-4, 0, 0, 0, 0, 0, 0, -4],
        [-4, 0, 2, 4, 4, 2, 0, -4],
        [-4, 0, 4, 6, 6, 4, 0, -4],
        [-4, 0, 4, 6, 6, 4, 0, -4],
        [-4, 1, 2, 4, 4, 2, 1, -4],
        [-4, 2, 1, 1, 1, 1, 2, -4],
        [-4, -4, -12, -4, -4, -12, -4, -4]],
    'R': [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 2, 2, 0, 0, 0]],
    'Q': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 2, 2, 1, 0, 0],
        [0, 0, 2, 3, 3, 2, 0, 0],
        [0, 0, 2, 3, 3, 2, 0, 0],
        [0, 0, 1, 2, 2, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [-5, -5, -5, -5, -5, -5, -5, -5]],
    # this should change with the game's phase
    'K': [
        [-40, -30, -50, -70, -70, -50, -30, -40],
        [-30, -20, -40, -60, -60, -40, -20, -30],
        [-20, -10, -30, -50, -50, -30, -10, -20],
        [-10, 0, -20, -40, -40, -20, 0, -10],
        [0, 10, -10, -30, -30, -10, 10, 0],
        [10, 20, 0, -20, -20, 0, 20, 10],
        [30, 40, 20, 0,   0, 20, 40, 30],
        [40, 50, 30, 10, 10, 30, 50, 40]],
    '.': [[0 for _ in range(8)] for _ in range(8)]
}
# The last 4 chars of the board contain the castling rights.
# If the char is true then castling is allowed
BOTTOM_LEFT_CASTLING = 124
BOTTOM_RIGHT_CASTLING = 125
TOP_LEFT_CASTLING = 126
TOP_RIGHT_CASTLING = 127
POSITION_VALUE = dict()
for piece_ in POSITION_VALUE_READABLE:
    POSITION_VALUE[piece_] = []
    POSITION_VALUE[piece_.lower()] = []
    for row in POSITION_VALUE_READABLE[piece_].__reversed__():
        POSITION_VALUE[piece_].extend(
            [PIECE_VALUE[piece_]+value for value in row]+[None]*8)
    for row in POSITION_VALUE_READABLE[piece_]:
        POSITION_VALUE[piece_.lower()].extend(
            [-PIECE_VALUE[piece_]-value for value in row.__reversed__()]+[None]*8)
assert len(POSITION_VALUE['K']) == 128


def evaluate(board)->float:
    return sum(POSITION_VALUE[board[x+16*y]][x+16*y] for x in range(8) for y in range(8))


def main(given_history, white_time, black_time):
    history = ai.to_array(given_history)
    player_is_white = len(history) % 2 == 1
    current_board = history[-1]
    best_score = -10**10
    for move, diff in ai.moves(current_board, player_is_white):
        score = evaluate(move)
        if not player_is_white:
            score *= -1
        if score > best_score:
            best_score = score
            best_move = move
    print(f'search depth: 1')
    print(f'expected score: {best_score}')
    return ai.from_array(best_move)
