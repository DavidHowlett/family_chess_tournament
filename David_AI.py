'''This was written by David for fun on 24th December 2016
Micheal is not allowed to read this file.
'''
import time
startTime = time.perf_counter()

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
gameState = [[char for char in line] for line in gameState]

# ---------- modify game state ----------

# ---------- write game state -----------
gameState = '\n'.join(''.join(char for char in line) for line in gameState.__reversed__())+'\n'
moveDuration = time.perf_counter() - startTime
toWrite = '\n-------- turn: {} --------\n'.format(turn+1)
toWrite += 'to move: {}\n'.format('b' if player == 'w' else 'w')
toWrite += 'white time: {}\n'.format(myTime-moveDuration if player == 'w' else theirTime)
toWrite += 'black time: {}\n'.format(myTime-moveDuration if player == 'b' else theirTime)
toWrite += gameState
open('game state.txt','a').write(toWrite)
print(toWrite)


