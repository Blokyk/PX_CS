# I feel way better about my logger implementation in Parsex now that
# I've written this horrible piece of code :)

from typing import List

from utils import letter_to_idx

from game_board import SetupGameBoard, GameBoard

def __print_board_header(board: SetupGameBoard, end: str = '') -> None:
        print('————'*board.columns_count + '—', end=end)

def print_side_by_side_boards(boards: List[SetupGameBoard]) -> None:
    max_line = max(boards, key=lambda b: b.lines_count).lines_count

    def print_boards_separator() -> None:
        print(' '*2 + '|' + ' '*2, end='')

    def print_headers(bs: List[SetupGameBoard]) -> None:
        for (i, b) in enumerate(bs):
            __print_board_header(b)
            if i != len(boards) - 1: # FIXME: this is incredibly ugly
                print_boards_separator()

    print_headers(boards)

    print()
    for l in range(max_line):
        for (i, b) in enumerate(boards):
            if (l > b.lines_count):
                print(' '*4*b.columns_count, end='')
                continue
            print_board_line(b, l)
            if i != len(boards) - 1: # FIXME: this is incredibly ugly
                print_boards_separator()
        print()
    print_headers(boards)
    print()

def print_board(board: SetupGameBoard) -> None:
    col_count = board.columns_count
    __print_board_header(board, end = '\n')
    for i in range(board.lines_count):
        print_board_line(board, i)
        print()
    __print_board_header(board, end = '\n')

def print_board_line(board: SetupGameBoard, idx: int) -> None:
    col_count = board.columns_count
    print('|', end='')
    for j in range(col_count):
        print(" " + board[idx][j] + " ", end='|')

def get_ship_part_at(grid: SetupGameBoard, line: int, col: int) -> str:
    return grid[line][col]

def internal_to_setup(board: GameBoard) -> SetupGameBoard:
    output = SetupGameBoard(10, 10)

    for ((line, col), ship) in board.items():
        output[line][col] = ship

    return output