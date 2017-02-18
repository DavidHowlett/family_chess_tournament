"""This player makes a random legal move each turn"""
import David_AI_v3
import random


def main(history, _, __):
    history = [[''.join(row) for row in board] for board in history]  # conversion to David's format
    move = random.choice(David_AI_v3.moves(history[-1], len(history) % 2))[0]
    return [[p for p in line] for line in move]
