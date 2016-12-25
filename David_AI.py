"""This was written by David for fun on 24th - 25th December 2016
Micheal is not allowed to read this file."""
import time
startTime = time.perf_counter()
value = {
    '.': 0,
    'K': 20, 'Q': 9, 'R': 5, 'B': 3.2, 'N': 3, 'P': 1,
    'k': -20, 'q': -9, 'r': -5, 'b': -3.2, 'n': -3, 'p': -1}


def score(board: [str])->float:
    """This takes a gameState object and returns the current score of white"""
    _score = 0.0
    for row in board:
        for square in row:
            _score += value[square]
    return _score


def move(board: [str], y1, x1, y2, x2)-> [str]:
    """returns a board with a move made"""
    assert 0 <= x1 <= 8
    assert 0 <= x2 <= 8
    assert 0 <= y1 <= 8
    assert 0 <= y2 <= 8
    board = board.copy()
    # add piece to destination
    line = board[y2]
    board[y2] = line[:x2] + board[y1][x1] + line[x2 + 1:]
    # remove piece from source
    line = board[y1]
    board[y1] = line[:x1] + '.' + line[x1 + 1:]
    return board


def moves(board: [str], _player: str)->[[str]]:
    """This generates a list of all possible game states after one move"""
    possibleMoves = []
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece == 'P':
                possibleMoves.append(move(board, x, y, 0, 1))
    return possibleMoves

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
gameState = move(gameState, 1, 0, 2, 0)
gameState = move(gameState, 7, 6, 5, 5)
# ---------- write game state -----------
runTime = time.perf_counter() - startTime
toWrite = '\n-------- turn: {} --------\n'.format(turn+1)
toWrite += 'to move: {}\n'.format('b' if player == 'w' else 'w')
toWrite += 'white time: {:.6f}\n'.format(myTime-runTime if player == 'w' else theirTime)
toWrite += 'black time: {:.6f}\n'.format(myTime-runTime if player == 'b' else theirTime)
toWrite += '\n'.join(gameState.__reversed__())+'\n'
open('new game state.txt','a').write(toWrite)
print(toWrite)
print('score: {:.3f}'.format(score(gameState)))
print('run time: {:.6f}'.format(runTime))


