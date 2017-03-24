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


def main(history, white_time, black_time):
    current_board = history[-1]
    if len(history)%4==2:
        current_board[7][6] = '.'
        current_board[5][7] = 'n'
    else:
        current_board[5][7] = '.'
        current_board[7][6] = 'n'
    return current_board
