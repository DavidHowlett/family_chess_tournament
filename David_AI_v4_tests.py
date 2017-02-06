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


assert len(David_AI_v4.moves(initialPosition, True)) == 20
assert len(David_AI_v4.moves(difficultPosition, True)) == 42
assert David_AI_v4.simple_score(initialPosition) == 0
assert David_AI_v4.positional_score(initialPosition) == 0
