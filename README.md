# Family AI chess tournament

Christmas 2016 the 3 Howlett brothers competed to see who could produce the best chess AI.
We agreed to build our AI's without looking at any of the existing literature or code on the subject.
David, Robert and Micheal all produced functional chess AI's in python.
David's AI was winning by the end of the christmas holidays.
After the christmas holidays we looked at the existing literature.

# How to play

- Clone the repo
- run runner.py and see how it works
- Add your own AI file
- Tweak the runner to run your file with the others.
- Check that your AI can play games without crashing anything
- Submit a pull request to David's copy of the repo

# Rules

Each player must provide a function called "main" that takes the
history of the game so far and returns a new board with the chosen move.

Using other people's chess code is not allowed. You must write your own AI.
Using libraries that are not chess specific are allowed. For example TensorFlow is ok.

Each player gets 5 seconds initially and gets 1 additional second to make each move.
This ensures that all games finish quickly.

A player loses if:
- They make an illegal move
- Their time remaining hits 0

Currently the runner will call a draw after 250 moves to prevent infinite games.
This maximum may be changed in future.

If a player wants to call a draw they should raise one of the exceptions in shared.py
Please only call draws when it is legal to do so.
