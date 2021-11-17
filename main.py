from typing import List
from board_utils import print_board
from game_board import GameBoard

from ships import ShipPart

boards = [[], []]

def init_board(column: int, rows: int) -> GameBoard:
    board = GameBoard()

    for line in range(column):
        board.append([]) # create empty line
        for _ in range(rows):
            board[line].append(ShipPart(' ')) # fill line with empty spaces

    return board

if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

boards[0] = init_board(10, 10)
boards[1] = init_board(10, 10)

#boards[0].put_at(ShipPart('S'), 'H', 'D', 2) # FIXME: 2 is an idx, not a number

def enter_position() -> List[int]:
    output = ''

    def is_valid_position_str(pos: str):
        return len(pos.split(' ')) == 2

    while not is_valid_position_str(output := input("Position : [line] [column]")):
        print('Invalid position !')

    return [int(output.split(' ')[0]), int(output.split(' ')[1])]

def enter_orientation() -> str:
    output = ''

    def is_valid_position_str(orientation: str):
        return orientation in ['H', 'V']

    while not is_valid_position_str(output := input("Orientation : H or V")):
        print('Invalid orientation !')

    return output

print_board(boards[0])
print_board(boards[1])