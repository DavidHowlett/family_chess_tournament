import David_AI_v4 as v4

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

assert v4.simple_score(initialPosition) == 0
assert 0.000001 > v4.board_score(initialPosition) > -0.000001
assert len(v4.moves(initialPosition, True)) == 20
assert len(v4.moves(difficultPosition, True)) == 42

v4.alpha_beta(difficultPosition, 3, v4.board_score(difficultPosition), True, -99999, 99999)
v4.alpha_beta(promotionPosition, 3, v4.board_score(promotionPosition), True, -99999, 99999)



