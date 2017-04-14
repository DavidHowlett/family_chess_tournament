import David_AI_v8 as ai
from array import array
from time import perf_counter as now

boards = {'initialPosition': '''
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R''',
'difficultPosition': '''
r . b q . . . r
p p p p n k p p
. . n b . p . .
. . . . p . . .
. . P . N . . .
P . . P B N . .
. P . . P P P P
R . . Q K B . R''',
'promotionPosition': '''
r . . . . . . .
. P . P . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . p . p .
. . . . . . . R''',
'pawnTakePosition1': '''
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .''',
'pawnTakePosition2': '''
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . p . . . .
. . . . P . . .
. . . . . . . .''',
'kingSavePosition':'''
r . . . . . . .
p . . . . . . .
P . . k p . . .
. . . . r . . .
. . . . Q . . .
. . . p . . P .
. . . . . . . P
. . . . K . N R'''}

for key in boards:
    board = boards[key].replace(' ', '').replace('\n', '')
    board = array('u', board)
    board.reverse()
    assert len(board) == 64
    board.append(chr(0))
    boards[key] = board
    # print(len(list(ai.moves(position, True))))

assert abs(ai.evaluate(boards['initialPosition'])) < 0.000001
assert len(list(ai.moves(boards['initialPosition'], True))) == 20
assert len(list(ai.moves(boards['difficultPosition'], True))) == 42
assert len(list(ai.moves(boards['pawnTakePosition1'], True))) == 2
assert len(list(ai.moves(boards['pawnTakePosition1'], False))) == 3
assert len(list(ai.moves(boards['pawnTakePosition2'], True))) == 3
assert len(list(ai.moves(boards['pawnTakePosition2'], False))) == 2

assert ai.POSITION_VALUE['R'][0] < ai.POSITION_VALUE['R'][63]
assert ai.POSITION_VALUE['N'][3+4*8] == ai.POSITION_VALUE['N'][4+3*8]
assert ai.POSITION_VALUE['N'][3+4*8] == -ai.POSITION_VALUE['n'][3+4*8]
assert ai.POSITION_VALUE['P'][8] < ai.POSITION_VALUE['P'][8*5]
assert ai.POSITION_VALUE['p'][8*6] > ai.POSITION_VALUE['p'][8*2]
assert ai.POSITION_VALUE['P'][8*4] < ai.POSITION_VALUE['P'][4+8*4]


def performance_test():
    ai.total_moves = 0
    board = boards['difficultPosition']
    test_start_time = now()
    for depth in range(1, 6):
        start_time = now()
        best_move, _ = ai.search(board, depth, ai.evaluate(board), True, -99999, 99999)
        print('{}\t\t\t{}\t\t{:.3f}\t{}'.format(ai.total_moves, depth, now() - start_time, len(ai.transpositionTable)))
        # print('\n'.join(' '.join(piece for piece in row) for row in best_move.__reversed__()) + '\n')
    print('{} moves made per second'.format(int(ai.total_moves/(now()-test_start_time))))


ai.transpositionTable = dict()
performance_test()

