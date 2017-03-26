initialPosition = '''r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R'''
x = [[piece for piece in row.replace(' ', '')] for row in initialPosition.split('\n')]

print(x)
