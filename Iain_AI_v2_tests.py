import Iain_AI_v2
initialPosition = '''r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R'''
taken = '''r . . . . b . r
. . . . p k p p
. . q . . n . .
. . . . . . . .
. . . R P P . P
. . B Q . . . .
. . K . B . . .
. . . . . . . .'''
x = list([[piece for piece in row.replace(' ', '')] for row in initialPosition.split('\n')].__reversed__())

# print(x)
for depth in range(1, 4):
    best_move, best_score = Iain_AI_v2.search(x, True, depth)
    print(best_score, best_move)