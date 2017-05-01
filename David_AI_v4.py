"""This chess engine was written by David for fun. A board is represented by a [str] representing a 2D board.

Not implemented yet:
    - castling
    - en passant
    - aspiration search
    - bonus in eval function for having lots of possible moves

"""
from time import perf_counter as now
from shared import ThreeFoldRepetition

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

# for most pieces there is a small advantage to being in the centre
POSITION_VALUE = [[0.02 * (3 + x - x * x / 7) * (1 + y - y * y / 7) for x in range(8)] for y in range(8)]
#  print('\n'.join(' '.join('{:.2f}'.format(POSITION_VALUE[y][x])for x in range(8))for y in range(8))+'\n')
# pawns are more valuable in the centre but more importantly they become much more valuable when they are close to being
# turned into queens
# calculating the below formula takes 861 ns but lookup in a 2D table only takes 73 ns.
# This is the reason for pre-calculation
PAWN_POSITION_VALUE = [[0.1*(x - (x * x / 7))+(0.003 * y**4)-0.5 for x in range(8)] for y in range(8)]
#  print('\n'.join(' '.join('{:.2f}'.format(PAWN_POSITION_VALUE[y][x])for x in range(8))for y in range(8))+'\n')
transpositionTable = dict()
total_moves = 0
time_out_point = now() + 20


def position_score(piece, x, y) -> float:
    if piece in '.kK':
        return 0
    if piece == 'P':
        return PAWN_POSITION_VALUE[y][x]
    if piece == 'p':
        return -PAWN_POSITION_VALUE[7-y][x]
    if piece.isupper():
        return POSITION_VALUE[y][x]
    return -POSITION_VALUE[y][x]


def board_score(_board: [str])->float:
    """This takes a board and returns the current score of white"""
    _score = 0.0
    for y in range(8):
        for x in range(8):
            piece = _board[y][x]
            _score += PIECE_VALUE[piece]
            _score += position_score(piece, x, y)
    return _score


def move(board: [str], y1, x1, y2, x2)-> [str]:
    global total_moves
    """returns a board with a move made"""
    board = board.copy()
    # add piece to destination
    line = board[y2]
    board[y2] = line[:x2] + board[y1][x1] + line[x2 + 1:]
    # remove piece from source
    line = board[y1]
    board[y1] = line[:x1] + '.' + line[x1 + 1:]
    total_moves += 1
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
                                position_score(piece, x2, y2) -
                                position_score(piece, x, y))
                        elif target_piece.islower() if _player_is_white else target_piece.isupper():
                            # then it is taking an opponent's piece
                            yield (
                                move(board, y, x, y2, x2),
                                position_score(piece, x2, y2) -
                                position_score(target_piece, x2, y2) -
                                position_score(piece, x, y) -
                                PIECE_VALUE[target_piece])
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
                                    yield(
                                        after_pawn_replacement,
                                        PIECE_VALUE[replacement_piece] -
                                        PIECE_VALUE[target_piece] -
                                        PIECE_VALUE[piece] +
                                        position_score(replacement_piece, x2, y2) -
                                        position_score(target_piece, x2, y2) -
                                        position_score(piece, x, y))
                            else:
                                yield(
                                    after_pawn_move,
                                    position_score(piece, x2, y2) -
                                    position_score(target_piece, x2, y2) -
                                    position_score(piece, x, y) -
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
                                position_score(replacement_piece, x, y2) -
                                position_score(piece, x, y))
                    else:
                        yield(
                            move(board, y, x, y2, x),
                            position_score(piece, x, y2) -
                            position_score(piece, x, y))
                    # check if pawn can move forwards 2
                    if y == 1 if _player_is_white else y == 6:
                        y2 = y + 2 if _player_is_white else y - 2
                        if board[y2][x] == '.':
                            yield(
                                move(board, y, x, y2, x),
                                position_score(piece, x, y2) -
                                position_score(piece, x, y))


def estimated_score(board, previous_score, diff, player_is_white):
    key = ''.join(board) + 'w' if player_is_white else 'b'
    if key in transpositionTable:
        return transpositionTable[key][0]
    else:
        return previous_score + diff


def alpha_beta(board, depth, current_score, player_is_white, alpha, beta)->float:
    """Implements alpha beta tree search, returns a score. This fails soft."""
    # assert abs(current_score - board_score(board)) < 0.001
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
            key=lambda _move: estimated_score(_move[0], current_score, _move[1], player_is_white),
            reverse=player_is_white)
    if not possible_moves:
        # this correctly scores stalemates
        # it only works on lists, not generators
        return 0
    current_best_score = (-99999) if player_is_white else 99999
    for possible_move, diff in possible_moves:
        move_score = current_score + diff
        # assert abs(move_score - board_score(possible_move)) < 0.001
        if depth == 1:
            # to save on time I don't recurse for the last move
            child_key = ''.join(possible_move) + 'w'
            if child_key not in transpositionTable:
                transpositionTable[child_key] = move_score, 'exact', 0
        elif abs(diff) < 100:
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


def search(possible_moves, depth, current_score, player_is_white, alpha, beta):
    """Implements alpha_beta tree search, returns a best move"""
    assert depth > 0
    possible_moves.sort(
        key=lambda _move: estimated_score(_move[0], current_score, _move[1], player_is_white),
        reverse=player_is_white)
    for possible_move, diff in possible_moves:
        # assert abs(current_score + diff - board_score(possible_move)) < 0.001
        if depth == 1:
            move_score = current_score + diff
        else:
            move_score = alpha_beta(possible_move, depth - 1, current_score + diff, not player_is_white, alpha, beta)
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
    current_score = board_score(history[-1])
    possible_moves = list(moves(history[-1], player_is_white))
    if (current_score < -11) if player_is_white else (current_score > 11):
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
    # 5 second depth search can take 13.149 seconds in worst case seen so far :-(
    for depth in range(1, 6):
        search_start_time = now()
        try:
            best_move, best_score = search(possible_moves, depth, current_score, player_is_white, alpha, beta)
        except TimeoutError:
            print('internal timeout')
            break
        search_run_time = now() - search_start_time
        time_remaining = available_time - (now() - start_time)
        if time_remaining < search_run_time * 20:
            break
        if abs(best_score) > 100:
            # print('victory is expected')
            break
    print(depth)
    return [[piece for piece in line] for line in best_move]


'''
switched to benchmarking search function
incremental     3       0.035
incremental     4       0.698
incremental     5       2.558
Start of AI_v4
partial rewrite of alpha_beta
writing to transposition table implemented
move count      depth   time taken
8079            3       0.035
155591          4       0.843
681810          5       3.424
exact matches in transposition table used
645796          5       3.443
fail high and fail low from transposition table used
570439          5       2.443
transposition table used for move ordering
transposition table write on every move generation
552651          5       3.197
fixed bugs in move scoring
327016          5       2.299
fixed another bug in move scoring
292592			5		1.949
removed bonus for king moving towards centre
294017			5		1.974
made moves() a generator
214728			5		1.387
472960			6		3.377
added timeout check & fixed bug in timing function
5696			3		0.040
11654			4		0.094
214728			5		1.412
472954			6		3.177
at this point David_AI_v4 now wins 15/16 games against all other AI,
losing only one to David_AI_v1
added iterative deepening to timing function
42			    1		0.001
225			    2		0.002
5696			3		0.036
11654			4		0.112
214728			5		1.324
471805			6		3.090
stopped search when king taken
42			    1		0.000
225			    2		0.002
5696			3		0.042
10942			4		0.071
213600			5		1.357
427801			6		2.842
At this point David_AI_v4 wins 16/16 games
'''
