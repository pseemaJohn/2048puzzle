# 2048puzzle
implement 2048 using minimax algorithm and a heuristic

# File Name : PlayerAI.py
# Description : implements the minimax and alpha-beta pruning algorithm for 2048 puzzle 
# the class object is invoked by GameManager file
# Called function  : getMove
# Function Details : The function implements minimax and alpha-beta pruning algo and returns 
# back the move it considers most successful in helping the player win against the computer
# to improve the move probability to be the best heuristics are used to add score
# heuristics used are - number of empty cells, just using it improves the search,
# but if u add weight that's log of score it becomes better
# in addition added clustering score reference - http://blog.datumbox.com/using-artificial-intelligence-to-solve-the-2048-game-java-code/
# Input Parameter : Grid (state of board)
# output Parameter : the move
