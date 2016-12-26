from subprocess import call

playerA = 'David_AI.py'
playerB = 'David_AI.py'

open('game state.txt', 'w').write('''-------- turn: 0 --------

rnbqkbnr
pppppppp
........
........
........
........
PPPPPPPP
RNBQKBNR

to move: w
white time: 5.0
black time: 5.0

''')

for i in range(10):
    for player in [playerA, playerB]:
        call(["python3", player])
        with open('game state.txt', 'a') as gameState:
            gameState.write('white time: {:.6f}\n'.format(5.5))
            gameState.write('black time: {:.6f}\n'.format(5.5))
            gameState.write('\n')

