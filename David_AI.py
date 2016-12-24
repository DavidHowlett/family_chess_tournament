import time
'''This was written by David for fun on 24th December 2016
Micheal is not allowed to read this file.
'''
startTime = time.perf_counter()

# --------- read in game state ----------
gameHistory = open('game state.txt').read().split('\n')
turn = int(gameHistory[-13].split(' ')[2])
player = gameHistory[-12][9]
whiteTime = float(gameHistory[-11][12:])
blackTime = float(gameHistory[-10][12:])
if player == 'w':
    myTime = whiteTime
    theirTime = blackTime
else:
    myTime = blackTime
    theirTime = whiteTime
gameState = gameHistory[-9:-1]
gameState.reverse()
gameState = [[char for char in line] for line in gameState]

# ---------- modify game state ----------

# ---------- write game state -----------
handle = open('game state.txt','a')
handle.write('\n-------- turn: {} --------\n'.format(turn+1))
handle.write('to move: {}\n'.format('b' if player == 'w' else 'w'))
moveDuration = time.perf_counter() - startTime
handle.write('white time: {}\n'.format(whiteTime+moveDuration if player == 'w' else whiteTime))
handle.write('black time: {}\n'.format(blackTime+moveDuration if player == 'b' else blackTime))
handle.write('\n'.join(''.join(char for char in line) for line in gameState.__reversed__())+'\n')


print(gameHistory)
print(turn)
print(player)
print(whiteTime)
print(blackTime)
print(gameState)


