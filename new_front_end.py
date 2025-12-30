"""
The main way to run this project is to run the runner.py file but runner.py was designed for programs to play
each other.

To allow my chess engine to play a single game against my Dad I created this hacky new front end for my chess program.
Every time he made a move I edited the below board to match the new board state and then re-ran this file
to get the next move of my engine. The below board is the point at which my dad (lowercase, black) resigned."""

import time

import David_AI_v9

currentBoard = """
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R"""

playerIsWhite = True

history = [
    list([list(line) for line in currentBoard.replace(" ", "").split()].__reversed__())
]
history *= (not playerIsWhite) + 1
startTime = time.perf_counter()
chosen_move = David_AI_v9.main(history, 10, 10)
print("computation took", time.perf_counter() - startTime, "seconds")
print(("\n".join(" ".join(row) for row in chosen_move.__reversed__()) + "\n"))
