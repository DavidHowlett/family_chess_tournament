"""This was written by David for fun on 24th - 25th December 2016
Micheal is not allowed to read this file."""
import time
import itertools
startTime = time.perf_counter()
PIECE_VALUE = {
    '.': 0,
    'K': 20, 'Q': 9, 'R': 5, 'B': 3.2, 'N': 3, 'P': 1,
    'k': -20, 'q': -9, 'r': -5, 'b': -3.2, 'n': -3, 'p': -1}
PIECE_MOVE_DIRECTION = {
    'K': ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)),
    'k': ((1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)),
    'Q': ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)),
    'q': ((1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)),
    'R': ((1,0), (0,1), (-1,0), (0,-1)),
    'r': ((1,0), (0,1), (-1,0), (0,-1)),
    'B': ((1,1), (1,-1), (-1,1), (-1,-1)),
    'b': ((1,1), (1,-1), (-1,1), (-1,-1)),
    'N': ((1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)),
    'n': ((1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)),
}


def score(board: [str])->float:
    """This takes a gameState object and returns the current score of white"""
    _score = 0.0
    for row in board:
        for square in row:
            _score += PIECE_VALUE[square]
    return _score


def move(_board: [str], y1, x1, y2, x2)-> [str]:
    """returns a board with a move made"""
    _board = _board.copy()
    # add piece to destination
    line = _board[y2]
    _board[y2] = line[:x2] + _board[y1][x1] + line[x2 + 1:]
    # remove piece from source
    line = _board[y1]
    _board[y1] = line[:x1] + '.' + line[x1 + 1:]
    return _board


def moves(board: [str], _player: str)->[[str]]:
    """This generates a list of all possible game states after one move"""
    _moves = []
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece in 'KQRBN' and _player == 'w' or piece in 'kqrbn' and _player == 'b':
                for xd, yd in PIECE_MOVE_DIRECTION[piece]:
                    for i in range(1, 100):
                        x2 = x+i*xd
                        y2 = y+i*yd
                        if not (0 <= x2 <= 7 and 0 <= y2 <= 7):
                            # then it is a move off the board
                            break
                        target_piece = board[y2][x2]
                        if (target_piece.isupper() and _player == 'w') or (target_piece.islower() and _player == 'b'):
                            # then it is taking it's own piece
                            break
                        if (target_piece.isupper() and _player == 'b') or (target_piece.islower() and _player == 'w'):
                            # then it is taking an opponent's piece
                            _moves.append(move(board, y, x, y2, x2))
                            break
                        _moves.append(move(board, y, x, y2, x2))
                        if piece in 'KkNn':
                            break
            '''
            # pawns are weird
            if piece == 'P' and _player == 'w' or piece == 'p' and _player == 'b':
                y2 = y+1 if _player == 'w' else y-1

                for i in (1,2) if (y == 1 and _player == 'w' or y == 6 and player == 'b') else (1,):
                    y2 = y+i*yd
                    if not 0 <= y2 <= 7:
                        # then it is a move off the board
                        break
                    target_piece = board[y2][x2]
                    if (target_piece.isupper() and _player == 'w') or (target_piece.islower() and _player == 'b'):
                        # then it is taking it's own piece
                        break
                    if (target_piece.isupper() and _player == 'b') or (target_piece.islower() and _player == 'w'):
                        # then it is taking an opponent's piece
                        _moves.append(move(board, y, x, y2, x2))
                        break
                    _moves.append(move(board, y, x, y2, x2))
                    if piece in 'KkNn':
                        break
            '''
    return _moves

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
for board in moves(gameState,'w'):
    print('\n'.join(board.__reversed__())+'\n')

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


