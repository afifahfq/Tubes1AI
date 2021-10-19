from os import stat
import random
from time import time

from src.model import Board, State
from src.constant import ShapeConstant, GameConstant
from src.utility import is_out

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

# Fungsi untuk mendapatkan value dan shape sebuah move
def calculate_value(state: State, n_player: int, row: int, col: int) -> Tuple[int, str]:
    board = state.board
    color = state.players[n_player].color

    check_order = [ShapeConstant.CROSS, ShapeConstant.CIRCLE, color]
    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    temp_value = -1
    temp_shape = state.players[n_player].shape

    for condition in check_order:
        if condition == ShapeConstant.CROSS:
            shape = ShapeConstant.CROSS

        elif condition == ShapeConstant.CIRCLE:
            shape = ShapeConstant.CIRCLE

        elif condition == color:
            shape = state.players[n_player].shape

        mark = 0
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(board, row_, col_):
                    if mark > temp_value:
                        temp_value = mark
                        temp_shape = shape
                    mark = 0
                    break

                shape_condition = (
                    (condition == ShapeConstant.CROSS or condition == ShapeConstant.CIRCLE)
                    and shape != board[row_, col_].shape
                )
                color_condition = (
                    condition == color
                    and color != board[row_, col_].color
                )
                if shape_condition or color_condition:
                    if mark > temp_value:
                        temp_value = mark
                        temp_shape = shape
                    mark = 0
                    break

                row_ += row_ax
                col_ += col_ax
                mark += 1
    return (temp_value, temp_shape)

# Fungsi untuk mendapatkan array value dan shape setiap successor
def make_value_array(state: State, n_player: int, succArray: List[int]):
    succ_value = []
    for col in range(len(succArray)):
        succ_value.append(calculate_value(state, n_player, succArray[col], col))
    
    return succ_value


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return None