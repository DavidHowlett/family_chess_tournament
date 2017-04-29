import Iain_AI_v2
initialPosition = '''r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R'''
stalemate = '''. . . . . k . r
p . p . . . p p
. . . b . . . .
. p . n . p . .
. . . . . P . .
. K . . . . . .
. . . . r . . .
. . . . . . . .'''
Knight_Fight = '''r . b q k b . r
p p p p p p p p
. . . . . N . .
. . . . . . . .
. . . . . . . .
. . . . P . . .
P P n P . P P P
R . B Q K B N R'''
x = list([[piece for piece in row.replace(' ', '')] for row in Knight_Fight.split('\n')].__reversed__())

# print(x)
for depth in range(1, 4):
    best_move, best_score = Iain_AI_v2.search(x, True, depth)
    print(depth, best_score, best_move)