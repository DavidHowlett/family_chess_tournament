import time
import copy
import shared
import David_AI_v3
import David_AI_v2
import David_AI_v1
import Michael_AI_v1_1
import Michael_AI_v1_0
import Robert_AI
import no_move_AI
import random_AI

initialTime = 5
timePerMove = 1
turnsToPlayFor = 150

David_AI_v3.__name = 'David_AI_v3'
David_AI_v2.__name = 'David_AI_v2'
David_AI_v1.__name = 'David_AI_v1'
Michael_AI_v1_1.__name = 'Michael_AI_v1_1'
Michael_AI_v1_0.__name = 'Michael_AI_v1_0'
Robert_AI.__name = 'Robert_AI'
no_move_AI.__name = 'no_move_AI'
random_AI.__name = 'random_AI'


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


def match(whiteAI, blackAI):
    print('Match between {} on white and {} on black'.format(whiteAI.__name, blackAI.__name))
    white_time_remaining = black_time_remaining = initialTime
    history = [[[piece for piece in line] for line in initialBoard.replace(' ', '').split()]]
    history[0].reverse()
    for turn in range(1, 1+turnsToPlayFor):
        start_time = time.process_time()
        try:
            chosen_move = (whiteAI if turn % 2 else blackAI)\
                .main(copy.deepcopy(history), white_time_remaining, black_time_remaining)
        except shared.StalemateException:
            return 0.5, 'Draw due to there being no valid moves'
        except shared.ThreeFoldRepetition:
            return 0.5, '{} called a draw with the threefold repetition rule'.format('White' if turn % 2 else 'Black')
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

competitors = [
    David_AI_v3,
    David_AI_v2,
    David_AI_v1,
    Michael_AI_v1_1,
    Michael_AI_v1_0,
    Robert_AI,
    random_AI
    # no_move_AI,

]
tournamentResults = [('white', 'black', 'result', 'explanation')]
for AI in competitors:
    AI.tournamentScore = 0

tournamentStartTime = time.perf_counter()
for whitePlayer in competitors:
    for blackPlayer in competitors:
        if whitePlayer == blackPlayer:
            continue
        game_start_time = time.perf_counter()
        result, cause = match(whitePlayer, blackPlayer)
        print(cause)
        print('The game took {:.3f} seconds'.format(time.perf_counter() - game_start_time))
        tournamentResults.append((whitePlayer.__name, blackPlayer.__name, result, cause))
        whitePlayer.tournamentScore += result
        blackPlayer.tournamentScore += (1-result)
print('\nAll the matches played in the tournament are shown below')

for result in tournamentResults:
    print(''.join('{:<16}'.format(r) for r in result), sep='\t')

print('\nThe tournament took: {:.3f} seconds'.format(time.perf_counter()-tournamentStartTime))
print('Each of the {} competitors has played {} games\n'.format(
    len(competitors), 2*len(competitors)-2))

competitors.sort(key=lambda c: c.tournamentScore, reverse=True)
for AI in competitors:
    print('{} score is {}/{}'.format(
        AI.__name, AI.tournamentScore, 2*len(competitors)-2))