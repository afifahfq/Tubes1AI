import random
from time import time

from src.constant import ShapeConstant
from src.model import *

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

import random
import math
from copy import deepcopy
from time import time

from src.utility import *
from src.model import State, Config

from typing import Tuple, List


'''class Minimax2:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement'''

class MinimaxGroup40:
    def __init__(self):
        self.alpha = -math.inf
        self.beta = math.inf

    def findEmptyCell(self, state: State):
        for col in range(0, state.board.col, 1):
            for row in range(state.board.row - 1, -1, -1):
                if state.board[row, col].shape == ShapeConstant.BLANK:
                    return [row, col]
        return None

    def listEmptyCells(self, state: State):
        solusi = []
        i = 0

        currCell = findEmptyCell(state)
        while (currCell != None):
            solusi[i] = currCell
            i += 1
            currCell = findEmptyCell(state)
        return solusi

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        if (is_win(state.board) == None and is_full(state.board) == False):
            emptyCell = listEmptyCells(state)

            if (n_player == self.config.player_choice):
                bestValue = -999
                
                i = 0
                while (i > len(emptyCell)):
                    j = 0
                    while (j > 1):
                        # board = Board(config.row, config.col)
                        stateX = state
                        if (stateX.players[n_player].quota["X"] > 1):
                            place(stateX, stateX.players[n_player], ShapeConstant.CROSS, emptyCell[i][1])
                            valueX = find(stateX, n_player, thinking_time)

                        stateO = state
                        if (stateO.players[n_player].quota["O"] > 1):
                            place(stateO, stateO.players[n_player], ShapeConstant.CIRCLE, emptyCell[i][1])
                            valueO = find(stateO, n_player, thinking_time)

                        if (state.players[n_player].shape == "X" and valueX >= valueO):
                            value = valueX
                            shape = "X"
                        elif (state.players[n_player].shape == "O" and valueO >= valueX):
                            value = valueO
                            shape = "O"
                        elif (valueO >= valueX):
                            value = valueO
                            shape = "O"
                        else: # valueX >= valueO
                            value = valueX
                            shape = "X"

                        if (value > bestValue):
                            bestValue = value
                            bestCell = emptyCell[i]

                        self.alpha = max(self.alpha, bestValue)
                        if (self.alpha >= self.beta):
                            break

                        j += 1
                    i += 1

                best_movement = (bestCell[1], shape)
                return best_movement

            else: #(n_player != self.config.player_choice)
                bestValue = 999
                
                i = 0
                while (i > len(emptyCell)):
                    j = 0
                    while (j > 1):
                        # board = Board(config.row, config.col)
                        stateX = state
                        if (stateX.players[n_player].quota["X"] > 1):
                            place(stateX, stateX.players[n_player], ShapeConstant.CROSS, emptyCell[i][1])
                            valueX = find(stateX, n_player, thinking_time)

                        stateO = state
                        if (stateO.players[n_player].quota["O"] > 1):
                            place(stateO, stateO.players[n_player], ShapeConstant.CIRCLE, emptyCell[i][1])
                            valueO = find(stateO, n_player, thinking_time)

                        if (state.players[n_player].shape == "X" and valueX < valueO):
                            value = valueX
                            shape = "X"
                        elif (state.players[n_player].shape == "O" and valueO < valueX):
                            value = valueO
                            shape = "O"
                        elif (valueO < valueX):
                            value = valueO
                            shape = "O"
                        else: # valueX < valueO
                            value = valueX
                            shape = "X"

                        if (value < bestValue):
                            bestValue = value
                            bestCell = emptyCell[i]

                        self.beta = min(self.beta, bestValue)
                        if (self.alpha >= self.beta):
                            break

                        j += 1
                    i += 1

                best_movement = (bestCell[1], shape)
                return best_movement
        
        else: # game dalam terminal state
            return (-1, -1)


