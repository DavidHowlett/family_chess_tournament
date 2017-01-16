# Family AI chess tournament

Christmas 2016 the 3 Howlett brothers competed to see who could produce the best chess AI. 
We agreed to build our AI's without looking at any of the existing literature or code on the subject.
David, Robert and Micheal all produced functional chess AI's in python.
David's AI was winning by the end of the christmas holidays. 

# How to play

- Clone the repo
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
This ensures that all games finish in sensible amounts of time.

The rules differ slightly from standard chess.

A player loses if:
- They make an illegal move
- Their time remaining hits 0
- Their king is taken (checking for the king being taken is a little easier then checking for checkmate)

Currently the runner will call a draw after 150 moves to prevent infinite games. 
This maximum may be increased in future. 

If a player wants to call a draw they should raise one of the exceptions in the shared file. 
Please only call draws when it is legal to do so.

# To do

Make the runner remember the results of matches between AI's with particular hashes. 
This should save time when re running the tournament after changing only one AI.
