import os
import time
import copy
from array import array
import hashlib
import inspect
import shared
import David_AI_v9 as ai

initialTime = 5
timePerMove = 1
turnsToPlayFor = 250
extraRepeatTime = 0.1
competitorNames = [
    # 'David_AI_v9',
    # 'David_AI_v8',
    # 'David_AI_v7',
    # 'David_AI_v6',
    # 'David_AI_v5',
    # 'David_AI_v4',
    # 'David_AI_v3',
    'David_AI_v2',
    # 'David_AI_v1',
    'Iain_AI_v2',
    # 'Iain_AI_v1',
    # 'Michael_AI_v1_3',
    # 'Michael_AI_v1_2',
    # 'Michael_AI_v1_1',
    # 'Michael_AI_v1_0',
    # 'Robert_AI',
    # 'no_search',
    # 'no_move_AI',
    # 'random_AI',
    # 'Human_player'
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


def print_state(_turn, board, run_time, white_time_remaining, black_time_remaining, white, black, repeat):
    ai.recalculate_position_values(ai.to_array(board))
    print(f'----- {white.__name__} vs {black.__name__} match {repeat} move {_turn} -----')
    print('\n'.join(' '.join(piece for piece in row)for row in board.__reversed__()) + '\n')
    print('{} took: {:.3f} seconds'.format('white' if _turn % 2 else 'black', run_time))
    print('white time: {:.3f}'.format(white_time_remaining))
    print('black time: {:.3f}'.format(black_time_remaining))
    print('score: {:.1f}'.format(ai.evaluate(ai.to_array(board))))
    print()


def legal_moves(history, player_is_white):
    """"Generates a list of legal moves. Missing castling, en-passant."""
    board = ai.to_array(history)[-1]
    moves = list(ai.moves(board, player_is_white))
    assert type(moves[0][0]) == array
    moves = [ai.from_array(move) for move, _score in moves]
    return moves


def make_file_name(white, black, repeat):
    return rf'results/{white.__name__} vs {black.__name__} repeat {repeat}.txt'


def source_hash(player):
    # this line makes things the same on windows and unix
    normalised_source = '\n'.join(inspect.getsource(player).split())
    return hashlib.sha256(normalised_source.encode()).hexdigest()


def match(white, black, repeat):
    """This plays a single match between the white and black players and records the result."""
    print(f'\nMatch {repeat} between {white.__name__} on white and {black.__name__} on black')
    # -------- turns and time -------
    black_moves = white_moves = 0
    black_time_taken = white_time_taken = 0

    history = [[[piece for piece in line] for line in initialBoard.replace(' ', '').split()]]
    history[0].reverse()

    to_record = {'score': 0.5, 'cause': 'Draw due to reaching {} turns'.format(turnsToPlayFor)}
    for turn in range(1, 1+turnsToPlayFor):
        player_is_white = turn % 2
        start_time = time.process_time()
        white_time = initialTime + white_moves * (timePerMove + (repeat - 1) * extraRepeatTime) - white_time_taken
        black_time = initialTime + black_moves * (timePerMove + (repeat - 1) * extraRepeatTime) - black_time_taken
        try:
            chosen_move = (white if player_is_white else black).main(
                copy.deepcopy(history), white_time, black_time)
        except shared.StalemateException:
            to_record = {'score': 0.5, 'cause': 'Draw due to stalemate'}
            break
        except shared.ThreeFoldRepetition:
            to_record = {'score': 0.5, 'cause': '{} called a draw with the threefold repetition rule'.format(
                'White' if player_is_white else 'Black')}
            break
        except shared.FiftyMoveException:
            to_record = {'score': 0.5, 'cause': '{} called a draw with the 50 move rule'.format(
                'White' if player_is_white else 'Black')}
            break
        run_time = time.process_time() - start_time
        if player_is_white:
            white_time_taken += run_time
            white_time = initialTime + white_moves * (timePerMove + (repeat - 1) * extraRepeatTime) - white_time_taken
            white_moves += 1
        else:
            black_time_taken += run_time
            black_time = initialTime + black_moves * (timePerMove + (repeat - 1) * extraRepeatTime) - black_time_taken
            black_moves += 1
        print_state(turn, chosen_move, run_time, white_time, black_time, white, black, repeat)
        if white_time < 0:
            to_record = {'score': 0, 'cause': 'Black won due to white running out of time'}
            break
        if black_time < 0:
            to_record = {'score': 1, 'cause': 'White won due to black running out of time'}
            break
        if not any(any(piece == 'K' for piece in row) for row in chosen_move):
            to_record = {'score': 0, 'cause': 'Black won by taking the king'}
            break
        if not any(any(piece == 'k' for piece in row) for row in chosen_move):
            to_record = {'score': 1, 'cause': 'White won by taking the king'}
            break
        if chosen_move not in legal_moves(history, player_is_white):
            if player_is_white:
                to_record = {'score': 0, 'cause': 'Black won because white made an illegal move'}
            else:
                to_record = {'score': 1, 'cause': 'White won because black made an illegal move'}
            break
        # once the move has been shown valid add it to the history
        history.append(chosen_move)
    to_record['white_time_taken'] = white_time_taken
    to_record['black_time_taken'] = black_time_taken
    to_record['white_moves'] = white_moves
    to_record['black_moves'] = black_moves
    print(to_record['cause'])
    open(make_file_name(white, black, repeat), 'w').write(current_versions+str(to_record))

if __name__ == '__main__':
    tournamentStartTime = time.perf_counter()
    for repeat in range(1, 1000):
        for white in competitors:
            for black in competitors:
                if white == black:
                    continue
                file_name = make_file_name(white, black, repeat)
                current_versions = (
                    f'{source_hash(white)} vs {source_hash(black)} repeat {repeat}\n')
                try:
                    file = open(file_name)
                    previous_versions = file.readline()
                    if current_versions == previous_versions:
                        # then skip this match
                        continue
                except (FileNotFoundError, SyntaxError):
                    pass
                match(white, black, repeat)

    if os.name == 'posix':
        # it can take a while to run and I want to do other things in the mean time
        os.system('say "tournament finished"')