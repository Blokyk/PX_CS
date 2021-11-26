from typing import Tuple
from game_board import SetupGameBoard

from utils import format_error, letter_to_idx

def input_position(board: SetupGameBoard) -> Tuple[int, int]:
    """Asks the user for a position. The position returned will always be valid
    """
    def to_pos(pos: str) -> Tuple[int, int]:
        parts = pos.split(' ')

        if not (str.isnumeric(parts[0]) and len(parts[1]) == 1 and parts[1].upper() in "ABCDEFGHIJ"):
            return (-1, -1)

        return (int(parts[0]) - 1, letter_to_idx(parts[1].upper()))

    output = input("Position (1-10, A-J) : [line] [column]\n\t")

    pos = to_pos(output)

    while not (len(output.split()) == 2 and board.is_on_board(pos[0], pos[1])):
        print(format_error('Invalid position'))
        output = input("Position (1-10, A-J) : [line] [column]\n\t")
        pos = to_pos(output)

    return to_pos(output)

def input_orientation() -> str:
    """Asks the user for a ship orientation ([h]orizontal or [v]ertical).
    The orientation returned will always be valid"""
    output = ''

    def is_valid_position_str(orientation: str):
        return orientation in ['H', 'V']

    while not is_valid_position_str(output := input("Orientation : H or V\n\t").upper()):
        print(format_error('Invalid orientation'))

    return output