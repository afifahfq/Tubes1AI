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

def findEmptyCell(state: State):
    for col in range(0, state.board.col, 1):
        for row in range(0, state.board.row, 1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return [row, col]
    return None

def createEmptyCells(state: State):
    solusi = []

    for col in range(0, state.board.col, 1):
        for row in range(0, state.board.row, 1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                solusi.append([row, col])
    return solusi

def listMoves(state: State, n_player):
    quota = state.players[n_player].quota
    listMoves = []

    for key, value in quota.items():
        if (value == 0):
            continue

        for col in range(state.board.col):
            listMoves.append((col, key))
    return listMoves

def checkRound(state: State, n_player: int):
    if n_player == 0:
        if (state.round % 2 == 1):
            return True
        else:
            return False
    else:
        if (state.round % 2 == 0):
            return True
        else:
            return False

class MinimaxGroup40:
    def __init__(self):
        self.alpha = -math.inf
        self.beta = math.inf

    def minimax(self, turn: bool, state: State, depth: int, listCells: List[int], alpha: int, beta: int, goalPath: List[State] = []):
        if (depth == 0 or is_win(state.board) == True or is_full(state.board) == True):
            return goalPath, 0
        else:
            if (turn):
                bestValue = -math.inf
                bestPath = None

                print(listCells)
                for cell in listCells:
                    newState = deepcopy(state)
                    posisi = place(newState, self.n_player, cell[1], cell[0])

                    if posisi != -1:
                        newPath = deepcopy(goalPath)
                        newPath.append((cell, newState))

                        path, value = self.minimax(
                            not(turn), 
                            newState,  
                            depth-1, 
                            listMoves(state, self.other_player), 
                            self.alpha, 
                            self.beta, 
                            newPath
                        )
                        print(path, "!", value)
                        if (value > bestValue):
                            bestValue = value
                            bestPath = path

                        if time() > self.thinking_time:
                            return (bestPath, bestValue)

                        print("alpha", alpha)
                        self.alpha = max(self.alpha, bestValue)
                        if (self.alpha >= self.beta):
                            break

                best_movement = (bestPath, bestValue)
                return best_movement

            else: #(n_player != self.config.player_choice)
                bestValue = math.inf
                bestPath = None

                for cell in listCells:
                    newState = deepcopy(state)
                    posisi = place(newState, self.other_player, cell[1], cell[0])

                    if posisi != -1:
                        newPath = deepcopy(goalPath)
                        newPath.append((cell, newState))
                        
                        path, value = self.minimax(
                            not(turn), 
                            newState, 
                            depth-1, 
                            listMoves(state, self.n_player), 
                            self.alpha, 
                            self.beta, 
                            newPath
                        )
                        if (value < bestValue):
                            bestValue = value
                            bestPath = path

                        if time() > self.thinking_time:
                            return (bestPath, bestValue)

                        self.beta = min(self.beta, bestValue)
                        if (self.alpha >= self.beta):
                            break

                best_movement = (bestPath, bestValue)
                return best_movement
        

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.n_player = n_player
        if n_player == 0:
            self.other_player = 1
        else:
            self.other_player = 0

        bestPath, bestValue = self.minimax(
            True, state, 3, listMoves(state, self.n_player), -math.inf, math.inf
        )

        return bestPath[0][0]


