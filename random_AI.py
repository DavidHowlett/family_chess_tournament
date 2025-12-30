"""This player makes a random legal move each turn"""

import random

import David_AI_v9 as ai


def main(history, _, __):
    possible_moves = list(ai.legal_moves(ai.to_array(history[-1]), len(history) % 2))
    move = random.choice(possible_moves)[0]
    return ai.from_array(move)
