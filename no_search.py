"""For fun I will try to write a player with no ability to search ahead, only an eval function"""
import David_AI_v9 as ai


def main(given_history, _, __):
    history = ai.to_array(given_history)
    player_is_white = len(history) % 2 == 1
    current_board = history[-1]
    best_score = -10**10
    for move, diff in ai.legal_moves(current_board, player_is_white):
        score = ai.evaluate(move)
        if not player_is_white:
            score = -score
        if score > best_score:
            best_score = score
            best_move = move
    print(f'search depth: 1')
    print(f'expected score: {best_score}')
    return ai.from_array(best_move)
