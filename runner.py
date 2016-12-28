import time
import copy
import David_AI
import Michael_AI_v1_1 as Micheal_AI

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
black = {'time remaining': initialTime, 'AI': Micheal_AI}


def print_state(_turn, board, run_time):
    print('----- move {} -----'.format(_turn))
    print('\n'.join(''.join(piece for piece in row)for row in board.__reversed__()) + '\n')
    print('run time: {:.3f} seconds'.format(run_time))
    #print('\n\nto move: {}\n'.format('w' if i % 2 else 'b'))
    print('white time: {:.6f}'.format(white['time remaining']))
    print('black time: {:.6f}'.format(black['time remaining']))
    print('score: {}'.format(int(David_AI.simple_score(board))))
    print()


def main():
    history = [[[piece for piece in line] for line in initialBoard.split()]]
    history[0].reverse()
    for turn in range(1, 1+turnsToPlayFor):
        player = white if turn % 2 else black
        startTime = time.perf_counter()
        try:
            chosenMove = player['AI'].main(copy.deepcopy(history), white['time remaining'], black['time remaining'])
        except ZeroDivisionError:  # catch stalemate here
            pass
        runTime = time.perf_counter() - startTime
        history.append(chosenMove)
        player['time remaining'] = player['time remaining'] + timePerMove - runTime
        print_state(turn, chosenMove, runTime)
        if not any(any(piece == 'k' for piece in row) for row in chosenMove):
            print('White won in {} moves'.format(turn))
            exit()
        if not any(any(piece == 'K' for piece in row) for row in chosenMove):
            print('Black won in {} moves'.format(turn))
            exit()
    print('Draw due to running out of time')

main()
