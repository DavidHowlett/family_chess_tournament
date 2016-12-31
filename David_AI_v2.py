"""This was written by David for fun on 24th - 27th December 2016
Micheal and Robert not allowed to read this file until the competition is over.
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

"""
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
'''The further into the future a take is, the less certain it is to be a good idea
The discount rate combines with the very high value of the king to value king takes
earlier strongly over piece takes later'''
DISCOUNT_RATE = 0.95  # a point in 5 turns is worth 0.95**5 of a point now

assert PIECE_VALUE['K'] > DISCOUNT_RATE*PIECE_VALUE['Q'] + DISCOUNT_RATE**2*PIECE_VALUE['K']
# for most pieces there is a small advantage to being in the centre
POSITION_VALUE = [[0.04 * (1 + x - x * x / 7) * (1 + y - y * y / 7) for x in range(8)] for y in range(8)]
# pawns are more valuable in the centre but more importantly they become much more valuable when they are close to being
# turned into queens
# calculating the below formula takes 861 ns but lookup in a 2D table only takes 73 ns.
# This is the reason for pre-calculation
PAWN_POSITION_VALUE = [[0.003 * (10 + x - x * x / 6.9) * (y+2) ** 2 for x in range(8)] for y in range(8)]


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

    return _moves


def simple_score(_board: [str])->float:
    """This takes a board and returns the current score of white"""
    _score = 0.0
    for row in _board:
        for piece in row:
            _score += PIECE_VALUE[piece]
    return _score


def calculate_tree(state, depth):
    """recursively calculates children of the given state """
    children = []
    child_is_white = not state['white']
    depth -= 1
    if depth:
        for board, score_diff in moves(state['board'], state['white']):
            child = {'board': board, 'white': child_is_white, 'diff': score_diff}
            calculate_tree(child, depth)
            children.append(child)
    else:
        for board, score_diff in moves(state['board'], state['white']):
            child = {'board': board, 'white': child_is_white, 'diff': score_diff}  # ToDo optimise this line
            children.append(child)
    # set the children of the current state to be the newly generated list
    state['children'] = children
    if children:
        if depth:
            # then set the score to be the (score diff + score) of the best child (discounted for being in the future)
            state['score'] = DISCOUNT_RATE * (
                max if state['white'] else min)(child['diff']+child['score'] for child in children)
        else:
            # then set the score to be the score diff of the best child (discounted for being in the future)
            state['score'] = DISCOUNT_RATE * (
                max if state['white'] else min)(child['diff'] for child in children)
    else:
        # if there are no valid moves then it is a stalemate (StalemateException)
        state['score'] = 0
    return state


def main(history, white_time, black_time):
    history = [[''.join(row) for row in board] for board in history]
    player_is_white = len(history) % 2 == 1
    initial_score = simple_score(history[-1])
    my_simple_score = initial_score if player_is_white else -initial_score
    # the type of "state": List[List[str], player_is_white, score, move_number, parent, children]
    initial_state = {'board': history[-1], 'white': player_is_white}
    calculate_tree(initial_state, global_depth)
    possible_moves = initial_state['children']
    if not possible_moves:
        raise StalemateException
    if my_simple_score < -0.5:
        # if I am losing and in a loop then call a draw
        if len(history) > 9 and history[-1] == history[-5] == history[-9]:
            raise ThreeFoldRepetition
    else:
        # If I am drawing or winning then avoid previous game states
        for state in possible_moves:
            if state['board'] in history:
                state['score'] = -3 if player_is_white else 3

    # add further exploration of the promising parts of the tree here

    if global_depth > 1:
        final_state = (max if player_is_white else min)(possible_moves, key=lambda s: s['diff'] + s['score'])
    elif global_depth == 1:
        final_state = (max if player_is_white else min)(possible_moves, key=lambda s: s['diff'])
    return [[piece for piece in line] for line in final_state['board']]

global_depth = 3

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
True        NA              3       0.060
after switching to using dicts for states (for ease of programming)
True        NA              3       0.059
True        NA              4       1.562
True        NA              5       44.370
after adding POSITION_VALUE, PAWN_POSITION_VALUE and DISCOUNT_RATE
True        NA              3       0.155
True        NA              4       2.101
True        NA              5       48.476

'''
