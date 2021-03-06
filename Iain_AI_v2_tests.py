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
promotionPosition = '''r . r . . . . .
. P . P . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . p . p .
. . . . . R . R'''
x = list([[piece for piece in row.replace(' ', '')] for row in difficultPosition.split('\n')].__reversed__())
for move in Iain_AI_v2.moves(x, True):
    print(move)
print(len(Iain_AI_v2.moves(x, True)))
# print(x)
for depth in range(1, 5):
    start_time = time.perf_counter()
    best_move, best_score = Iain_AI_v2.search(x, True, depth)
    end_time = time.perf_counter()
    print(depth, best_score, end_time - start_time)  # , best_move)


''' performance before optimisation
1 80 0.00220390942092681
2 -205 0.09845219473448505
3 25 3.126428370698206
created move function
1 80 0.002263578584288147
2 -205 0.0991942096530591
3 25 3.123364391239797
differential scoring
1 80 0.0018940165566047572
2 -205 0.0803750820050783
3 25 2.580656265187982
moved score calculation
1 80 0.002009505371031876
2 -205 0.07904118619844507
3 25 2.540729857226953
removed deepcopy
1 80 0.00011613041895171445
2 -205 0.00410338173704801
3 25 0.14609174623899446
4 -125 5.050977404292655
Now searches single pawn advancements even when double advance is possible
1 310 0.00013698256600105544
2 5 0.00473279577567581
3 240 0.15794250261052842
4 5 5.883278342478872
'''