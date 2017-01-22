import time
import copy
import shared
initialTime = 5
timePerMove = 1
turnsToPlayFor = 150
competitorNames = [
    'David_AI_v3',
    'David_AI_v2',
    'David_AI_v1',
    'Michael_AI_v1_2',
    'Michael_AI_v1_1',
    'Michael_AI_v1_0',
    'Robert_AI',
    'random_AI',
    # 'no_move_AI',
]
for name in competitorNames:
    exec('import ' + name)

competitors = [eval(name) for name in competitorNames]

initialBoard = '''
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R'''


def print_state(_turn, board, run_time, white_time_remaining, black_time_remaining):
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


def match(white, black):
    print('Match between {} on white and {} on black'.format(white.__name__, black.__name__))
    white_time_remaining = black_time_remaining = initialTime
    history = [[[piece for piece in line] for line in initialBoard.replace(' ', '').split()]]
    history[0].reverse()
    for turn in range(1, 1+turnsToPlayFor):
        start_time = time.process_time()
        try:
            chosen_move = (white if turn % 2 else black).main(
                copy.deepcopy(history), white_time_remaining, black_time_remaining)
        except shared.StalemateException:
            return 0.5, 'Draw due to stalemate'
        except shared.ThreeFoldRepetition:
            return 0.5, '{} called a draw with the threefold repetition rule'.format('White' if turn % 2 else 'Black')
        except shared.FiftyMoveException:
            return 0.5, '{} called a draw with the 50 move rule'.format('White' if turn % 2 else 'Black')
        run_time = time.process_time() - start_time
        history.append(chosen_move)
        if turn % 2:
            white_time_remaining = white_time_remaining + timePerMove - run_time
        else:
            black_time_remaining = black_time_remaining + timePerMove - run_time
        print_state(turn, chosen_move, run_time, white_time_remaining, black_time_remaining)
        if white_time_remaining < 0:
            return 0, 'Black won due to white running out of time'
        if black_time_remaining < 0:
            return 1, 'White won due to black running out of time'
        if 'P' in chosen_move[7]:
            return 0, 'Black won because white made and illegal move'
        if 'p' in chosen_move[0]:
            return 1, 'White won because black made and illegal move'
        if not any(any(piece == 'K' for piece in row) for row in chosen_move):
            return 0, 'Black won by taking the king'
        if not any(any(piece == 'k' for piece in row) for row in chosen_move):
            return 1, 'White won by taking the king'
    return 0.5, 'Draw due to reaching {} turns'.format(turnsToPlayFor)

minimise = False

#match(David_AI_v3, no_move_AI)
#exit()

tournamentResults = [('white', 'black', 'result', 'explanation')]
for player in competitors:
    player.tournamentScore = 0

tournamentStartTime = time.perf_counter()
for white in competitors:
    for black in competitors:
        if white == black:
            continue
        game_start_time = time.perf_counter()
        result, cause = match(white, black)
        print(cause)
        print('The game took {:.3f} seconds'.format(time.perf_counter() - game_start_time))
        tournamentResults.append((white.__name__, black.__name__, result, cause))
        white.tournamentScore += result
        black.tournamentScore += (1-result)
print('\nAll the matches played in the tournament are shown below')

for result in tournamentResults:
    print(''.join('{:<16}'.format(r) for r in result), sep='\t')

print('\nThe tournament took: {:.3f} seconds'.format(time.perf_counter()-tournamentStartTime))
print('Each of the {} competitors has played {} games\n'.format(
    len(competitors), 2*len(competitors)-2))

competitors.sort(key=lambda c: c.tournamentScore, reverse=True)
for player in competitors:
    print('{} score is {}/{}'.format(
        player.__name__, player.tournamentScore, 2*len(competitors)-2))