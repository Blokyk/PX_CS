
from typing import List
from board_utils import print_board, print_side_by_side_boards
from game_board import GameBoard

from ships import ShipPart, get_size
from utils import format_error, format_pos_and_angle, letter_to_idx

def init_board(column: int, rows: int) -> GameBoard:
    board = GameBoard()

    for line in range(column):
        board.append([]) # create empty line
        for _ in range(rows):
            board[line].append(ShipPart(' ')) # fill line with empty spaces

    return board

def enter_position(board: GameBoard) -> List[int]:
    def decode(pos: str) -> List[int]:
        return [int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper())]

    output = input("Position (1-10, A-J) : [line] [column]\n\t")

    pos = decode(output)

    while not (len(output.split()) == 2 and board.is_on_board(pos[0], pos[1])):
        print(format_error('Invalid position'))
        output = input("Position (1-10, A-J) : [line] [column]\n\t")
        pos = decode(output)

    return decode(output)

def enter_orientation() -> str:
    output = ''

    def is_valid_position_str(orientation: str):
        return orientation in ['H', 'V']

    while not is_valid_position_str(output := input("Orientation : H or V\n\t").upper()):
        print(format_error('Invalid orientation'))

    return output