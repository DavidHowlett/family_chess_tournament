import time
import subprocess

initialTime = 5
timePerMove = 1

playerA = ['w', 5.0, ('python3', 'David_AI.py')]
playerB = ['b', 5.0, ('python3', 'Michael_AI_v1.0.py')]

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
white time: {}
black time: {}

'''.format(playerA[1], playerB[1]))

for i in range(100):
    for colour, timeRemaining, AI in [playerA, playerB]:
        startTime = time.perf_counter()
        subprocess.run(AI)
        runTime = time.perf_counter() - startTime
        if colour == 'w':
            playerA[1] = timeRemaining + timePerMove - runTime
        else:
            playerB[1] = timeRemaining + timePerMove - runTime
        with open('game state.txt', 'a') as gameState:
            gameState.write('\n\nto move: {}\n'.format('b' if colour == 'w' else 'w'))
            gameState.write('white time: {:.6f}\n'.format(playerA[1]))
            gameState.write('black time: {:.6f}\n'.format(playerB[1]))
            gameState.write('\n')
        print(open('game state.txt').read().split('\n\n\n')[-1])
        print('run time: {:.3f} seconds'.format(runTime))

