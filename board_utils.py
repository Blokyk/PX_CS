from typing import List, Tuple

from game_board import SetupGameBoard, GameBoard

def board_to_internal(board: SetupGameBoard) -> GameBoard:
    """Converts a SetupGameBoard to the GameBoard type used internally"""
    output = GameBoard()

    for line in range(board.lines_count):
        for col in range(board.columns_count):
            if (board[line][col] != ' '):
                output[line, col] = board[line][col]

    return output

def internal_to_setup(board: GameBoard, lines: int = 10, columns: int = 10) -> SetupGameBoard:
    """Converts an internal GameBoard to a SetupGameBoard

    Params :
        - lines (int) & columns (int) -- optional dimensions for the game board.
        Set to 10 by default.
    """
    output = SetupGameBoard(lines, columns)

    for ((line, col), ship) in board.items():
        output[line][col] = ship

    return output

def is_on_board(hit: Tuple[int, int], lines: int = 10, cols: int = 10) -> bool:
    """Checks if a position is on the board

    Params :
        - lines (int) & columns (int) -- optional dimensions for the game board.
        Set to 10 by default.
    """
    return 0 <= hit[0] < lines and 0 <= hit[1] < cols

def does_attack_hit(board: GameBoard, hit: Tuple[int, int]) -> bool:
    return hit in board.keys()

def get_hit_result(board: GameBoard, hit: Tuple[int, int]) -> str:
    return board[hit] if does_attack_hit(board, hit) else " "