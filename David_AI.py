"""This was written by David for fun on 24th - 25th December 2016
Micheal is not allowed to read this file.

Not implemented yet:
    - castling
    - en passant

"""
import time
startTime = time.perf_counter()
PIECE_VALUE = {
    '.': 0,
    'K': 20, 'Q': 9, 'R': 5, 'B': 3.2, 'N': 3, 'P': 1,
    'k': -20, 'q': -9, 'r': -5, 'b': -3.2, 'n': -3, 'p': -1}
PIECE_MOVE_DIRECTION = {
    'K': ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)),
    'k': ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
    'Q': ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)),
    'q': ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
    'R': ((1, 0), (0, 1), (-1, 0), (0, -1)),
    'r': ((1, 0), (0, 1), (-1, 0), (0, -1)),
    'B': ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    'b': ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    'N': ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)),
    'n': ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)),
}


def move(board: [str], y1, x1, y2, x2)-> [str]:
    """returns a board with a move made"""
    board = board.copy()
    # add piece to destination
    line = board[y2]
    board[y2] = line[:x2] + board[y1][x1] + line[x2 + 1:]
    # remove piece from source
    line = board[y1]
    board[y1] = line[:x1] + '.' + line[x1 + 1:]
    return board


def moves(board: [str], _player_is_white: bool)->[[str]]:
    """This generates a list of all possible game states after one move"""
    _moves = []
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece in 'KQRBN' if _player_is_white else piece in 'kqrbn':
                for xd, yd in PIECE_MOVE_DIRECTION[piece]:
                    for i in range(1, 100):
                        x2 = x+i*xd
                        y2 = y+i*yd
                        if not (0 <= x2 <= 7 and 0 <= y2 <= 7):
                            # then it is a move off the board
                            break
                        target_piece = board[y2][x2]
                        if target_piece.isupper() if _player_is_white else target_piece.islower():
                            # then it is taking it's own piece
                            break
                        if target_piece.islower() if _player_is_white else target_piece.isupper():
                            # then it is taking an opponent's piece
                            _moves.append(move(board, y, x, y2, x2))
                            break
                        _moves.append(move(board, y, x, y2, x2))
                        if piece in 'KkNn':
                            break

            # pawns are weird
            if piece == 'P' if _player_is_white else piece == 'p':
                pawn_moves = []
                y2 = y+1 if _player_is_white else y-1
                for x2 in (x - 1, x + 1):
                    if 0 <= x2 <= 7:
                        if board[y2][x2].islower() if _player_is_white else board[y2][x2].isupper():
                            # then a take is possible
                            pawn_moves.append((y2, x2))
                # move forward by 1
                if board[y2][x] == '.':
                    # then the move is into an empty square
                    pawn_moves.append((y2, x))
                    # move forward by 2
                    if y == 1 if _player_is_white else y == 6:
                        y2 = y + 2 if _player_is_white else y - 2
                        if board[y2][x] == '.':
                            pawn_moves.append((y2, x))
                for y2, x2 in pawn_moves:
                    after_pawn_move = move(board, y, x, y2, x2)
                    if y2 == 7 if _player_is_white else y2 == 0:
                        # then the end of the board has been reached and promotion is needed
                        for replacement_piece in ('QRBN' if _player_is_white else 'qrbn'):
                            after_pawn_replacement = board.copy()
                            line = after_pawn_replacement[y2]
                            after_pawn_replacement[y2] = line[:x2] + replacement_piece + line[x2 + 1:]
                            _moves.append(after_pawn_replacement)
                    else:
                        _moves.append(after_pawn_move)
    return _moves


def score(_board: [str])->float:
    """This takes a gameState object and returns the current score of white"""
    _score = 0.0
    for row in _board:
        for square in row:
            _score += PIECE_VALUE[square]
    return _score


def smartScore(board: [str], _player_is_white: bool, depth: int)->[str]:
    if depth == 1:
        if _player_is_white:
            return max(score(_move) for _move in moves(board))
        else:
            return min(score(_move) for _move in moves(board))
    else:
        if _player_is_white:
            return max(smartScore(_move, not _player_is_white, depth - 1) for move in moves(board))
        else:
            return max(smartScore(_move, not _player_is_white, depth - 1) for move in moves(board))


# --------- read in game state ----------
gameHistory = open('game state.txt').read().split('\n')
turn = int(gameHistory[-13].split(' ')[2])
player_is_white = gameHistory[-12][9] == 'w'
whiteTime = float(gameHistory[-11][12:])
blackTime = float(gameHistory[-10][12:])
if player_is_white:
    myTime = whiteTime + 2
    theirTime = blackTime
else:
    myTime = blackTime + 2
    theirTime = whiteTime
gameState = gameHistory[-9:-1]
gameState.reverse()

# ---------- modify game state ----------
gameState = explore(gameState, player_is_white, 3)
'''
i = 0
for move1 in moves(gameState, player_is_white):
    for move2 in moves(move1, not player_is_white):
        for move3 in moves(move2, player_is_white):
            score3 = score(move3)
print(i)
    #print('\n'.join(move3.__reversed__())+'\n')
'''
# ---------- write game state -----------
runTime = time.perf_counter() - startTime
toWrite = '\n-------- turn: {} --------\n'.format(turn+1)
toWrite += 'to move: {}\n'.format('b' if player_is_white else 'w')
toWrite += 'white time: {:.6f}\n'.format(myTime-runTime if player_is_white else theirTime)
toWrite += 'black time: {:.6f}\n'.format(theirTime if player_is_white else myTime-runTime)
toWrite += '\n'.join(gameState.__reversed__())+'\n'
open('new game state.txt', 'a').write(toWrite)
print(toWrite)
print('score: {:.3f}'.format(score(gameState)))
print('run time: {:.3f}ms'.format(runTime*1000))  # micheal take 5.7 seconds to plan 3 moves ahead from the start
