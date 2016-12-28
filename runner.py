import time
import os
import subprocess

initialTime = 5
timePerMove = 1

white = {'time remaining': initialTime, 'AI': 'David_AI.py'}
black = {'time remaining': initialTime, 'AI': 'David_AI_old.py'}

if os.name == 'posix':
    python = 'python3'
else:
    python = 'python'
print(os.name)

open('game state.txt', 'w').write(
    '''-------- turn: 0 --------

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

'''.format(initialTime, initialTime))

for i in range(100):
    player = black if i % 2 else white
    startTime = time.perf_counter()
    if subprocess.run((python, player['AI'])).returncode:
        print('{} stopped the game'.format(player['AI']))
        exit()
    runTime = time.perf_counter() - startTime
    player['time remaining'] = player['time remaining'] + timePerMove - runTime
    board = open('game state.txt').read().split('\n\n\n')[-1].split('\n\n')[-1]
    print(board)
    print('run time: {:.3f} seconds\n'.format(runTime))
    with open('game state.txt', 'a') as gameState:
        gameState.write('\n\nto move: {}\n'.format('w' if i % 2 else 'b'))
        gameState.write('white time: {:.6f}\n'.format(white['time remaining']))
        gameState.write('black time: {:.6f}\n'.format(black['time remaining']))
        gameState.write('\n')
        if 'k' not in board:
            gameState.write('White won!\n')
            print('White won in {} moves'.format(i+1))
            exit()
        if 'K' not in board:
            gameState.write('Black won!\n')
            print('Black won in {} moves'.format(i+1))
            exit()
print('Draw due to running out of time')

