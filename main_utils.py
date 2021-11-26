
from typing import Callable, Dict, List, Tuple
from board_setup_utils import print_board, print_side_by_side_boards
from game_board import SetupGameBoard, GameBoard


from ships import get_size, ship_types
from utils import debug, format_error, format_pos_and_angle, letter_to_idx

from random import randint, random

def input_(board: SetupGameBoard) -> Tuple[int, int]:
    def decode(pos: str) -> Tuple[int, int]:
        return (int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper()))

    output = input("Position (1-10, A-J) : [line] [column]\n\t")

    pos = decode(output)

    while not (len(output.split()) == 2 and board.is_on_board(pos[0], pos[1])):
        print(format_error('Invalid position'))
        output = input("Position (1-10, A-J) : [line] [column]\n\t")
        pos = decode(output)

    return decode(output)

def input_orientation() -> str:
    output = ''

    def is_valid_position_str(orientation: str):
        return orientation in ['H', 'V']

    while not is_valid_position_str(output := input("Orientation : H or V\n\t").upper()):
        print(format_error('Invalid orientation'))

    return output

def generate_random_board(lines: int, columns: int) -> SetupGameBoard:
    board = SetupGameBoard(lines, columns)
    for part in ship_types:

        pos = [-1, -1]
        ori = "v"

        while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
            pos = [randint(0, 9), randint(0, 9)]
            ori = "v" if random() < 0.5 else "h"

        board.insert_ship_at(part, ori, pos[0], pos[1])
    return board

def generate_boards(number_of_boards: int, lines: int, columns: int, generator: Callable[[int, int], SetupGameBoard]) -> List[SetupGameBoard]:
    return [generator(lines, columns) for _ in range(number_of_boards)]

def init_player_board(lines: int, columns: int) -> SetupGameBoard:
    board = SetupGameBoard(lines, columns)
    for part in ship_types:
        print(f"Where do you want to put your {part} ({get_size(part)} spaces) ?")

        pos = input_(board)
        ori = input_orientation()

        while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
            print(format_error("You can't put a ship there !"), end='')

            if (board[pos[0]][pos[1]] != ' '):
                print(format_error(f"There's already a {board[pos[0]][pos[1]]} !"), end='')

            print()

            pos = input_(board)
            ori = input_orientation()

        board.insert_ship_at(part, ori, pos[0], pos[1])
        #debug("Successfully inserted" + str(part) + "@ " + format_pos_and_angle(pos[0], pos[1], ori))
    return board

def get_enemy_board_idx(player_idx: int) -> int:
    return (player_idx + 1) % 2