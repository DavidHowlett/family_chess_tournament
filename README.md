# family_chess_tournament
Christmas 2016 I am competing with my brother and my mum to see who can produce the best chess AI

# rules
The AI will work by reading in a file called “game state.txt”
looking at the last game state then appending a new game state to the file.
The programs of the players will be run alternately.
The players are required to increment their timer by the amount of time it took to move.

A player looses if:
    - they make an illegal move
    - the total time by them spent exceeds 60 seconds
    - their king is taken

Human players have no time limit on their moves
