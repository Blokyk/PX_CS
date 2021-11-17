from typing import List

from ships import ShipPart
from utils import letter_to_idx

from game_board import GameBoard

def print_board(board: GameBoard) -> None:
    for i in range(len(board)):
        print(board[i])

def get_ship_part_at(grid: GameBoard, line_letter: str, col: int) -> ShipPart:
    return grid[letter_to_idx(line_letter)][col]