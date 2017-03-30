"""This chess engine was written by David for fun. A board is represented by a [str] representing a 2D board.

ToDo:
    - look one move further into the future if the last move is a take
    - bonus / penalty to evaluation for tempo to better enable variable depth search
    - castling
    - en passant
    - aspiration search
    - 
note that the cscore only includes parts of the score that are cumulatively evaluated
score is the result of the evaluation function
"""
from time import perf_counter as now
import copy
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
    'K': 20000, 'Q': 975, 'R': 500, 'B': 335, 'N': 325, 'P': 100,
    'k': -20000, 'q': -975, 'r': -500, 'b': -335, 'n': -325, 'p': -100
}

POSITION_VALUE_READABLE = {
    'P': [[5*(x - (x * x / 7))+(0.02 * (y+2)**4)-10 for x in range(8)] for y in range(7, -1, -1)],
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
POSITION_VALUE = dict()
for piece_ in POSITION_VALUE_READABLE:
    tmp = copy.deepcopy(POSITION_VALUE_READABLE[piece_])
    POSITION_VALUE[piece_.lower()] = [[-value for value in row] for row in tmp]
    tmp.reverse()
    POSITION_VALUE[piece_] = tmp
transpositionTable = dict()
total_leaves = 0
time_out_point = now() + 100


def get_cscore(_board: [str])->float:
    """This takes a board and returns the material and position score of white"""
    _score = 0.0
    for y in range(8):
        for x in range(8):
            piece = _board[y][x]
            _score += PIECE_VALUE[piece]
            _score += POSITION_VALUE[piece][y][x]
    return _score


def extra_terms(board: [str]):
    global total_leaves
    """Returns extra terms in evaluation function, speed appears to be more important though"""
    total_leaves += 1
    return 0
    added_score = 0
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece == '.':
                continue
            white = piece.isupper()
            # pawns are weird
            if piece in 'Pp':
                y2 = y + 1 if white else y - 1
                # check if a take is possible
                for x2 in (x - 1, x + 1):
                    if 0 <= x2 <= 7:
                        target_piece = board[y2][x2]
                        if target_piece.islower() if white else target_piece.isupper():
                            # then a take is possible
                            if y2 == 7 if white else y2 == 0:
                                added_score += 400 if white else -400
                            else:
                                added_score += 20 if white else -20
                # check if pawn can move forwards 1
                if board[y2][x] == '.':
                    # check if pawn can be promoted
                    if y2 == 7 if white else y2 == 0:
                        added_score += 300 if white else -300
                    else:
                        added_score += 10 if white else -10
                        # check if pawn can move forwards 2
                    if y == 1 if white else y == 6:
                        y2 = y + 2 if white else y - 2
                        if board[y2][x] == '.':
                            added_score += 10 if white else -10
            else:
                for xd, yd in PIECE_MOVE_DIRECTION[piece]:
                    for i in range(1, 100):
                        x2 = x + i * xd
                        y2 = y + i * yd
                        if not (0 <= x2 <= 7 and 0 <= y2 <= 7):
                            # then it is a move off the board
                            break
                        target_piece = board[y2][x2]
                        if target_piece == '.':
                            # then it is moving into an empty square
                            added_score += 5 if white else -5
                        elif target_piece.islower() if white else target_piece.isupper():
                            # then it is attacking
                            added_score += 5 if white else -5
                            break
                        else:
                            # then it is defending it's own piece
                            added_score += 5 if white else -5
                            break
                        if piece in 'KkNn':
                            break
    return added_score


def evaluate(_board: [str])->float:
    return get_cscore(_board) + extra_terms(_board)


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


def moves(board: [str], _player_is_white: bool):
    global total_moves
    """This generates a list of all possible game states after one move.
    Preferred moves should be later in the returned list."""
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
                            yield (
                                move(board, y, x, y2, x2),
                                POSITION_VALUE[piece][y2][x2] -
                                POSITION_VALUE[piece][y][x])
                        elif target_piece.islower() if _player_is_white else target_piece.isupper():
                            # then it is taking an opponent's piece
                            yield (
                                move(board, y, x, y2, x2),
                                POSITION_VALUE[piece][y2][x2] -
                                POSITION_VALUE[target_piece][y2][x2] -
                                POSITION_VALUE[piece][y][x] -
                                PIECE_VALUE[target_piece])
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
                                    yield(
                                        after_pawn_replacement,
                                        PIECE_VALUE[replacement_piece] -
                                        PIECE_VALUE[target_piece] -
                                        PIECE_VALUE[piece] +
                                        POSITION_VALUE[replacement_piece][y2][x2] -
                                        POSITION_VALUE[target_piece][y2][x2] -
                                        POSITION_VALUE[piece][y][x])
                            else:
                                yield(
                                    after_pawn_move,
                                    POSITION_VALUE[piece][y2][x2] -
                                    POSITION_VALUE[target_piece][y2][x2] -
                                    POSITION_VALUE[piece][y][x] -
                                    PIECE_VALUE[target_piece])
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
                            yield(
                                after_pawn_replacement,
                                PIECE_VALUE[replacement_piece] -
                                PIECE_VALUE[piece] +
                                POSITION_VALUE[replacement_piece][y2][x] -
                                POSITION_VALUE[piece][y][x])
                    else:
                        yield(
                            move(board, y, x, y2, x),
                            POSITION_VALUE[piece][y2][x] -
                            POSITION_VALUE[piece][y][x])
                    # check if pawn can move forwards 2
                    if y == 1 if _player_is_white else y == 6:
                        y2 = y + 2 if _player_is_white else y - 2
                        if board[y2][x] == '.':
                            yield(
                                move(board, y, x, y2, x),
                                POSITION_VALUE[piece][y2][x] -
                                POSITION_VALUE[piece][y][x])


def estimated_score(board, previous_cscore, diff, player_is_white):
    key = ''.join(board) + 'w' if player_is_white else 'b'
    if key in transpositionTable:
        return transpositionTable[key][0]
    else:
        return previous_cscore + diff + extra_terms(board)


def alpha_beta(board, depth, current_cscore, player_is_white, alpha, beta)->int:
    """Implements alpha beta tree search, returns a score. This fails soft."""
    # assert abs(current_cscore - board_score(board)) < 0.001
    # lookup the current node to see if it has already been searched
    key = ''.join(board) + ('w' if player_is_white else 'b')
    if key in transpositionTable:
        node_score, node_type, node_search_depth = transpositionTable[key]
        if node_search_depth >= depth:
            if (node_type == 'exact' or
                    node_type == 'high' and node_score >= beta or
                    node_type == 'low' and node_score <= alpha):
                return node_score

    possible_moves = moves(board, player_is_white)
    if depth > 1:
        if now() > time_out_point:
            raise TimeoutError
        # then try to guess the best order to try moves
        possible_moves = list(possible_moves)
        possible_moves.sort(
            key=lambda _move: estimated_score(_move[0], current_cscore, _move[1], player_is_white),
            reverse=player_is_white)
    if not possible_moves:
        # this correctly scores stalemates
        # it only works on lists, not generators
        return 0
    current_best_score = (-99999) if player_is_white else 99999
    for possible_move, diff in possible_moves:
        move_score = current_cscore + diff + extra_terms(possible_move)
        # assert abs(move_score - evaluate(possible_move)) < 0.001
        if depth > 1 and abs(diff) < 10000:
            # then the kings are both still present so it is worth searching further.
            # this if statement also stops my engine trading my king now for your king later
            move_score = alpha_beta(possible_move, depth - 1, move_score, not player_is_white, alpha, beta)
        if player_is_white:
            if move_score > current_best_score:
                current_best_score = move_score
                if move_score > alpha:
                    alpha = move_score
                    if alpha >= beta:
                        # the score failed high
                        transpositionTable[key] = current_best_score, 'high', depth
                        break
        else:
            if move_score < current_best_score:
                current_best_score = move_score
                if move_score < beta:
                    beta = move_score
                    if alpha >= beta:
                        # the score failed low
                        transpositionTable[key] = current_best_score, 'low', depth
                        break
    else:
        # the score is exact and the earlier check of the table ensures that we are not overwriting
        # an entry of greater depth
        transpositionTable[key] = current_best_score, 'exact', depth
    return current_best_score


def search(possible_moves, depth, current_cscore, player_is_white, alpha, beta):
    """Implements alpha_beta tree search, returns a best move"""
    # assert depth > 0
    possible_moves.sort(
        key=lambda _move: estimated_score(_move[0], current_cscore, _move[1], player_is_white),
        reverse=player_is_white)
    for possible_move, diff in possible_moves:
        if depth == 1:
            move_score = current_cscore + diff + extra_terms(possible_move)
            # assert abs(move_score - evaluate(possible_move)) < 0.001
        else:
            move_score = alpha_beta(possible_move, depth - 1, current_cscore + diff, not player_is_white, alpha, beta)
        if player_is_white:
            if move_score > alpha:
                alpha = move_score
                best_move = possible_move
        else:
            if move_score < beta:
                beta = move_score
                best_move = possible_move
    return best_move, alpha if player_is_white else beta


def main(history, white_time, black_time):
    global transpositionTable
    global time_out_point
    transpositionTable = dict()
    start_time = now()
    player_is_white = len(history) % 2 == 1
    available_time = white_time if player_is_white else black_time
    time_out_point = start_time + available_time - 0.5  # always hold 0.5 seconds in reserve
    history = [[''.join(row) for row in board] for board in history]
    current_score = evaluate(history[-1])
    current_cscore = get_cscore(history[-1])
    possible_moves = list(moves(history[-1], player_is_white))
    if not possible_moves:
        raise StalemateException
    if (current_score < -1100) if player_is_white else (current_score > 1100):
        # if I am losing badly and in a loop then call a draw
        if len(history) > 9 and history[-1] == history[-5] == history[-9]:
            raise ThreeFoldRepetition
    else:
        # otherwise avoid repeated states
        repeat_free_moves = [m for m in possible_moves if m[0] not in history]
        if repeat_free_moves:
            # only remove repeats if there are still choices remaining
            possible_moves = repeat_free_moves
    best_move = None
    alpha = -99999
    beta = 99999
    # 5 depth search can take 13.149 seconds in worst case seen so far :-(
    for depth in range(1, 10):
        search_start_time = now()
        try:
            best_move, best_score = search(possible_moves, depth, current_cscore, player_is_white, alpha, beta)
        except TimeoutError:
            print('internal timeout')
            break
        search_run_time = now() - search_start_time
        time_remaining = available_time - (now() - start_time)
        if time_remaining < search_run_time * 20:
            break
        if abs(best_score) > 10000:
            # print('check mate is expected')
            break
    print(depth)
    return [[piece for piece in line] for line in best_move]


'''
At this point David_AI_v4 wins 16/16 games
changed position scoring to make David_AI_v5
this also causes the search of more moves for the benchmark position
250			2		0.002
5160			3		0.046
18017			4		0.090
217693			5		1.385
737830			6		3.568
144904 moves searched per second
small boost from removing unnecessary code
250			2		0.002
5160			3		0.050
18017			4		0.138
217693			5		1.092
737965			6		2.868
177823 moves searched per second
added move counting
300			2		0.083
3508			3		0.483
12901			4		1.628
109606			5		13.375
396902			6		47.114
6331 moves searched per second
switched to centipawn evaluation & tweaked scoring
358			2		0.055
4777			3		0.612
21297			4		2.285
286896			5		36.687
7237 leaves searched per second
15/20 scored with the extra terms
18/20 with extra terms removed
24/26 after conversion to centipawns
23.5/26 with CPW piece square tables (add incentive to move pawns forwards)
166			2		0.002
4876			3		0.040
19911			4		0.097
287690			5		1.339
1105592			6		4.259
192741 leaves searched per second
simplified piece value lookup
159			2		0.002
5164			3		0.033
20096			4		0.086
160780			5		0.809
172953 leaves searched per second
removed function call for position value lookup
159			2		0.001
5164			3		0.024
20096			4		0.094
160780			5		0.669
204022 leaves searched per second :-)
'''