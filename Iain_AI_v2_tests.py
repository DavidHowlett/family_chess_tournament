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
x = list([[piece for piece in row.replace(' ', '')] for row in taken.split('\n')].__reversed__())

# print(x)
best_move, best_score = Iain_AI_v2.search(x, False, 3)
print(best_score, best_move)