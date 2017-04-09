import os
import time
import copy
import hashlib
import inspect
import shared
import David_AI_v6 as ai

initialTime = 5
timePerMove = 1
turnsToPlayFor = 200
competitorNames = [
    'David_AI_v8',
    'David_AI_v7',
    'David_AI_v6',
    'David_AI_v5',
    'David_AI_v4',
    'David_AI_v3',
    'David_AI_v2',
    'David_AI_v1',
    'Michael_AI_v1_2',
    'Michael_AI_v1_1',
    'Michael_AI_v1_0',
    'Robert_AI',
    'Iain_AI_v2',
    'Iain_AI_v1',
    'no_move_AI',
    'random_AI',
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
            _turn, int(ai.evaluate(board)), 'white' if _turn % 2 else 'black', run_time,
            white_time_remaining, black_time_remaining))
    else:
        print('----- move {} -----'.format(_turn))
        print('\n'.join(' '.join(piece for piece in row)for row in board.__reversed__()) + '\n')
        print('{} took: {:.3f} seconds'.format('white' if _turn % 2 else 'black', run_time))
        print('white time: {:.3f}'.format(white_time_remaining))
        print('black time: {:.3f}'.format(black_time_remaining))
        print('score: {:.2f}'.format(ai.evaluate(board)))
        print()


def legal_moves(history, player_is_white):
    """"Generates a list of legal moves. Missing castling, en-passant."""
    board = [''.join(piece for piece in line) for line in history[-1]]
    moves = [[[piece for piece in row] for row in board] for board, _ in ai.moves(board, player_is_white)]
    return moves


def match(white, black):
    """This plays a single match between the white and black players. If the match has been played before then it
    returns quickly with the previous result."""
    # -------- memoization -------
    file_name = r'results/{} vs {}.txt'.format(
        white.__name__,
        black.__name__
    )
    current_versions = '{} vs {}\n'.format(
        hashlib.sha256(inspect.getsource(white).encode()).hexdigest(),
        hashlib.sha256(inspect.getsource(black).encode()).hexdigest())
    try:
        file = open(file_name)
        previous_versions = file.readline()
        if current_versions == previous_versions:
            # then return the previous result
            return eval(file.readline())
    except (FileNotFoundError, SyntaxError):
        pass
    print('Match between {} on white and {} on black'.format(white.__name__, black.__name__))
    file = open(file_name, 'w')
    file.write(current_versions)
    # -------- turns and time -------
    black_moves = white_moves = 0
    black_time_taken = white_time_taken = 0

    history = [[[piece for piece in line] for line in initialBoard.replace(' ', '').split()]]
    history[0].reverse()

    to_return = {'score': 0.5, 'cause': 'Draw due to reaching {} turns'.format(turnsToPlayFor)}
    for turn in range(1, 1+turnsToPlayFor):
        player_is_white = turn % 2
        start_time = time.process_time()
        white_time = initialTime + white_moves * timePerMove - white_time_taken
        black_time = initialTime + black_moves * timePerMove - black_time_taken
        try:
            chosen_move = (white if player_is_white else black).main(
                copy.deepcopy(history), white_time, black_time)
        except shared.StalemateException:
            to_return = {'score': 0.5, 'cause': 'Draw due to stalemate'}
            break
        except shared.ThreeFoldRepetition:
            to_return = {'score': 0.5, 'cause': '{} called a draw with the threefold repetition rule'.format(
                'White' if player_is_white else 'Black')}
            break
        except shared.FiftyMoveException:
            to_return = {'score': 0.5, 'cause': '{} called a draw with the 50 move rule'.format(
                'White' if player_is_white else 'Black')}
            break
        run_time = time.process_time() - start_time
        if player_is_white:
            white_time_taken += run_time
            white_time = initialTime + white_moves * timePerMove - white_time_taken
            white_moves += 1
        else:
            black_time_taken += run_time
            black_time = initialTime + black_moves * timePerMove - black_time_taken
            black_moves += 1
        print_state(turn, chosen_move, run_time, white_time, black_time)
        if white_time < 0:
            to_return = {'score': 0, 'cause': 'Black won due to white running out of time'}
            break
        if black_time < 0:
            to_return = {'score': 1, 'cause': 'White won due to black running out of time'}
            break
        if not any(any(piece == 'K' for piece in row) for row in chosen_move):
            to_return = {'score': 0, 'cause': 'Black won by taking the king'}
            break
        if not any(any(piece == 'k' for piece in row) for row in chosen_move):
            to_return = {'score': 1, 'cause': 'White won by taking the king'}
            break
        if chosen_move not in legal_moves(history, player_is_white):
            if player_is_white:
                to_return = {'score': 0, 'cause': 'Black won because white made an illegal move'}
            else:
                to_return = {'score': 1, 'cause': 'White won because black made an illegal move'}
            break
        # once the move has been shown valid add it to the history
        history.append(chosen_move)
    to_return['white_time_taken'] = white_time_taken
    to_return['black_time_taken'] = black_time_taken
    to_return['white_moves'] = white_moves
    to_return['black_moves'] = black_moves
    file.write(str(to_return))
    to_return['not from file'] = True
    return to_return

minimise = False

tournamentResults = [('white', 'black', 'result', 'moves', 'time', 'explanation')]
for player in competitors:
    player.totalMoves_ = 0
    player.totalTime_ = 0
    player.tournamentScore_ = 0

tournamentStartTime = time.perf_counter()
for white in competitors:
    for black in competitors:
        if white == black:
            continue
        result = match(white, black)
        score = result['score']
        white.tournamentScore_ += score
        white.totalMoves_ += result['white_moves']
        white.totalTime_ += result['white_time_taken']
        black.tournamentScore_ += (1 - score)
        black.totalMoves_ += result['black_moves']
        black.totalTime_ += result['black_time_taken']
        if 'not from file' in result:
            print(result['cause'])
            print('The game took {:.3f} seconds'.format(result['white_time_taken'] + result['black_time_taken']))
        tournamentResults.append(
            (white.__name__, black.__name__, score, result['black_moves'] + result['white_moves'],
             '{:.3f}'.format(result['black_time_taken'] + result['white_time_taken']), result['cause']))

print('\nAll the matches played in the tournament are shown below')

for result in tournamentResults:
    print(''.join('{:<16}'.format(r) for r in result), sep='\t')

print('\nThe tournament took: {:.1f} seconds'.format(time.perf_counter()-tournamentStartTime))
print('Each of the {} competitors has played {} games\n'.format(
    len(competitors), 2*len(competitors)-2))

competitors.sort(key=lambda c: c.tournamentScore_, reverse=True)
for player in competitors:
    print('{} scored {}/{} taking on average {:.3f} seconds'.format(
        player.__name__, player.tournamentScore_, 2*len(competitors)-2, player.totalTime_/player.totalMoves_))

if os.name == 'posix':
    # it can take a while to run and I want to do other things in the mean time
    os.system('say "tournament finished"')