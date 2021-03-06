import David_AI_v4 as v4
from time import perf_counter as now

initialPosition = '''
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R'''
initialPosition = initialPosition.replace(' ', '').split()
initialPosition.reverse()

difficultPosition = '''
r . b q . . . r
p p p p n k p p
. . n b . p . .
. . . . p . . .
. . P . N . . .
P . . P B N . .
. P . . P P P P
R . . Q K B . R'''
difficultPosition = difficultPosition.replace(' ', '').split()
difficultPosition.reverse()

promotionPosition = '''
r . . . . . . .
. P . P . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . p . p .
. . . . . . . R'''
promotionPosition = promotionPosition.replace(' ', '').split()
promotionPosition.reverse()

pawnTakePosition1 = '''
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .'''
pawnTakePosition1 = pawnTakePosition1.replace(' ', '').split()
pawnTakePosition1.reverse()

pawnTakePosition2 = '''
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .'''
pawnTakePosition2 = pawnTakePosition2.replace(' ', '').split()
pawnTakePosition2.reverse()

kingSavePosition = '''
r . . . . . . .
p . . . . . . .
P . . k p . . .
. . . . r . . .
. . . . Q . . .
. . . p . . P .
. . . . . . . P
. . . . K . N R'''
kingSavePosition = kingSavePosition.replace(' ', '').split()
kingSavePosition.reverse()

ps = v4.position_score
assert ps('R', 0, 0) == ps('R', 7, 7)
assert ps('R', 0, 0) == -ps('r', 7, 7)
assert ps('R', 1, 0) > ps('R', 0, 0)
assert ps('R', 0, 1) > ps('R', 0, 0)
assert ps('R', 4, 4) > ps('R', 0, 0)
assert ps('R', 3, 4) == ps('R', 4, 3)
assert ps('R', 3, 4) == -ps('r', 4, 3)
assert ps('P', 0, 0) < ps('P', 0, 7)
assert ps('P', 0, 0) < ps('P', 1, 0)
assert ps('p', 0, 0) == -ps('P', 0, 7)
assert ps('p', 0, 1) == -ps('P', 0, 6)
assert ps('p', 1, 1) == -ps('P', 1, 6)
assert ps('p', 0, 0) < ps('p', 0, 1)
assert ps('P', 3, 4) == -ps('p', 3, 3)
assert ps('P', 3, 4) == -ps('p', 3, 3)
assert ps('K', 3, 0) == -ps('k', 3, 7)
assert ps('K', 4, 0) == -ps('k', 4, 7)

assert abs(v4.board_score(initialPosition)) < 0.000001
assert len(list(v4.moves(initialPosition, True))) == 20
assert len(list(v4.moves(difficultPosition, True))) == 42
assert len(list(v4.moves(pawnTakePosition1, True))) == 2
assert len(list(v4.moves(pawnTakePosition1, False))) == 3
assert len(list(v4.moves(pawnTakePosition2, True))) == 3
assert len(list(v4.moves(pawnTakePosition2, False))) == 2
# print(list(v5.moves(pawnTakePosition1, True))[0])
# print(list(v5.moves(pawnTakePosition1, False))[0])
# print(list(v5.moves(pawnTakePosition2, True))[0])
# print(list(v5.moves(pawnTakePosition2, False))[0])


v4.alpha_beta(difficultPosition, 3, v4.board_score(difficultPosition), True, -99999, 99999)
v4.alpha_beta(promotionPosition, 3, v4.board_score(promotionPosition), True, -99999, 99999)

# todo fix this bad move
bestMove = v4.search(list(v4.moves(kingSavePosition, True)), 3, v4.board_score(kingSavePosition), True, -99999, 99999)


def performance_test():
    v4.total_moves = 0
    v4.transpositionTable = dict()
    global_depth = 5
    start_time = now()
    _possible_moves = list(v4.moves(difficultPosition, True))
    _possible_moves.sort(key=lambda x: x[1], reverse=True)
    best_move, _ = v4.search(_possible_moves, global_depth, v4.board_score(difficultPosition), True, -99999, 99999)
    print('{}\t\t\t{}\t\t{:.3f}'.format(v4.total_moves, global_depth, now()-start_time))
    print('\n'.join(' '.join(piece for piece in row) for row in best_move.__reversed__()) + '\n')

performance_test()

