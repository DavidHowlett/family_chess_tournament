"""This chess engine was written by David for fun. 
A board is represented by 128 char array

ToDo:
    - score moves towards enemy king more highly
    - score repeated positions differently as they lead to draws
    - create isCheck function
    - use isCheck in castling
    - add strict legal move generation function (look for check and stalemate)
    - create isStalemate function
    - make runner end the game when there is checkmate
    - make runner end the game when there are no legal moves (stalemate)
    - en passant
    - switch to negamax
    - aspiration search
"""
from time import perf_counter as now
from copy import copy
from array import array
from itertools import count
from shared import ThreeFoldRepetition

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
    'K': 20000, 'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'P': 100,
    'k': -20000, 'q': -900, 'r': -500, 'b': -330, 'n': -320, 'p': -100
}
POSITION_VALUE_READABLE = {
    'P': [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]],
    # [[5*(x - (x * x / 7))+(0.02 * (y+2)**4)-10 for x in range(8)] for y in range(7, -1, -1)],
    # print('\n'.join(' '.join('{}'.format(int(PAWN_POSITION_VALUE[y][x]))
    #   for x in range(8))for y in range(8))+'\n')
    'N': [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]],
    'B': [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]],
    'R': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]],
    'Q': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]],
    # this should change with the game's phase
    'K_early': [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]],
    'K_late': [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]],
    '.': [[0 for _ in range(8)] for _ in range(8)]
}
# The last 4 chars of the board contain the castling rights.
# If the char is true then castling is allowed
BOTTOM_LEFT_CASTLING = 124
BOTTOM_RIGHT_CASTLING = 125
TOP_LEFT_CASTLING = 126
TOP_RIGHT_CASTLING = 127
# valid positions
valid_pos = [x+16*y for x in range(8) for y in range(8)]
assert len(valid_pos) == 64
transpositionTable = dict()
total_moves = 0
time_out_point = now() + 100
history = []
position_value = None


def evaluate(board)->float:
    return sum(position_value[board[x + 16 * y]][x + 16 * y] for x in range(8) for y in range(8))


def recalculate_position_values(board):
    global position_value
    position_value = dict()
    # total_material is 48190 at the games start and can go as low as 40000 at the games end
    total_material = sum(abs(PIECE_VALUE[board[x+16*y]]) for x in range(8) for y in range(8))
    # game_phase should be 1 when the score is 48190 and should hit 0 when the score is 40600
    game_phase = (total_material-40600)/7590
    game_phase = max(game_phase, 0)
    POSITION_VALUE_READABLE['K'] = [[
        game_phase * POSITION_VALUE_READABLE['K_early'][y][x] +
        (1-game_phase) * POSITION_VALUE_READABLE['K_late'][y][x]
        for x in range(8)] for y in range(8)]
    for piece_ in POSITION_VALUE_READABLE:
        if piece_.startswith('K_'):
            # then it is not an actual piece
            continue
        position_value[piece_] = []
        position_value[piece_.lower()] = []
        for row in POSITION_VALUE_READABLE[piece_].__reversed__():
            position_value[piece_].extend(
                [PIECE_VALUE[piece_]+value for value in row]+[None]*8)
        for row in POSITION_VALUE_READABLE[piece_]:
            position_value[piece_.lower()].extend(
                [-PIECE_VALUE[piece_]-value for value in row.__reversed__()]+[None]*8)


def move(board, pos1, pos2):
    global total_moves
    """returns a board with a move made"""
    total_moves += 1
    board = copy(board)
    # add piece to destination
    board[pos2] = board[pos1]
    # remove piece from source
    board[pos1] = '.'

    # most moves don't affect castling rights so I do a fast set membership test
    if pos1 in {0, 4, 7,
                0+7*16, 4+7*16, 7+7*16}:
        if pos1 == 0:
            board[BOTTOM_LEFT_CASTLING] = '\0'
        elif pos1 == 4:
            board[BOTTOM_LEFT_CASTLING] = board[BOTTOM_RIGHT_CASTLING] = '\0'
        elif pos1 == 7:
            board[BOTTOM_RIGHT_CASTLING] = '\0'
        elif pos1 == 0+7*16:
            board[TOP_LEFT_CASTLING] = '\0'
        elif pos1 == 4+7*16:
            board[TOP_LEFT_CASTLING] = board[TOP_RIGHT_CASTLING] = '\0'
        elif pos1 == 7+7*16:
            board[TOP_RIGHT_CASTLING] = '\0'
    return board


def moves(board, _player_is_white: bool):
    """This generates a list of all possible game states after one move.
    It does not check for whether the king is in check."""
    for pos1 in valid_pos:
        piece = board[pos1]
        if piece in 'KQRBN' if _player_is_white else piece in 'kqrbn':
            for direction in PIECE_MOVE_DIRECTION[piece]:
                for pos2 in count(pos1+direction, direction):
                    if pos2 & 0x88:
                        # then it is a move off the board
                        break
                    target_piece = board[pos2]
                    if target_piece == '.':
                        # then it is moving into an empty square
                        yield (
                            move(board, pos1, pos2),
                            position_value[piece][pos2] -
                            position_value[piece][pos1])
                    elif target_piece.islower() if _player_is_white else target_piece.isupper():
                        # then it is taking an opponent's piece
                        yield (
                            move(board, pos1, pos2),
                            position_value[piece][pos2] -
                            position_value[target_piece][pos2] -
                            position_value[piece][pos1])
                        break
                    else:
                        # then it is taking it's own piece
                        break
                    if piece in 'KkNn':
                        break
        # pawns are weird
        if piece == 'P' if _player_is_white else piece == 'p':
            # this section is for captures
            for pos2 in (pos1+1+16, pos1-1+16) if _player_is_white else (pos1+1-16, pos1-1-16):
                if pos2 & 0x88:
                    continue
                target_piece = board[pos2]
                if target_piece.islower() if _player_is_white else target_piece.isupper():
                    # then a take is possible
                    after_pawn_move = move(board, pos1, pos2)
                    if pos2 >= (7*16) if _player_is_white else pos2 < 8:
                        # then the end of the board has been reached and promotion is needed
                        for replacement_piece in ('QRBN' if _player_is_white else 'qrbn'):
                            after_pawn_replacement = copy(after_pawn_move)
                            after_pawn_replacement[pos2] = replacement_piece
                            yield(
                                after_pawn_replacement,
                                position_value[replacement_piece][pos2] -
                                position_value[target_piece][pos2] -
                                position_value[piece][pos1])
                    else:
                        yield(
                            after_pawn_move,
                            position_value[piece][pos2] -
                            position_value[target_piece][pos2] -
                            position_value[piece][pos1])

            # Check if pawn can move forwards 1
            # Note that there is no need to check for moving off the edge of the board
            # due to pawns on the back row always being promoted.
            pos2 = pos1 + (16 if _player_is_white else -16)
            if board[pos2] == '.':
                # check if pawn can be promoted
                if pos2 >= (7*16) if _player_is_white else pos2 < 8:
                    after_pawn_move = move(board, pos1, pos2)
                    # add each possible promotion to _moves
                    for replacement_piece in ('QRBN' if _player_is_white else 'qrbn'):
                        after_pawn_replacement = copy(after_pawn_move)
                        after_pawn_replacement[pos2] = replacement_piece
                        yield(
                            after_pawn_replacement,
                            position_value[replacement_piece][pos2] -
                            position_value[piece][pos1])
                else:
                    yield(
                        move(board, pos1, pos2),
                        position_value[piece][pos2] -
                        position_value[piece][pos1])
                # check if pawn can move forwards 2
                if pos1 < 32 if _player_is_white else pos1 >= 6*16 :
                    pos2 = pos1 + (32 if _player_is_white else -32)
                    if board[pos2] == '.':
                        yield(
                            move(board, pos1, pos2),
                            position_value[piece][pos2] -
                            position_value[piece][pos1])
    # TODO this should check if the king is moving into, out of or through check
    if _player_is_white:
        if (board[BOTTOM_LEFT_CASTLING] and
                board[0] == 'R' and
                board[1] == '.' and
                board[2] == '.' and
                board[3] == '.' and
                board[4] == 'K'):
            yield castle(board, 0, 4, 3, 2)
        if (board[BOTTOM_RIGHT_CASTLING] and
                board[7] == 'R' and
                board[6] == '.' and
                board[5] == '.' and
                board[4] == 'K'):
            yield castle(board, 7, 4, 5, 6)
    else:
        if (board[TOP_LEFT_CASTLING] and
                board[0+7*16] == 'r' and
                board[1+7*16] == '.' and
                board[2+7*16] == '.' and
                board[3+7*16] == '.' and
                board[4+7*16] == 'k'):
            yield castle(board, 0+7*16, 4+7*16, 3+7*16, 2+7*16)
        if (board[TOP_RIGHT_CASTLING] and
                board[7+7*16] == 'r' and
                board[6+7*16] == '.' and
                board[5+7*16] == '.' and
                board[4+7*16] == 'k'):
            yield castle(board, 7+7*16, 4+7*16, 5+7*16, 6+7*16)


def castle(board, old_rook_location, old_king_location, new_rook_location, new_king_location):
    board = copy(board)
    board[new_rook_location] = rook = board[old_rook_location]
    board[new_king_location] = king = board[old_king_location]
    board[old_rook_location] = board[old_king_location] = '.'
    if old_king_location == 4:
        board[BOTTOM_LEFT_CASTLING] = board[BOTTOM_RIGHT_CASTLING] = '\0'
    else:
        board[TOP_LEFT_CASTLING] = board[TOP_RIGHT_CASTLING] = '\0'
    return (
        board,
        position_value[rook][new_rook_location] +
        position_value[king][new_king_location] -
        position_value[rook][old_rook_location] -
        position_value[king][old_king_location])


def alpha_beta(board, depth, current_cscore, player_is_white, alpha, beta)->int:
    """Implements alpha beta tree search, returns a score. This fails soft."""
    # if abs(current_cscore - evaluate(board)) > 0.1:
    #    print(current_cscore, evaluate(board), board)
    # assert len(board) == 128
    # lookup the current node to see if it has already been searched
    key = board.tobytes() + (b'w' if player_is_white else b'b')
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
        possible_moves.sort(key=lambda _move: _move[1], reverse=player_is_white)
    current_best_score = (-99999) if player_is_white else 99999
    for possible_move, diff in possible_moves:
        move_score = current_cscore + diff
        # assert abs(move_score - evaluate(possible_move)) < 0.001
        # Only search deeper if both kings are still present.
        # This also stops my engine trading my king now for your king later.
        # I also search deeper then normal if a take is made
        # Note that the comparison is ordered for evaluation speed
        if depth >= 1 and (depth >= 2 or abs(diff) > 0.5) and abs(diff) < 1000:
            # this does not always use move ordering :-( todo
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


def estimated_score(board, previous_cscore, diff, player_is_white):
    key = board.tobytes() + (b'w' if player_is_white else b'b')
    if key in transpositionTable:
        return transpositionTable[key][0]
    else:
        return previous_cscore + diff


def search(board, depth, current_cscore, player_is_white, alpha, beta):
    """Implements top level node in alpha_beta tree search, returns a best move"""
    # assert depth > 0
    possible_moves = list(moves(board, player_is_white))
    possible_moves.sort(
        key=lambda _move: estimated_score(_move[0], current_cscore, _move[1], player_is_white),
        reverse=player_is_white)
    for possible_move, diff in possible_moves:
        if depth == 1:
            move_score = current_cscore + diff
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


def to_array(given_history: [[str]] or [[[str]]]) -> array or [array]:
    """Converts boards from a list of lists to arrays"""
    # shortcut the method if only given a single board
    if type(given_history[0][0]) == str:
        return array('u', ''.join(''.join(row)+'_'*8 for row in given_history))
    assert len(given_history[0]) == 8
    assert len(given_history[0][0]) == 8
    _history = []
    # at the beginning of a game all castling options are possible
    castling_rights = array('u', '____')
    # incrementally update the castling rights
    for given_board in given_history:
        board = array('u', ''.join(''.join(row)+'_'*8 for row in given_board))
        if board[0] != 'R':
            castling_rights[0] = '\0'
        if board[4] != 'K':
            castling_rights[0] = castling_rights[1] = '\0'
        if board[7] != 'R':
            castling_rights[1] = '\0'
        if board[0+7*16] != 'r':
            castling_rights[2] = '\0'
        if board[4+7*16] != 'k':
            castling_rights[2] = castling_rights[3] = '\0'
        if board[7+7*16] != 'r':
            castling_rights[3] = '\0'
        board[-4:] = castling_rights
        _history.append(board)
    return _history


def from_array(given_history: array or [array]) -> [[str]] or [[[str]]]:
    """Converts boards from arrays to lists of lists"""
    if type(given_history) == array:
        array_board = given_history
        list_of_lists = [[array_board[x + 16 * y] for x in range(8)] for y in range(8)]
        assert type(list_of_lists) == list
        assert type(list_of_lists[0]) == list
        return list_of_lists
    _history = [[[
        array_board[x + 16 * y] for x in range(8)] for y in range(8)]
        for array_board in given_history]
    assert type(_history) == list
    assert type(_history[0]) == list
    assert type(_history[0][0]) == list
    return _history


def main(given_history, white_time, black_time):
    global transpositionTable
    global time_out_point
    global history
    start_time = now()
    history = to_array(given_history)
    current_board = history[-1]
    assert len(current_board) == 128
    assert type(history[-1]) == type(current_board)
    if len(history) < 3:
        transpositionTable = dict()
    player_is_white = len(history) % 2 == 1
    available_time = white_time if player_is_white else black_time
    time_out_point = start_time + available_time - 0.5  # always hold 0.5 seconds in reserve
    recalculate_position_values(current_board)
    current_score = evaluate(current_board)
    best_move = None
    alpha = -99999
    beta = 99999
    for depth in range(1, 99):
        search_start_time = now()
        try:
            best_move, best_score = search(current_board, depth, current_score, player_is_white, alpha, beta)
            # the transposition table write is inside the try: to ensure it is only written when the search completes
            transpositionTable[current_board.tobytes()] = best_score, 'exact', depth
        except TimeoutError:
            print('internal timeout')
            break
        search_run_time = now() - search_start_time
        # print(f'{depth}  {search_run_time:.3f}')
        time_remaining = available_time - (now() - start_time)
        if time_remaining < search_run_time * 40:
            break
        if abs(best_score) > 10000:
            # print('check mate is expected')
            break
    print(f'search depth: {depth}-{depth+1}')
    print(f'expected score: {best_score:.1f}')
    # if I am losing badly and in a loop then call a draw
    if (((best_score < -400) if player_is_white else (best_score > 400)) and
            len(history) > 9 and history[-1] == history[-5] == history[-9]):
        raise ThreeFoldRepetition
    assert len(best_move) == 128
    return from_array(best_move)


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
changed pawn lookup table and switched to testing on PC
131			2		0.001
4057			3		0.029
18982			4		0.108
126569			5		0.776
138422 leaves searched per second
added quiescence search to depth 2
878			2		0.008
45827			3		0.336
197728			4		1.433
1102823			5		6.893
127180 leaves searched per second
ditched fancy move sorting
878			2		0.008
44478			3		0.332
190035			4		1.300
1032192			5		6.660
124355 leaves searched per second
removed all traces of evaluate
878			2		0.008
45726			3		0.312
194771			4		1.297
1094450			5		6.508
134704 leaves searched per second
quiescence search to depth 1
210			2		0.002
8224			3		0.068
58484			4		0.354
311780			5		2.244
116886 leaves searched per second
switched back to mac
210			2		0.003
8224			3		0.056
58484			4		0.311
311780			5		2.356
114390 leaves searched per second
reordered comparison
210			2		0.002
8224			3		0.087
58484			4		0.218
311780			5		1.363
186732 leaves searched per second
switched back to using lists of lists
210			2		0.002	65
8224			3		0.059	1977
58484			4		0.226	3889
311780			5		1.751	59593
152995 leaves searched per second
changed way moves are counted
42			1		0.001	0
252			2		0.004	65
8266			3		0.073	1977
58526			4		0.203	3889
311822			5		1.746	59593
153933 moves made per second
switched to using arrays
42			1		0.000	0
262			2		0.002	64
8585			3		0.075	2018
18977			4		0.156	2981
251061			5		1.476	56693
146883 moves made per second
removed PIECE_VALUE
42			1		0.000	0
262			2		0.001	64
8585			3		0.054	2018
18977			4		0.052	2981
251061			5		1.378	56693
169003 moves made per second
added tracking of castling rights
42			1		0.000	0
262			2		0.002	64
8585			3		0.055	2018
18977			4		0.076	2981
251061			5		1.666	56693
139514 moves made per second
make tracking of castling rights more efficient
42			1		0.001	0
262			2		0.004	64
8585			3		0.067	2018
18977			4		0.062	2981
251061			5		1.507	56693
153069 moves made per second
switched to unoptimised 0x88 representation
42			1		0.000	0
262			2		0.001	64
8589			3		0.052	2022
18984			4		0.082	2986
252137			5		1.962	57081
120205 moves made per second
optimised 0x88 move generation
42			1		0.000	0
262			2		0.001	64
8589			3		0.043	2018
18986			4		0.057	2981
251283			5		1.316	56691
177237 moves made per second
implemented castling & changed move generation order
42			1		0.000	0
252			2		0.001	65
8353			3		0.060	1989
59137			4		0.179	3921
315452			5		1.253	60681
211089 moves made per second
changed piece square tables
'''
