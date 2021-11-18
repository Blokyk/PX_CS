from typing import List

from ships import ShipPart
from utils import letter_to_idx

from game_board import GameBoard

# I feel way better about my logger implementation in Parsex now that
# I've written this shit piece of code :)

def __print_board_header(board: GameBoard) -> None:
        print('————'*board.get_columns_count() + '—', end='')

def print_side_by_side_boards(boards: List[GameBoard]) -> None:
    max_line = max(boards, key=lambda b: b.lines_count).lines_count

    def print_boards_separetor() -> None:
        print(' '*2 + '|' + ' '*2, end='')

    def print_headers(bs: List[GameBoard]) -> None:
        for (i, b) in enumerate(bs):
            __print_board_header(b)
            if i != len(boards) - 1:
                print_boards_separetor()

    print_headers(boards)

    print()
    for l in range(max_line):
        for (i, b) in enumerate(boards):
            if (l > b.lines_count):
                print(' '*4*b.get_columns_count(), end='')
                continue
            print_board_line(b, l)
            if i != len(boards) - 1:
                print_boards_separetor()
        print()
    print_headers(boards)
    print()

def print_board(board: GameBoard) -> None:
    col_count = board.get_columns_count()
    for i in range(board.lines_count):
        print('————'*col_count + '—')
        print_board_line(board, i)
        print()
    print('————'*board.get_columns_count() + '—')

def print_board_line(board: GameBoard, idx: int) -> None:
    col_count = board.get_columns_count()
    print('|', end='')
    for j in range(col_count):
        print(board[idx][j], end='|')

def get_ship_part_at(grid: GameBoard, line: int, col: int) -> ShipPart:
    return grid[line][col]