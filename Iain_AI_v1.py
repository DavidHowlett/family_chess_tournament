""" "
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
    if len(history) % 2 == 1:
        white_turn = True
    else:
        white_turn = False
    current_board = history[-1]
    if white_turn:
        if len(history) % 4 == 1:
            current_board[0][1] = "."
            current_board[2][0] = "N"
        else:
            current_board[2][0] = "."
            current_board[0][1] = "N"
    else:
        if len(history) % 4 == 2:
            current_board[7][6] = "."
            current_board[5][7] = "n"
        else:
            current_board[5][7] = "."
            current_board[7][6] = "n"
    return current_board
