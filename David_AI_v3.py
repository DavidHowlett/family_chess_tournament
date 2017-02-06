"""This was written by David for fun
This program implements a tree search of possible future moves.
The main data structures are:
    - board: this is a [str] representing a 2D board
    - state: a list representing a node in a the search tree. It contains a board and some metadata.

A board can be scored with the score function.

The score of a state can be simply calculated by passing its associated board to the score function. To get a more
accurate score of a position it is necessary to explore the children of the state.

Not implemented yet:
    - castling
    - en passant
    - avoiding trading our king now for their king later

"""
from time import perf_counter as now
from shared import StalemateException, ThreeFoldRepetition

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
    'K': 1000, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 0.7,
    'k': -1000, 'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -0.7}


# for most pieces there is a small advantage to being in the centre
POSITION_VALUE = [[0.02 * (3 + x - x * x / 7) * (1 + y - y * y / 7) for x in range(8)] for y in range(8)]
#  print('\n'.join(' '.join('{:.2f}'.format(POSITION_VALUE[y][x])for x in range(8))for y in range(8))+'\n')
# pawns are more valuable in the centre but more importantly they become much more valuable when they are close to being
# turned into queens
# calculating the below formula takes 861 ns but lookup in a 2D table only takes 73 ns.
# This is the reason for pre-calculation
PAWN_POSITION_VALUE = [[0.006 * (10 + x - x * x / 7) * (y+2) ** 2 for x in range(8)] for y in range(8)]
#  print('\n'.join(' '.join('{:.2f}'.format(PAWN_POSITION_VALUE[y][x])for x in range(8))for y in range(8))+'\n')
total_moves = 0


def move(board: [str], y1, x1, y2, x2)-> [str]:
    """returns a board with a move made"""
    board = board.copy()
    # add piece to destination
    line = board[y2]
    board[y2] = line[:x2] + board[y1][x1] + line[x2 + 1:]
    # remove piece from source
    line = board[y1]
    board[y1] = line[:x1] + '.' + line[x1 + 1:]
    return board


def moves(board: [str], _player_is_white: bool)->[([str], float)]:
    global total_moves
    """This generates a list of all possible game states after one move.
    Preferred moves should be later in the returned list."""
    _moves = []
    position_multipler = 1 if _player_is_white else -1
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece in 'KQRBN' if _player_is_white else piece in 'kqrbn':
                for xd, yd in PIECE_MOVE_DIRECTION[piece]:
                    for i in range(1, 100):
                        x2 = x+i*xd
                        y2 = y+i*yd
                        if not (0 <= x2 <= 7 and 0 <= y2 <= 7):
                            # then it is a move off the board
                            break
                        target_piece = board[y2][x2]
                        if target_piece == '.':
                            # then it is moving into an empty square
                            _moves.append((move(board, y, x, y2, x2),
                                           position_multipler * (POSITION_VALUE[y2][x2] - POSITION_VALUE[y][x])))
                        elif target_piece.islower() if _player_is_white else target_piece.isupper():
                            # then it is taking an opponent's piece
                            _moves.append((move(board, y, x, y2, x2),
                                           position_multipler * (2*POSITION_VALUE[y2][x2] - POSITION_VALUE[y][x]) -
                                           PIECE_VALUE[target_piece]))
                            break
                        else:
                            # then it is taking it's own piece
                            break
                        if piece in 'KkNn':
                            # don't reward moving the king towards the centre
                            # _moves[-1] = _moves[-1][0], PIECE_VALUE[target_piece]
                            break

            # pawns are weird
            if piece == 'P' if _player_is_white else piece == 'p':
                y2 = y+1 if _player_is_white else y-1
                # check if a take is possible
                for x2 in (x - 1, x + 1):
                    if 0 <= x2 <= 7:
                        target_piece = board[y2][x2]
                        if target_piece.islower() if _player_is_white else target_piece.isupper():
                            # then a take is possible
                            after_pawn_move = move(board, y, x, y2, x2)
                            if y2 == 7 if _player_is_white else y2 == 0:
                                # then the end of the board has been reached and promotion is needed
                                for replacement_piece in ('QRBN' if _player_is_white else 'qrbn'):
                                    after_pawn_replacement = after_pawn_move.copy()
                                    line = after_pawn_replacement[y2]
                                    after_pawn_replacement[y2] = line[:x2] + replacement_piece + line[x2 + 1:]
                                    _moves.append(
                                        (after_pawn_replacement, position_multipler *
                                         (2 * POSITION_VALUE[y2][x2] - POSITION_VALUE[y][x]) +
                                         PIECE_VALUE[replacement_piece] - PIECE_VALUE[target_piece] -
                                         PIECE_VALUE[piece]))
                            else:
                                _moves.append(
                                    (after_pawn_move, position_multipler *
                                     (2 * POSITION_VALUE[y2][x2] - POSITION_VALUE[y][x]) - PIECE_VALUE[target_piece]))
                # check if pawn can move forwards 1
                if board[y2][x] == '.':
                    # check if pawn can be promoted
                    if y2 == 7 if _player_is_white else y2 == 0:
                        after_pawn_move = move(board, y, x, y2, x)
                        # add each possible promotion to _moves
                        for replacement_piece in ('QRBN' if _player_is_white else 'qrbn'):
                            after_pawn_replacement = after_pawn_move.copy()
                            line = after_pawn_replacement[y2]
                            after_pawn_replacement[y2] = line[:x] + replacement_piece + line[x + 1:]
                            _moves.append((after_pawn_replacement,
                                           position_multipler * (POSITION_VALUE[y2][x] - POSITION_VALUE[y][x])))
                    else:
                        _moves.append((move(board, y, x, y2, x),
                                       position_multipler * (POSITION_VALUE[y2][x] - POSITION_VALUE[y][x])))
                    # check if pawn can move forwards 2
                    if y == 1 if _player_is_white else y == 6:
                        y2 = y + 2 if _player_is_white else y - 2
                        if board[y2][x] == '.':
                            _moves.append((move(board, y, x, y2, x),
                                           position_multipler * (POSITION_VALUE[y2][x] - POSITION_VALUE[y][x])))
    total_moves += len(_moves)
    return _moves


def simple_score(_board: [str])->float:
    """This takes a board and returns the current score of white"""
    _score = 0.0
    for row in _board:
        for piece in row:
            _score += PIECE_VALUE[piece]
    return _score


def alpha_beta(board, depth, score_diff, player_is_white, alpha, beta)->int:
    """Implements alpha beta scoring"""
    assert depth > 0
    possible_moves = moves(board, player_is_white)
    if not possible_moves:
        # this correctly scores stalemates
        return 0
    if depth == 1:
        return score_diff + (max if player_is_white else min)(m[1] for m in possible_moves)
    possible_moves.sort(key=lambda x: x[1], reverse=player_is_white)
    if player_is_white:
        v = -99999
        for possible_move, diff in possible_moves:
            v = max(v, alpha_beta(possible_move, depth - 1, score_diff+diff, False, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break  # beta cut off
    else:
        v = 99999
        for possible_move, diff in possible_moves:
            v = min(v, alpha_beta(possible_move, depth - 1, score_diff+diff, True, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break  # alpha cut off
    return v


def search(possible_moves, player_is_white, depth):
        alpha = -99999
        beta = 99999
        if player_is_white:
            for possible_move, diff in possible_moves:
                move_score = alpha_beta(possible_move, depth - 1, diff, False, alpha, beta)
                if move_score > alpha:
                    alpha = move_score
                    best_move = possible_move
        else:
            for possible_move, diff in possible_moves:
                move_score = alpha_beta(possible_move, depth - 1, diff, True, alpha, beta)
                if move_score < beta:
                    beta = move_score
                    best_move = possible_move
        return best_move


def main(history, white_time, black_time):
    start_time = now()
    history = [[''.join(row) for row in board] for board in history]
    player_is_white = len(history) % 2 == 1
    available_time = white_time if player_is_white else black_time
    score = simple_score(history[-1])
    possible_moves = moves(history[-1], player_is_white)
    if not possible_moves:
        raise StalemateException
    if (score < -10) if player_is_white else (score > 10):
        # if I am losing badly and in a loop then call a draw
        if len(history) > 9 and history[-1] == history[-5] == history[-9]:
            raise ThreeFoldRepetition
    else:
        # otherwise avoid repeated states
        repeat_free_moves = [m for m in possible_moves if m[0] not in history]
        if repeat_free_moves:
            # only remove repeats if there are still choices remaining
            possible_moves = repeat_free_moves
    possible_moves.sort(key=lambda x: x[1], reverse=player_is_white)
    best_move = None
    for depth in range(2, 10):
        search_start_time = now()
        best_move = search(possible_moves, player_is_white, depth)
        search_run_time = now() - search_start_time
        time_remaining = available_time - (now() - start_time)
        if time_remaining < search_run_time * 20:
            break
    print(depth)
    return [[piece for piece in line] for line in best_move]


'''
I use the time to calculate and score the first moves as a benchmark for my algorithm.
To get reliable figures wait for the CPU usage to fall below 10% before starting

buildTree   score           depth   time taken
----------------------------------------------------------------------
None        None            0       0.094 # everything other then search & scoring
False       fancy_score     4       5.969
False       simple_score    4       2.936
True        simple_score    4       3.687
True        simple_score    5       92.041
True        simple_score    3       0.328
after switching to runner calling main
True        simple_score    2       0.020
True        simple_score    3       0.132
True        simple_score    4       3.213
True        simple_score    5       80.615
after switching to incremental scoring (for efficiency)
True        incremental     3       0.060
after switching to using dicts for states (for ease of programming)
True        incremental     3       0.059
True        incremental     4       1.562
True        incremental     5       44.370
after adding POSITION_VALUE, PAWN_POSITION_VALUE and DISCOUNT_RATE
True        incremental     3       0.155
True        incremental     4       2.101
True        incremental     5       48.476
I chose to start using avg time to make moves in tournament play as my benchmark.
The interaction between players is important.
True        incremental     3       0.308
True        incremental     4       7.407
I decide that tournaments take too long so I pick the most difficult example in the tournament as my benchmark
True        incremental     3       0.330
True        incremental     4       14.933
First working attempt at alpha_beta scoring
False       incremental     3       0.050
False       incremental     4       0.932
False       incremental     5       3.411
Moving with alpha_beta now works
False       incremental     3       0.035
False       incremental     4       0.790
False       incremental     5       3.087
switched to benchmarking search function
False       incremental     3       0.035
False       incremental     4       0.698
False       incremental     5       2.558
'''

if __name__ == '__main__':
    difficultPosition = '''
r . b q . . . r
p p p p n k p p
. . n b . p . .
. . . . p . . .
. . P . N . . .
P . . P B N . .
. P . . P P P P
R . . Q K B . R'''
    test_board = [line for line in difficultPosition.replace(' ', '').split()]
    test_board.reverse()
    startTime = now()
    # main([test_board], 50, 0)

    _possible_moves = moves(test_board, True)
    _possible_moves.sort(key=lambda x: x[1], reverse=True)
    bestMove = search(_possible_moves, True, 2)
    print('{:.3f}'.format(now()-startTime))
    print(total_moves)
    print('\n'.join(' '.join(piece for piece in row) for row in bestMove.__reversed__()) + '\n')

