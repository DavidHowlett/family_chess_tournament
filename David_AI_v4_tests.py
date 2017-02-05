import David_AI_v4
import David_AI_v3

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


def test_move_count():
    assert len(David_AI_v4.moves(initialPosition, True)) == 20
    assert len(David_AI_v4.moves(difficultPosition, True)) == 42


def test_alpha_beta():
    for board in initialPosition, difficultPosition:
        for depth in range(1, 4):
            assert (David_AI_v3.alpha_beta(board, depth, 0, True, -99999, 99999) ==
                    David_AI_v4.alpha_beta(board, depth, 0, True, -99999, 99999))


def test_search():
    for board in initialPosition, difficultPosition:
        possible_moves = David_AI_v4.moves(board, True)
        for depth in range(2, 4):
            assert (David_AI_v3.search(possible_moves, True, depth) ==
                    David_AI_v4.search(possible_moves, 0, True, depth))
