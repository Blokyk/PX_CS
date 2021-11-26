# I feel way better about my logger implementation in Parsex now that
# I've written this horrible piece of code :)

from math import ceil, floor
from typing import List

from game_board import SetupGameBoard

def __print_board_header(board: SetupGameBoard, label: str = '', end: str = '') -> None:
    if label == '':
        print('————'*board.columns_count + '—', end=end)
        return

    dash_count = (4*board.columns_count - (len(label) + 2))/2
    print('—' * floor(dash_count), end='')
    print(' ' + label + ' ', end='')
    print('—' * ceil(dash_count), end='')
    print('—', end=end)


def print_side_by_side_boards(boards: List[SetupGameBoard], labels: List[str] = []) -> None:
    """Prints a list of boards one next to each other

    Params:
        - labels (list[str]) -- a list of labels to put on the boards ; if the label is the
        empty string, no label will be put on that board
    """
    max_line = max(boards, key=lambda b: b.lines_count).lines_count

    def print_boards_separator() -> None:
        """Print the divider and space separating two boards"""
        print(' '*2 + '|' + ' '*2, end='')

    def print_headers(bs: List[SetupGameBoard], labels: List[str] = []) -> None:
        """Prints the headers for a list of boards and labels"""
        print_boards_separator()
        for (i, b) in enumerate(bs):
            __print_board_header(b, labels[i] if i < len(labels) else '')
            #if i != len(boards) - 1: # FIXME: this is incredibly ugly
            print_boards_separator()

    print_headers(boards, labels)

    print()
    for l in range(max_line):
        print_boards_separator()
        for (i, b) in enumerate(boards):
            if (l > b.lines_count):
                print(' '*4*b.columns_count, end='')
                continue
            print_board_line(b, l)
            #if i != len(boards) - 1: # FIXME: this is incredibly ugly
            print_boards_separator()
        print()
    print_headers(boards)
    print()

def print_board(board: SetupGameBoard) -> None:
    """Prints the given board"""
    col_count = board.columns_count
    __print_board_header(board, end = '\n')
    for i in range(board.lines_count):
        print_board_line(board, i)
        print()
    __print_board_header(board, end = '\n')

def print_board_line(board: SetupGameBoard, line_number: int) -> None:
    """Prints a given line from a board"""
    col_count = board.columns_count
    print('|', end='')
    for j in range(col_count):
        print(" " + board[line_number][j] + " ", end='|')

def get_ship_part_at(grid: SetupGameBoard, line: int, col: int) -> str:
    """Returns the ship at the given spot"""
    return grid[line][col]