import time
import copy
import shared
import David_AI_v2
import David_AI_v1
import Michael_AI_v1_1 as Michael_AI
import Robert_AI
import no_move_AI

initialTime = 5
timePerMove = 1
turnsToPlayFor = 200
initialBoard = '''
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R'''


def print_state(_turn, board, run_time, whiteTimeRemaining, blackTimeRemaining):
    print('----- move {} -----'.format(_turn))
    print('\n'.join(' '.join(piece for piece in row)for row in board.__reversed__()) + '\n')
    print('{} took: {:.3f} seconds'.format('white' if _turn % 2 else 'black', run_time))
    print('white time: {:.3f}'.format(whiteTimeRemaining))
    print('black time: {:.3f}'.format(blackTimeRemaining))
    print('score: {}'.format(int(David_AI_v2.simple_score(board))))
    print()


def match(whiteAI, blackAI):
    whiteTimeRemaining = blackTimeRemaining = initialTime
    history = [[[piece for piece in line] for line in initialBoard.replace(' ', '').split()]]
    history[0].reverse()
    for turn in range(1, 1+turnsToPlayFor):
        start_time = time.perf_counter()
        try:
            chosen_move = (whiteAI if turn % 2 else blackAI)\
                .main(copy.deepcopy(history), whiteTimeRemaining, blackTimeRemaining)
        except shared.StalemateException:
            print('Draw due to there being no valid moves')
            return
        except shared.ThreeFoldRepetition:
            print('{} called a draw with the threefold repetition rule'.format('White' if turn % 2 else 'Black'))
            return
        run_time = time.perf_counter() - start_time
        history.append(chosen_move)
        if turn % 2:
            whiteTimeRemaining = whiteTimeRemaining + timePerMove - run_time
        else:
            blackTimeRemaining = whiteTimeRemaining + timePerMove - run_time
        print_state(turn, chosen_move, run_time, whiteTimeRemaining, blackTimeRemaining)
        if whiteTimeRemaining < 0:
            print('Black won due to white running out of time')
            return
        if blackTimeRemaining < 0:
            print('White won due to black running out of time')
            return
        if not any(any(piece == 'k' for piece in row) for row in chosen_move):
            print('White won in {} moves'.format(turn))
            return
        if not any(any(piece == 'K' for piece in row) for row in chosen_move):
            print('Black won in {} moves'.format(turn))
            return
    print('Draw due to running out of time')

game_start_time = time.perf_counter()
match(David_AI_v2, Robert_AI)
print('The game took {:.3f} seconds'.format(time.perf_counter()-game_start_time))
