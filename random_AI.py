"""This player makes a random legal move each turn"""
import David_AI_v3
import random


def main(history, __, ___):
    history = [[''.join(row) for row in board] for board in history] # conversion to David's format
    return random.choice(David_AI_v3.moves(history[-1], len(history) % 2))[0]