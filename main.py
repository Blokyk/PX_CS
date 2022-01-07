from typing import List
from typing_utils import T, GameBoard

import tui

def init_matrix(columns: int, rows: int, default: T) -> List[List[T]]:
    return [[default]*columns for i in range(rows)]

def create_game_board() -> GameBoard:
    return init_matrix(8, 8, '    ')

def populate_game_board(board: GameBoard) -> GameBoard:
    first_line  = ['T1', 'C1', 'F1', 'RE', 'RO', 'F2', 'C2', 'T2']
    second_line = [ 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']

    for i, p in enumerate(first_line):
        board[0][i] = p + "_N"
        board[-1][i] = p + "_B"

    for i, p in enumerate(second_line):
        board[1][i] = p + "_N"
        board[-2][i] = p + "_B"

    return board

board = populate_game_board(create_game_board())

tui.print_game_board(board)