import Iain_AI_v2
import time
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
. . . n . . . .
. . . . P . . .
P P P P . P P P
R . B Q K B N R'''
difficultPosition = '''r . b q . . . r
p p p p n k p p
. . n b . p . .
. . . . p . . .
. . P . N . . .
P . . P B N . .
. P . . P P P P
R . . Q K B . R'''
x = list([[piece for piece in row.replace(' ', '')] for row in difficultPosition.split('\n')].__reversed__())

# print(x)
for depth in range(1, 4):
    start_time = time.perf_counter()
    best_move, best_score = Iain_AI_v2.search(x, False, depth)
    end_time = time.perf_counter()
    print(depth, best_score,end_time - start_time, best_move)

''' performance before optimisation
1 80 0.00220390942092681
2 -205 0.09845219473448505
3 25 3.126428370698206
'''