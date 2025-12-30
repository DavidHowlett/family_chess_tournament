from array import array
from time import perf_counter as now

import David_AI_v9 as ai

boards = {
    "initialPosition": """
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R""",
    "difficultPosition": """
r . b q . . . r
p p p p n k p p
. . n b . p . .
. . . . p . . .
. . P . N . . .
P . . P B N . .
. P . . P P P P
R . . Q K B . R""",
    "promotionPosition": """
r . . . . . . .
. P . P . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . p . p .
. . . . . . . R""",
    "pawnTakePosition1": """
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .""",
    "pawnTakePosition2": """
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .""",
    "kingSavePosition": """
r . . . . . . .
p . . . . . . .
P . . k p . . .
. . . . r . . .
. . . . Q . . .
. . . p . . P .
. . . . . . . P
. . . . K . N R""",
    "kingThreat": """
r . . . . . . .
p . . . . . . .
P . . . p . . .
. . . . k . . .
. . . . Q . . .
. . . p . . P .
. . . . . . . P
. . . . K . N R""",
    "castlingPosition": """
r . . . k . . r
p . . . . . . p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P . . . . . . P
R . . . K . . R""",
    "findCheckMate": """
. . . . . . k .
. . . R . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . p
. . . . . . . P
P . P . . P P .
. . . . . R K .""",
}

for key in boards:
    board = boards[key].replace(" ", "").split().__reversed__()
    board = array("u", "".join(row + "_" * 8 for row in board))
    assert len(board) == 128
    boards[key] = board
    # print(len(list(ai.moves(position, True))))
assert abs(ai.evaluate(boards["initialPosition"])) < 0.000001
assert len(list(ai.moves(boards["initialPosition"], True))) == 20
assert len(list(ai.moves(boards["difficultPosition"], True))) == 42
assert len(list(ai.moves(boards["pawnTakePosition1"], True))) == 2
assert len(list(ai.moves(boards["pawnTakePosition1"], False))) == 3
assert len(list(ai.moves(boards["pawnTakePosition2"], True))) == 3
assert len(list(ai.moves(boards["pawnTakePosition2"], False))) == 2
assert len(list(ai.moves(boards["castlingPosition"], True))) == 16
assert len(list(ai.moves(boards["castlingPosition"], False))) == 16
assert not ai.is_check(boards["kingSavePosition"], True)
assert not ai.is_check(boards["kingSavePosition"], False)
assert not ai.is_check(boards["kingThreat"], True)
assert ai.is_check(boards["kingThreat"], False)
assert ai.position_value["N"][3 + 4 * 16] == ai.position_value["N"][4 + 3 * 16]
assert ai.position_value["N"][3 + 4 * 16] == -ai.position_value["n"][3 + 4 * 16]
assert ai.position_value["P"][16] < ai.position_value["P"][5 * 16]
assert ai.position_value["p"][6 * 16] > ai.position_value["p"][2 * 16]
assert ai.position_value["P"][4 * 16] < ai.position_value["P"][4 + 4 * 16]
# the king can be taken in 5 ply
assert (
    ai.search(
        boards["findCheckMate"],
        4,
        ai.evaluate(boards["findCheckMate"]),
        True,
        -99999,
        99999,
    )[1]
    < 10000
)
assert (
    ai.search(
        boards["findCheckMate"],
        5,
        ai.evaluate(boards["findCheckMate"]),
        True,
        -99999,
        99999,
    )[1]
    > 10000
)


def performance_test():
    ai.transpositionTable = dict()
    ai.total_moves = 0
    _board = boards["difficultPosition"]
    test_start_time = now()
    for depth in range(1, 6):
        start_time = now()
        best_move, _ = ai.search(
            _board, depth, ai.evaluate(_board), True, -99999, 99999
        )
        print(
            "{}\t\t\t{}\t\t{:.3f}\t{}".format(
                ai.total_moves, depth, now() - start_time, len(ai.transpositionTable)
            )
        )
        # print('\n'.join(' '.join(piece for piece in row) for row in best_move.__reversed__()) + '\n')
    print(
        "{} moves made per second".format(
            int(ai.total_moves / (now() - test_start_time))
        )
    )


performance_test()
