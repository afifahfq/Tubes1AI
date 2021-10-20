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

from src import *
from src.utility import *
from src.model import State, Config
from src.ai import *

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
        pass

    def checkStreak(self, board: Board, row: int, col: int, shape: str, color: str, foundShape: int, foundColor: int, streakTuple: List[Tuple[int, int]]):
        cell = board[row, col]
        for i, j in streakTuple:
            newrow = row + i
            newcol = col + j

            newfoundColor = 0
            newfoundShape = 0
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(board, newrow, newcol):
                    break

                if cell.shape == board[newrow, newcol].shape:
                    newfoundShape += 1
                if cell.color == board[newrow, newcol].color:
                    newfoundColor += 1
            foundShape += (newfoundShape ** 2)
            foundColor += (newfoundColor ** 2)

        return foundShape, foundColor

    def count_streak(self, board: Board, shape: str, color: str, foundShape: int, foundColor: int):
        streakTuple = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for i in range(board.row):
            for j in range(board.col):
                countShape, countColor = self.checkStreak(board, i, j, shape, color, 0, 0, streakTuple)
                foundShape += countShape
                foundColor += countColor
        return foundShape, foundColor
    
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

    def getPoint(self, state: State, winner: Tuple[str, str], player: Player, enemy: Player):
        if winner != None:
            if winner[0] == player.shape and winner[1] == player.color:
                return 100
            else:
                return -100

        playerPoint = sum(self.count_streak(state.board, player.shape, player.color, 0, 0))
        enemyPoint = sum(self.count_streak(state.board, enemy.shape, enemy.color, 0, 0))

        score = playerPoint - enemyPoint
        if score == 0:
            score = random.uniform(0, 2)

        return score

    def listMoves(self, state: State, n_player):
        quota = state.players[n_player].quota
        listMoves = []

        for key, value in quota.items():
            if (value == 0):
                continue

            for col in range(state.board.col):
                listMoves.append((col, key))
        return listMoves

    def minimax(self, turn: bool, state: State, depth: int, listCells: List[int], alpha: float, beta: float, goalPath: List[State] = []) -> float:
        if (depth == 0 or is_win(state.board) == True or is_full(state.board) == True):
            return goalPath, self.getPoint(state, is_win(state.board), state.players[self.n_player], state.players[self.other_player])

        else:
            if (turn):
                bestValue = float("-inf")
                bestPath = None

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
                            self.listMoves(state, self.other_player), 
                            alpha, 
                            beta, 
                            newPath,
                        )
                        if (value > bestValue):
                            bestValue = value
                            bestPath = path

                        if time() > self.thinking_time:
                            return (bestPath, bestValue)

                        alpha = max(alpha, bestValue)
                        if (alpha >= beta):
                            break

                best_movement = (bestPath, bestValue)
                return best_movement

            else: #(n_player != self.config.player_choice)
                bestValue = float("inf")
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
                            self.listMoves(state, self.n_player), 
                            alpha, 
                            beta, 
                            newPath,
                        )
                        if (value < bestValue):
                            bestValue = value
                            bestPath = path

                        if time() > self.thinking_time:
                            return (bestPath, bestValue)

                        beta = min(beta, bestValue)
                        if (alpha >= beta):
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
            True, state, 3, self.listMoves(state, self.n_player), float("-inf"), float("inf")
        )

        return bestPath[0][0]


