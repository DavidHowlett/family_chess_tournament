"""This chess engine was written by David for fun. A board is represented by a [str] representing a 2D board.

ToDo:
    - switch to negamax
    - change positional scoring according to the game's phase
    - discount future scores
    - castling
    - en passant
    - aspiration search
    -
note that the cscore only includes parts of the score that are cumulatively evaluated
score is the result of the evaluation function
"""

import copy
from time import perf_counter as now

from shared import ThreeFoldRepetition

PIECE_MOVE_DIRECTION = {
    "K": ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)),
    "k": ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
    "Q": ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)),
    "q": ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
    "R": ((1, 0), (0, 1), (-1, 0), (0, -1)),
    "r": ((1, 0), (0, 1), (-1, 0), (0, -1)),
    "B": ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    "b": ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    "N": ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)),
    "n": ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)),
}
PIECE_VALUE = {
    ".": 0,
    "K": 20000,
    "Q": 975,
    "R": 500,
    "B": 335,
    "N": 325,
    "P": 100,
    "k": -20000,
    "q": -975,
    "r": -500,
    "b": -335,
    "n": -325,
    "p": -100,
}

POSITION_VALUE_READABLE = {
    "P": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # [[5*(x - (x * x / 7))+(0.02 * (y+2)**4)-10 for x in range(8)] for y in range(7, -1, -1)],
    # print('\n'.join(' '.join('{}'.format(int(PAWN_POSITION_VALUE[y][x]))
    #   for x in range(8))for y in range(8))+'\n')
    "N": [
        [-8, -8, -8, -8, -8, -8, -8, -8],
        [-8, 0, 0, 0, 0, 0, 0, -8],
        [-8, 0, 4, 6, 6, 4, 0, -8],
        [-8, 0, 6, 8, 8, 6, 0, -8],
        [-8, 0, 6, 8, 8, 6, 0, -8],
        [-8, 0, 4, 6, 6, 4, 0, -8],
        [-8, 0, 1, 2, 2, 1, 0, -8],
        [-16, -12, -8, -8, -8, -8, -12, -16],
    ],
    "B": [
        [-4, -4, -4, -4, -4, -4, -4, -4],
        [-4, 0, 0, 0, 0, 0, 0, -4],
        [-4, 0, 2, 4, 4, 2, 0, -4],
        [-4, 0, 4, 6, 6, 4, 0, -4],
        [-4, 0, 4, 6, 6, 4, 0, -4],
        [-4, 1, 2, 4, 4, 2, 1, -4],
        [-4, 2, 1, 1, 1, 1, 2, -4],
        [-4, -4, -12, -4, -4, -12, -4, -4],
    ],
    "R": [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 2, 2, 0, 0, 0],
    ],
    "Q": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 2, 2, 1, 0, 0],
        [0, 0, 2, 3, 3, 2, 0, 0],
        [0, 0, 2, 3, 3, 2, 0, 0],
        [0, 0, 1, 2, 2, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [-5, -5, -5, -5, -5, -5, -5, -5],
    ],
    "K": [
        [-40, -30, -50, -70, -70, -50, -30, -40],
        [-30, -20, -40, -60, -60, -40, -20, -30],
        [-20, -10, -30, -50, -50, -30, -10, -20],
        [-10, 0, -20, -40, -40, -20, 0, -10],
        [0, 10, -10, -30, -30, -10, 10, 0],
        [10, 20, 0, -20, -20, 0, 20, 10],
        [30, 40, 20, 0, 0, 20, 40, 30],
        [40, 50, 30, 10, 10, 30, 50, 40],
    ],
    ".": [[0 for _ in range(8)] for _ in range(8)],
}
POSITION_VALUE = dict()
for piece_ in POSITION_VALUE_READABLE:
    tmp = copy.deepcopy(POSITION_VALUE_READABLE[piece_])
    POSITION_VALUE[piece_.lower()] = [[-value for value in row] for row in tmp]
    tmp.reverse()
    POSITION_VALUE[piece_] = tmp
transpositionTable = dict()
total_moves = 0
time_out_point = now() + 100


def evaluate(_board: [str]) -> float:
    _score = 0.0
    for y in range(8):
        for x in range(8):
            piece = _board[y][x]
            _score += PIECE_VALUE[piece]
            _score += POSITION_VALUE[piece][y][x]
    return _score


def piece_count(board):
    total = 0
    for row in board:
        for piece in row:
            if piece != ".":
                total += 1
    return total


def move(board: [str], y1, x1, y2, x2) -> [str]:
    global total_moves
    """returns a board with a move made"""
    total_moves += 1
    board = board.copy()
    # add piece to destination
    board[y2] = board[y2].copy()
    board[y2][x2] = board[y1][x1]
    # remove piece from source
    board[y1] = board[y1].copy()
    board[y1][x1] = "."
    return board


def moves(board: [str], _player_is_white: bool):
    """This generates a list of all possible game states after one move.
    Preferred moves should be later in the returned list."""
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece in "KQRBN" if _player_is_white else piece in "kqrbn":
                for xd, yd in PIECE_MOVE_DIRECTION[piece]:
                    for i in range(1, 100):
                        x2 = x + i * xd
                        y2 = y + i * yd
                        if not (0 <= x2 <= 7 and 0 <= y2 <= 7):
                            # then it is a move off the board
                            break
                        target_piece = board[y2][x2]
                        if target_piece == ".":
                            # then it is moving into an empty square
                            yield (
                                move(board, y, x, y2, x2),
                                POSITION_VALUE[piece][y2][x2]
                                - POSITION_VALUE[piece][y][x],
                            )
                        elif (
                            target_piece.islower()
                            if _player_is_white
                            else target_piece.isupper()
                        ):
                            # then it is taking an opponent's piece
                            yield (
                                move(board, y, x, y2, x2),
                                POSITION_VALUE[piece][y2][x2]
                                - POSITION_VALUE[target_piece][y2][x2]
                                - POSITION_VALUE[piece][y][x]
                                - PIECE_VALUE[target_piece],
                            )
                            break
                        else:
                            # then it is taking it's own piece
                            break
                        if piece in "KkNn":
                            break

            # pawns are weird
            if piece == "P" if _player_is_white else piece == "p":
                y2 = y + 1 if _player_is_white else y - 1
                # check if a take is possible
                for x2 in (x - 1, x + 1):
                    if 0 <= x2 <= 7:
                        target_piece = board[y2][x2]
                        if (
                            target_piece.islower()
                            if _player_is_white
                            else target_piece.isupper()
                        ):
                            # then a take is possible
                            after_pawn_move = move(board, y, x, y2, x2)
                            if y2 == 7 if _player_is_white else y2 == 0:
                                # then the end of the board has been reached and promotion is needed
                                for replacement_piece in (
                                    "QRBN" if _player_is_white else "qrbn"
                                ):
                                    after_pawn_replacement = after_pawn_move.copy()
                                    after_pawn_replacement[y2] = after_pawn_replacement[
                                        y2
                                    ].copy()
                                    after_pawn_replacement[y2][x2] = replacement_piece
                                    yield (
                                        after_pawn_replacement,
                                        PIECE_VALUE[replacement_piece]
                                        - PIECE_VALUE[target_piece]
                                        - PIECE_VALUE[piece]
                                        + POSITION_VALUE[replacement_piece][y2][x2]
                                        - POSITION_VALUE[target_piece][y2][x2]
                                        - POSITION_VALUE[piece][y][x],
                                    )
                            else:
                                yield (
                                    after_pawn_move,
                                    POSITION_VALUE[piece][y2][x2]
                                    - POSITION_VALUE[target_piece][y2][x2]
                                    - POSITION_VALUE[piece][y][x]
                                    - PIECE_VALUE[target_piece],
                                )
                # check if pawn can move forwards 1
                if board[y2][x] == ".":
                    # check if pawn can be promoted
                    if y2 == 7 if _player_is_white else y2 == 0:
                        after_pawn_move = move(board, y, x, y2, x)
                        # add each possible promotion to _moves
                        for replacement_piece in "QRBN" if _player_is_white else "qrbn":
                            after_pawn_replacement = after_pawn_move.copy()
                            after_pawn_replacement[y2] = after_pawn_replacement[
                                y2
                            ].copy()
                            after_pawn_replacement[y2][x] = replacement_piece
                            yield (
                                after_pawn_replacement,
                                PIECE_VALUE[replacement_piece]
                                - PIECE_VALUE[piece]
                                + POSITION_VALUE[replacement_piece][y2][x]
                                - POSITION_VALUE[piece][y][x],
                            )
                    else:
                        yield (
                            move(board, y, x, y2, x),
                            POSITION_VALUE[piece][y2][x] - POSITION_VALUE[piece][y][x],
                        )
                    # check if pawn can move forwards 2
                    if y == 1 if _player_is_white else y == 6:
                        y2 = y + 2 if _player_is_white else y - 2
                        if board[y2][x] == ".":
                            yield (
                                move(board, y, x, y2, x),
                                POSITION_VALUE[piece][y2][x]
                                - POSITION_VALUE[piece][y][x],
                            )


def alpha_beta(board, depth, current_cscore, player_is_white, alpha, beta) -> int:
    """Implements alpha beta tree search, returns a score. This fails soft."""
    # assert abs(current_cscore - evaluate(board)) < 0.001
    # lookup the current node to see if it has already been searched
    key = "".join(piece for row in board for piece in row) + (
        "w" if player_is_white else "b"
    )
    if key in transpositionTable:
        node_score, node_type, node_search_depth = transpositionTable[key]
        if node_search_depth >= depth:
            if (
                node_type == "exact"
                or node_type == "high"
                and node_score >= beta
                or node_type == "low"
                and node_score <= alpha
            ):
                return node_score

    possible_moves = moves(board, player_is_white)
    if depth > 1:
        if now() > time_out_point:
            raise TimeoutError
        # then try to guess the best order to try moves
        possible_moves = list(possible_moves)
        possible_moves.sort(key=lambda _move: _move[1], reverse=player_is_white)
    if not possible_moves:
        # this correctly scores stalemates
        # it only works on lists, not generators
        return 0
    current_best_score = (-99999) if player_is_white else 99999
    for possible_move, diff in possible_moves:
        move_score = current_cscore + diff
        # assert abs(move_score - evaluate(possible_move)) < 0.001
        # Only search deeper if both kings are still present.
        # This also stops my engine trading my king now for your king later.
        # I also search deeper then normal if a take is made
        # Note that the comparison is ordered for evaluation speed
        if depth >= 1 and (depth >= 2 or abs(diff) > 50) and abs(diff) < 1000:
            # this does not always use move ordering :-( todo
            move_score = alpha_beta(
                possible_move, depth - 1, move_score, not player_is_white, alpha, beta
            )
        if player_is_white:
            if move_score > current_best_score:
                current_best_score = move_score
                if move_score > alpha:
                    alpha = move_score
                    if alpha >= beta:
                        # the score failed high
                        transpositionTable[key] = current_best_score, "high", depth
                        break
        else:
            if move_score < current_best_score:
                current_best_score = move_score
                if move_score < beta:
                    beta = move_score
                    if alpha >= beta:
                        # the score failed low
                        transpositionTable[key] = current_best_score, "low", depth
                        break
    else:
        # the score is exact and the earlier check of the table ensures that we are not overwriting
        # an entry of greater depth
        transpositionTable[key] = current_best_score, "exact", depth
    assert key in transpositionTable
    return current_best_score


def estimated_score(board, previous_cscore, diff, player_is_white):
    key = "".join(piece for row in board for piece in row) + (
        "w" if player_is_white else "b"
    )
    if key in transpositionTable:
        return transpositionTable[key][0]
    else:
        return previous_cscore + diff


def search(possible_moves, depth, current_cscore, player_is_white, alpha, beta):
    """Implements top level node in alpha_beta tree search, returns a best move"""
    # assert depth > 0
    possible_moves.sort(
        key=lambda _move: estimated_score(
            _move[0], current_cscore, _move[1], player_is_white
        ),
        reverse=player_is_white,
    )
    for possible_move, diff in possible_moves:
        if depth == 1:
            move_score = current_cscore + diff
            # assert abs(move_score - evaluate(possible_move)) < 0.001
        else:
            move_score = alpha_beta(
                possible_move,
                depth - 1,
                current_cscore + diff,
                not player_is_white,
                alpha,
                beta,
            )
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
    time_out_point = (
        start_time + available_time - 0.5
    )  # always hold 0.5 seconds in reserve
    # history = [[''.join(row) for row in board] for board in history]
    current_score = evaluate(history[-1])
    possible_moves = list(moves(history[-1], player_is_white))
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
            best_move, best_score = search(
                possible_moves, depth, current_score, player_is_white, alpha, beta
            )
        except TimeoutError:
            print("internal timeout")
            break
        search_run_time = now() - search_start_time
        # print(f'{depth}  {search_run_time:.3f}')
        time_remaining = available_time - (now() - start_time)
        if time_remaining < search_run_time * 30:
            break
        if abs(best_score) > 10000:
            # print('check mate is expected')
            break
    print(f"search depth: {depth}-{depth + 1}")
    print(f"expected score: {best_score}")
    return best_move  # [[piece for piece in line] for line in best_move]


"""
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

"""
