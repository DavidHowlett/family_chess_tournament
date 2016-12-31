import time
import copy
import shared
import David_AI_v2
import David_AI_v1
import Michael_AI_v1_0
import Michael_AI_v1_1
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


def print_state(_turn, board, run_time, white_time_remaining, black_time_remaining, minimise):
    if minimise:
        print('{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t'.format(
            _turn, int(David_AI_v2.simple_score(board)), 'white' if _turn % 2 else 'black', run_time,
            white_time_remaining, black_time_remaining))
    else:
        print('----- move {} -----'.format(_turn))
        print('\n'.join(' '.join(piece for piece in row)for row in board.__reversed__()) + '\n')
        print('{} took: {:.3f} seconds'.format('white' if _turn % 2 else 'black', run_time))
        print('white time: {:.3f}'.format(white_time_remaining))
        print('black time: {:.3f}'.format(black_time_remaining))
        print('score: {}'.format(int(David_AI_v2.simple_score(board))))
        print()


def match(whiteAI, blackAI):
    white_time_remaining = black_time_remaining = initialTime
    history = [[[piece for piece in line] for line in initialBoard.replace(' ', '').split()]]
    history[0].reverse()
    for turn in range(1, 1+turnsToPlayFor):
        start_time = time.perf_counter()
        try:
            chosen_move = (whiteAI if turn % 2 else blackAI)\
                .main(copy.deepcopy(history), white_time_remaining, black_time_remaining)
        except shared.StalemateException:
            print('Draw due to there being no valid moves')
            return 0.5
        except shared.ThreeFoldRepetition:
            print('{} called a draw with the threefold repetition rule'.format('White' if turn % 2 else 'Black'))
            return 0.5
        run_time = time.perf_counter() - start_time
        history.append(chosen_move)
        if turn % 2:
            white_time_remaining = white_time_remaining + timePerMove - run_time
        else:
            black_time_remaining = white_time_remaining + timePerMove - run_time
        print_state(turn, chosen_move, run_time, white_time_remaining, black_time_remaining, False)
        if white_time_remaining < 0:
            print('Black won due to white running out of time')
            return 0
        if black_time_remaining < 0:
            print('White won due to black running out of time')
            return 1
        if not any(any(piece == 'K' for piece in row) for row in chosen_move):
            print('Black won in {} moves'.format(turn))
            return 0
        if not any(any(piece == 'k' for piece in row) for row in chosen_move):
            print('White won in {} moves'.format(turn))
            return 1
    print('Draw due to running out of time')

game_start_time = time.perf_counter()
match(Robert_AI, David_AI_v2)
print('The game took {:.3f} seconds'.format(time.perf_counter()-game_start_time))

competitors = [
    David_AI_v2,
    David_AI_v1,
    Michael_AI_v1_0,
    Michael_AI_v1_1,
    Robert_AI,
    no_move_AI
]
