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

PIECE_VALUE = {
    '.': 0,
    'K': 20, 'Q': 9, 'R': 5, 'B': 3.2, 'N': 3, 'P': 1,
    'k': -20, 'q': -9, 'r': -5, 'b': -3.2, 'n': -3, 'p': -1}
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
                            _moves.append((move(board, y, x, y2, x2), 0))
                        elif target_piece.islower() if _player_is_white else target_piece.isupper():
                            # then it is taking an opponent's piece
                            _moves.append((move(board, y, x, y2, x2), -PIECE_VALUE[target_piece]))
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
                                    _moves.append((after_pawn_replacement,
                                                  PIECE_VALUE[replacement_piece] - PIECE_VALUE[target_piece] - 1))
                            else:
                                _moves.append((after_pawn_move, -PIECE_VALUE[target_piece]))
                # check if pawn can move forwards 1
                if board[y2][x] == '.':
                    # check if pawn can move forwards 2
                    if y == 1 if _player_is_white else y == 6:
                        _moves.append((move(board, y, x, y2, x), 0))
                        y2 = y + 2 if _player_is_white else y - 2
                        if board[y2][x] == '.':
                            _moves.append((move(board, y, x, y2, x), 0))
                    # check if pawn can be promoted
                    elif y2 == 7 if _player_is_white else y2 == 0:
                        after_pawn_move = move(board, y, x, y2, x)
                        # add each possible promotion to move list
                        for replacement_piece in ('QRBN' if _player_is_white else 'qrbn'):
                            after_pawn_replacement = after_pawn_move.copy()
                            line = after_pawn_replacement[y2]
                            after_pawn_replacement[y2] = line[:x] + replacement_piece + line[x + 1:]
                            _moves.append((after_pawn_replacement,
                                          PIECE_VALUE[replacement_piece] - 1))  # assume pawn value of 1
                    else:
                        _moves.append((move(board, y, x, y2, x), 0))
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
    global leafCount
    children = []
    child_is_white = not state[1]
    child_move_no = state[3]+1
    depth -= 1
    if depth:
        for board, score_diff in moves(state[0], state[1]):
            child = [board, child_is_white, None, child_move_no, state, None, score_diff]
            calculate_tree(child, depth)
            children.append(child)
    else:
        for board, score_diff in moves(state[0], state[1]):
            leafCount += 1
            child = [board, child_is_white, None, child_move_no, state, None, score_diff]
            children.append(child)
    # set the children of the current state to be the newly generated list
    state[5] = children
    if children:
        if depth:
            # then set the score to be the (score diff + score) of the best child
            state[2] = (max if state[1] else min)(child[6]+child[2] for child in children)
        else:
            # then set the score to be the score diff of the best child
            state[2] = (max if state[1] else min)(child[6] for child in children)
    else:
        # if there are no valid moves then it is a stalemate (StalemateException)
        state[2] = 0
    return state


def main(history, white_time, black_time):
    global leafCount
    leafCount = 0
    history = [[''.join(row) for row in board] for board in history]
    player_is_white = len(history) % 2 == 1
    initial_score = simple_score(history[-1])
    my_simple_score = initial_score if player_is_white else -initial_score
    # the type of "state": List[List[str], player_is_white, score, move_number, parent, children]
    initial_state = [history[-1], player_is_white, initial_score, 0, None, None]
    calculate_tree(initial_state, global_depth)
    possible_moves = initial_state[5]
    if not possible_moves:
        raise StalemateException
    if my_simple_score < -0.5:
        # if I am losing and in a loop then call a draw
        if len(history) > 9 and history[-1] == history[-5] == history[-9]:
            raise ThreeFoldRepetition
    else:
        # If I am drawing or winning then avoid previous game states
        for state in possible_moves:
            if state[0] in history:
                state[2] = -3 if player_is_white else 3

    # add further exploration of the promising parts of the tree here

    final_state = (max if player_is_white else min)(possible_moves, key=lambda s: s[2])
    final_board = final_state[0]
    print(leafCount)
    return [[piece for piece in line] for line in final_board]

# below are the settings for the algorithm
global_depth = 3
# score = fancy_score
leafCount = 0

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
after switching to runner calling main:
True        simple_score    2       0.020
True        simple_score    3       0.132
True        simple_score    4       3.213
True        simple_score    5       80.615

'''
