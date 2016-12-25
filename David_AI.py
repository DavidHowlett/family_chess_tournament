"""This was written by David for fun on 24th December 2016
Micheal is not allowed to read this file."""
import time
startTime = time.perf_counter()
value = {
    '.': 0,
    'K': 1000, 'Q': 9, 'R': 5, 'B': 3.2, 'N': 3, 'P': 1,
    'k': -1000, 'q': -9, 'r': -5, 'b': -3.2, 'n': -3, 'p': -1}


def score(board:[str])->float:
    'This takes a gameState object and returns the current score of white'
    _score = 0.0
    for row in board:
        for square in row:
            _score += value[square]
    return _score

# --------- read in game state ----------
gameHistory = open('game state.txt').read().split('\n')
turn = int(gameHistory[-13].split(' ')[2])
player = gameHistory[-12][9]
whiteTime = float(gameHistory[-11][12:])
blackTime = float(gameHistory[-10][12:])
if player == 'w':
    myTime = whiteTime + 2
    theirTime = blackTime
else:
    myTime = blackTime + 2
    theirTime = whiteTime
gameState = gameHistory[-9:-1]
gameState.reverse()

# ---------- modify game state ----------

# ---------- write game state -----------
runTime = time.perf_counter() - startTime
toWrite = '\n-------- turn: {} --------\n'.format(turn+1)
toWrite += 'to move: {}\n'.format('b' if player == 'w' else 'w')
toWrite += 'white time: {:.6f}\n'.format(myTime-runTime if player == 'w' else theirTime)
toWrite += 'black time: {:.6f}\n'.format(myTime-runTime if player == 'b' else theirTime)
toWrite += '\n'.join(gameState.__reversed__())+'\n'
open('game state.txt','a').write(toWrite)
print(toWrite)
print('score: {:.3f}'.format(score(gameState)))
print('run time: {:.5f}'.format(runTime))


