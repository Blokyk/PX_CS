from typing import List, Tuple

from game_board import SetupGameBoard, GameBoard

def board_to_internal(board: SetupGameBoard) -> GameBoard:
    output = GameBoard()

    for line in range(board.lines_count):
        for col in range(board.columns_count):
            if (board[line][col] != ' '):
                output[(line, col)] = board[line][col]

    return output

def is_on_board(hit: Tuple[int, int]) -> bool:
    # fuck extensibility
    return 0 <= hit[0] < 10 and 0 <= hit[1] < 10

def does_attack_hit(board: GameBoard, hit: Tuple[int, int]) -> bool:
    return hit in board.keys()

def hit_result(board: GameBoard, hit: Tuple[int, int]) -> str:
    return board[hit] if does_attack_hit(board, hit) else " "