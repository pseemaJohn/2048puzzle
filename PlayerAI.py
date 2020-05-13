# File Name : PlayerAI.py
# Description : implements the minimax and alpha-beta pruning algorithm for 2048 puzzle \
# the class object is invoked by GameManager file
# Called function  : getMove
# Function Details : The function implements minimax and alpha-beta pruning algo and returns \
# back the move it considers most successful in helping the player win against the computer
# to improve the move probability to be the best heuristics are used to add score
# heuristics used are - number of empty cells, just using it improves the search,\
# but if u add weight that's log of score it becomes better\
# in addition added clustering score reference - http://blog.datumbox.com/using-artificial-intelligence-to-solve-the-2048-game-java-code/
# Input Parameter : Grid (state of board)
# output Parameter : the move


from BaseAI import BaseAI
from random import randint
import math
import time

# below list is to identify the clustering val
clusterRange = [[(0, 1), (1, 0)], [(0, 0), (1, 1), (0, 2)], [(0, 1), (1, 2), (0, 3)], [(0, 2), (1, 3)],
                [(0, 0), (1, 1), (2, 1)], [(0, 1), (1, 1), (2, 1), (1, 2)], [(0, 2), (1, 1), (1, 3), (2, 2)],
                [(0, 2), (1, 2), (2, 3)], [(1, 0), (2, 1), (3, 0)], [(2, 0), (1, 1), (2, 2), (3, 1)],
                [(2, 1), (1, 2), (2, 3), (3, 2)], [(1, 3), (2, 2), (3, 3)], [(2, 0), (3, 1)], [(3, 0), (2, 1), (3, 2)],
                [(3, 1), (2, 2), (3, 3)], [(2, 3), (3, 2)]]


class PlayerAI(BaseAI):
    def __init__(self):
        self.player1 = True
        self.player2 = False
        self.startTime = 0
        return

    # Function name - getMove
    # Input parameter - grid
    # Output parameter - move pos
    # this function is invoked by Game Manager

    def getMove(self, grid):
        # adding depth of 7
        self.startTime = time.perf_counter()
        move, bestScore, _, _, _ = self.getMinMaxVal(grid, 5, -1, self.player1, -math.inf, math.inf)
        # print("GetMove: Move value is  ",move, "and Score is ", bestScore)
        return move

    # function name  : player2play
    # Function Details : Performs the action to be taken by second player (computer) \
    # this function basically tries to what the computer could do to get minimum val
    # Input Parameter : Grid (state of board)
    # Output Parameter : List containing grids with value of 2 or 4 in different position
    # the function contains 3 different moves that can be considered by player 2, the one selected is based on the output
    def player2play(self, grid):
        player2children = []
        cells = grid.getAvailableCells()
        for cell in cells:
            if randint(0, 99) < 100 * 0.9:
                val = 2
            else:
                val = 4
            # third format
            # if cell in [[0,0],[0,3],[3,0],[3,3]]: #max it gives is 128
            #    val = 4
            # else:
            #   val = 2
            cloneGrid = grid.clone()
            cloneGrid.setCellValue(cell, val)
            # second format
            # cloneGrid1 = grid.clone()
            # cloneGrid.setCellValue(cell, 2)
            # cloneGrid1.setCellValue(cell, 4)
            # player2children.append(cloneGrid1)
            player2children.append(cloneGrid)
        return player2children

    # function name  : getclusterval
    # Function Details : Implements the heuristic of clustering \
    # this function calculates the heuristic by using the technique of clustering
    # Input Parameter : list (list of state of board)
    # Output Parameter : heuristic value of the board.
    # the function contains 3 different moves that can be considered by player 2, the one selected is based on the output
    def getclusterval(self, maplist):
        clusterscore = 0
        counter = 0
        for i in range(4):
            for j in range(4):
                for k in clusterRange[counter]:
                    clusterscore = clusterscore + abs(maplist[i][j] - maplist[k[0]][k[1]])
                counter += 1
        return clusterscore

    def getmontonocityval(self, maplist):
        monoscore = 0
        monolist = []
        counter = 0
        order = [3,3,0,0]
        round = 1
        for k in range(4):
            for i in range(4):
                if k >= 2:
                    counter = (order[k]* round) - i
                    if k == 3:
                        counter *= -1
                else:
                    counter = (order[k] - i) * round
                #print("Value of k=",k,"Value of i = ",i, "Value of round =", round)
                for j in range(4):
                    monoscore = monoscore + (counter * maplist[i][j])
                    #print("Counter = ",counter, "monoscore = ",monoscore)
                    counter -= round
            if k == 1:
                round = round * 1
            else:
                round = round * -1
            monolist.append(monoscore)
        return max(monolist)
    # function name  : getMinMaxVal
    # Function Details : Implements the minimax and alpha-beta pruning \
    # this function implements minimax and alpha-bets pruning and returns back the position based on the heurisitic value
    # Input Parameter : grid (state of board), depth (search depth), move (move selected), \
    # flag (player1 or player2), bestAlphaScore (aplha score), bestBetaScore (beta Score)
    # Output Parameter : move the board should make.
    # the function contains 3 different moves that can be considered by player 2, the one selected is based on the output

    def getMinMaxVal(self, grid, depth, move, flag, bestAlphaScore, bestBetaScore):
        score = 0
        bestScore = 0
        retFlag = False
        if (time.perf_counter() - self.startTime) > 0.2 or depth == 0 or grid.canMove() is False:
            scoreTemp = grid.getMaxTile()
            scoreTemp += math.log(scoreTemp) * len(grid.getAvailableCells())
            #temp = scoreTemp - self.getclusterval(grid.map)
            #if temp > 0:
                #scoreTemp = temp
            scoreTemp += self.getmontonocityval(grid.map)
            #exit(0)
            return move, scoreTemp , bestAlphaScore, bestBetaScore, True

        if flag == self.player1:
            player1moves = grid.getAvailableMoves()
            for noC, player1move in enumerate(player1moves):
                tempGrid = grid.clone()
                tempGrid.move(player1move)
                _, score, AlphaScore, BetaScore, retFlag = self.getMinMaxVal(tempGrid, depth - 1, player1move,
                                                                             self.player2, bestAlphaScore,
                                                                             bestBetaScore)

                if bestScore == 0 or score > bestScore:
                    bestScore = score
                    move = player1move
                if retFlag == False:
                    bestAlphaScore = max(BetaScore, AlphaScore, bestAlphaScore)
                else:
                    bestAlphaScore = max(bestAlphaScore, score)
                if bestAlphaScore >= bestBetaScore:
                    return (move, bestScore, bestAlphaScore, bestBetaScore, False)
            return (move, bestScore, bestAlphaScore, bestBetaScore, False)
        else:  # player2
            player2moves = self.player2play(grid)

            for noc1, player2move in enumerate(player2moves):
                _, score, AlphaScore, BetaScore, retFlag = self.getMinMaxVal(player2move, depth - 1, move, self.player1,
                                                                             bestAlphaScore, bestBetaScore)
                if bestScore == 0 or score < bestScore:
                    bestScore = score
                if retFlag == False:
                    bestBetaScore = min(BetaScore, AlphaScore, bestBetaScore)
                else:
                    bestBetaScore = min(bestBetaScore, score)

                if bestAlphaScore >= bestBetaScore:
                    return (move, bestScore, bestAlphaScore, bestBetaScore, False)
            return (move, bestScore, bestAlphaScore, bestBetaScore, False)
