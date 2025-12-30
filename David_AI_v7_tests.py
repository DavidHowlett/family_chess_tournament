from time import perf_counter as now

import David_AI_v7 as ai

initialPosition = """
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R"""
initialPosition = [
    line.split(" ") for line in initialPosition.split("\n") if len(line) > 5
]
initialPosition.reverse()

difficultPosition = """
r . b q . . . r
p p p p n k p p
. . n b . p . .
. . . . p . . .
. . P . N . . .
P . . P B N . .
. P . . P P P P
R . . Q K B . R"""
difficultPosition = [
    line.split(" ") for line in difficultPosition.split("\n") if len(line) > 5
]
difficultPosition.reverse()

promotionPosition = """
r . . . . . . .
. P . P . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . p . p .
. . . . . . . R"""
promotionPosition = [
    line.split(" ") for line in promotionPosition.split("\n") if len(line) > 5
]
promotionPosition.reverse()

promotionPosition2 = """
. r . . . . k r
. p p . . p p p
p . P . . . . .
. . . . . N . .
. . n . p . . .
. . . . P . . .
P . P . . P P P
. R . . . . K R"""
promotionPosition2 = [
    line.split(" ") for line in promotionPosition2.split("\n") if len(line) > 5
]
promotionPosition2.reverse()

pawnTakePosition1 = """
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . ."""
pawnTakePosition1 = [
    line.split(" ") for line in pawnTakePosition1.split("\n") if len(line) > 5
]
pawnTakePosition1.reverse()

pawnTakePosition2 = """
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . ."""
pawnTakePosition2 = [
    line.split(" ") for line in pawnTakePosition2.split("\n") if len(line) > 5
]
pawnTakePosition2.reverse()

kingSavePosition = """
r . . . . . . .
p . . . . . . .
P . . k p . . .
. . . . r . . .
. . . . Q . . .
. . . p . . P .
. . . . . . . P
. . . . K . N R"""
kingSavePosition = [
    line.split(" ") for line in kingSavePosition.split("\n") if len(line) > 5
]
kingSavePosition.reverse()


# for position in (initialPosition, difficultPosition, promotionPosition, promotionPosition2, pawnTakePosition1,
#                 pawnTakePosition2, kingSavePosition):
#    print(len(list(ai.moves(position, True))))

assert len(initialPosition) == 8
assert len(initialPosition[0]) == 8
assert abs(ai.evaluate(initialPosition)) < 0.000001
assert len(list(ai.moves(initialPosition, True))) == 20
assert len(list(ai.moves(difficultPosition, True))) == 42
assert len(list(ai.moves(pawnTakePosition1, True))) == 2
assert len(list(ai.moves(pawnTakePosition1, False))) == 3
assert len(list(ai.moves(pawnTakePosition2, True))) == 3
assert len(list(ai.moves(pawnTakePosition2, False))) == 2


def performance_test():
    ai.total_moves = 0
    board = difficultPosition
    test_start_time = now()
    for depth in range(1, 3):
        start_time = now()
        _possible_moves = list(ai.moves(board, True))
        _possible_moves.sort(key=lambda x: x[1], reverse=True)
        best_move, _ = ai.search(
            _possible_moves, depth, ai.evaluate(board), True, -99999, 99999
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


ai.transpositionTable = dict()
performance_test()
