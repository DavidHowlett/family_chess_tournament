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


def main(history, white_time, black_time):
    current_board = history[-1]
    if len(history) % 4 == 2:
        current_board[7][6] = '.'
        current_board[5][7] = 'n'
    else:
        current_board[5][7] = '.'
        current_board[7][6] = 'n'
    print('current score is:')
    print(score(current_board))
    return current_board
