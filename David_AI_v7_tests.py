import David_AI_v7 as ai
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

'''
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
'''

assert abs(ai.evaluate(initialPosition)) < 0.000001
assert len(list(ai.moves(initialPosition, True))) == 20
assert len(list(ai.moves(difficultPosition, True))) == 42
assert len(list(ai.moves(pawnTakePosition1, True))) == 2
assert len(list(ai.moves(pawnTakePosition1, False))) == 3
assert len(list(ai.moves(pawnTakePosition2, True))) == 3
assert len(list(ai.moves(pawnTakePosition2, False))) == 2


def performance_test():
    ai.total_moves = 0
    test_start_time = now()
    for depth in range(2, 6):
        start_time = now()
        _possible_moves = list(ai.moves(difficultPosition, True))
        _possible_moves.sort(key=lambda x: x[1], reverse=True)
        best_move, _ = ai.search(_possible_moves, depth, ai.evaluate(difficultPosition), True, -99999, 99999)
        print('{}\t\t\t{}\t\t{:.3f}'.format(ai.total_moves, depth, now() - start_time))
        # print('\n'.join(' '.join(piece for piece in row) for row in best_move.__reversed__()) + '\n')
    print('{} leaves searched per second'.format(int(ai.total_moves/(now()-test_start_time))))


ai.transpositionTable = dict()
performance_test()

