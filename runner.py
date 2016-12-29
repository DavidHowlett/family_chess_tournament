import time
import copy
import shared
import David_AI
import David_AI_old
import Michael_AI_v1_1 as Michael_AI
import Robert_AI

initialTime = 5
timePerMove = 1
turnsToPlayFor = 200
initialBoard = '''
rnbqkbnr
pppppppp
........
........
........
........
PPPPPPPP
RNBQKBNR'''
white = {'time remaining': initialTime, 'AI': David_AI}
black = {'time remaining': initialTime, 'AI': David_AI_old}


def print_state(_turn, board, run_time):
    print('----- move {} -----'.format(_turn))
    print('\n'.join(' '.join(piece for piece in row)for row in board.__reversed__()) + '\n')
    print('{} took: {:.3f} seconds'.format('white' if _turn % 2 else 'black', run_time))
    print('white time: {:.3f}'.format(white['time remaining']))
    print('black time: {:.3f}'.format(black['time remaining']))
    print('score: {}'.format(int(David_AI.simple_score(board))))
    print()


def main():
    history = [[[piece for piece in line] for line in initialBoard.split()]]
    history[0].reverse()
    for turn in range(1, 1+turnsToPlayFor):
        player = white if turn % 2 else black
        start_time = time.perf_counter()
        try:
            chosen_move = player['AI'].main(copy.deepcopy(history), white['time remaining'], black['time remaining'])
        except shared.StalemateException:
            print('Draw due to there being no valid moves')
            return
        except shared.ThreeFoldRepetition:
            print('{} called a draw with the threefold repetition rule'.format('White' if turn % 2 else 'Black'))
            return
        run_time = time.perf_counter() - start_time
        history.append(chosen_move)
        player['time remaining'] = player['time remaining'] + timePerMove - run_time
        print_state(turn, chosen_move, run_time)
        if white['time remaining'] < 0:
            print('Black won due to white running out of time')
            return
        if black['time remaining'] < 0:
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
main()
print('The game took {:.3f} seconds'.format(time.perf_counter()-game_start_time))
