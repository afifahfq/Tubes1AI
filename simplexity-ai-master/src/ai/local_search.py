import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List

# Fungsi untuk mendapatkan row
def whereRow(state: State, col: int) -> int:
        for row in range(state.board.row - 1, -1, -1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return row

# Fungsi untuk mendapatkan array 7 suksesor
def makeArraySucc(state:State):
    succArray = []
    for col in range (7):
        succArray.append(whereRow(state,col))
    return succArray

class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return None