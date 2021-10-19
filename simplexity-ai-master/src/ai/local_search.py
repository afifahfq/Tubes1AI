import random
from time import time

from src.constant import ShapeConstant, ColorConstant, GameConstant

from src.model import State
from src.utility import is_out


from typing import Tuple, List

def whereRow(state: State, col: int) -> int:
        for row in range(state.board.row - 1, -1, -1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return row
        return -1

def makeArraySucc(state:State):
    succArray = []
    for col in range (7):
        succArray.append(whereRow(state,col))
    return succArray

def calculate_value(state: State, n_player: int, row: int, col: int) -> Tuple[int, str]:
    board = state.board
    if (n_player == 0):
        our_shape = ShapeConstant.CIRCLE
        our_color = ColorConstant.RED
        enemy_shape = ShapeConstant.CROSS
    else:
        our_shape = ShapeConstant.CROSS
        our_color = ColorConstant.BLUE
        enemy_shape = ShapeConstant.CIRCLE
        

    check_order = [ShapeConstant.CROSS, ShapeConstant.CIRCLE, ColorConstant.BLUE, ColorConstant.RED]
    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    temp_value = -1
    temp_shape = state.players[n_player].shape

    for condition in check_order:
        if (condition == ShapeConstant.CROSS):
            shape = ShapeConstant.CROSS
            color = our_color

        elif (condition == ShapeConstant.CIRCLE):
            shape = ShapeConstant.CIRCLE
            color = our_color

        elif (condition == ColorConstant.RED):
            shape = random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])
            color = ColorConstant.RED

        elif (condition == ColorConstant.BLUE):
            shape = random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])
            color = ColorConstant.BLUE

        mark = 0
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(board, row_, col_):
                    if mark > temp_value:
                        if (condition == ShapeConstant.CROSS or condition == ShapeConstant.CIRCLE):
                            temp_value = mark
                            temp_shape = our_shape
                        elif (condition == ColorConstant.RED or condition == ColorConstant.BLUE):
                            temp_value = mark
                            temp_shape = enemy_shape
                    mark = 0
                    break

                shape_condition = (
                    (condition == ShapeConstant.CROSS or condition == ShapeConstant.CIRCLE)
                    and shape != board[row_, col_].shape
                )
                color_condition = (
                    (condition == ColorConstant.RED or condition == ColorConstant.BLUE)
                    and color != board[row_, col_].color
                )
                if shape_condition:
                    if (mark > temp_value):
                        temp_value = mark
                        temp_shape = our_shape
                    mark = 0
                    break
                elif color_condition:
                    if (mark > temp_value):
                        temp_value = mark
                        temp_shape = enemy_shape
                    mark = 0
                    break

                row_ += row_ax
                col_ += col_ax
                mark += 1
    return (temp_value, temp_shape)

def bestChoice(state:State,n_player: int):
    default = -1
    succ = makeArraySucc(state)
    someChoices = []
    for col in range(7):
        if (succ[col] == -1):
            continue
        choices = calculate_value(state,n_player,succ[col],col)
        if (state.players[n_player].quota[choices[1]] == 0):
            if (choices[1] == ShapeConstant.CROSS):
                choices = (choices[0], ShapeConstant.CIRCLE)
            else:
                choices = choices[0], ShapeConstant.CROSS
        if (default <= choices[0]):
            if (default < choices[0]):
                someChoices = []
            default = choices[0]
            someChoices.append((col, choices[1]))
    return random.choice(someChoices)



class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = bestChoice(state,n_player)

        return best_movement
