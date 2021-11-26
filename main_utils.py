
from typing import Dict, List, Tuple
from board_setup_utils import print_board, print_side_by_side_boards
from game_board import SetupGameBoard, GameBoard

from ships import get_size
from utils import format_error, format_pos_and_angle, letter_to_idx

from random import randint, random

ship_types = ['P', 'C', 'R', 'S', 'T']

def input_position(board: SetupGameBoard) -> Tuple[int, int]:
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

def mock_player_boards(boards: List[SetupGameBoard]):
    for board in boards:
        for part in ship_types:

            pos = [-1, -1]
            ori = "v"

            while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
                pos = [randint(0, 9), randint(0, 9)]
                ori = "v" if random() < 0.5 else "h"

            board.insert_ship_at(part, ori, pos[0], pos[1])

    return boards

def init_player_boards(boards: List[SetupGameBoard]) -> List[SetupGameBoard]:
    for board in boards:
        for part in ship_types:
            print("Where do you want to put your" + str(part) + "(" + str(get_size(part)) + " spaces) ?")

            pos = input_position(board)
            ori = input_orientation()

            while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
                print(format_error("You can't put a ship there !"), end='')

                if (board[pos[0]][pos[1]] != ' '):
                    print(format_error("There's already a" + str(board[pos[0]][pos[1]]) + "!"), end='')

                print()

                pos = input_position(board)
                ori = input_orientation()

            board.insert_ship_at(part, ori, pos[0], pos[1])
            print_board(board)
            #debug("Successfully inserted" + str(part) + "@ " + format_pos_and_angle(pos[0], pos[1], ori))
    return boards

def ship_type_is_sunk(part: str, board: GameBoard, tried_list: GameBoard) -> bool:
    counter = 0

    for (coords, ship) in board.items():
        if ship == part and (coords, ship) in tried_list.items():
            counter += 1

    #debug("Ship type " + part + " has been sunk " + str(counter))

    return counter == get_size(part)

def are_all_ships_sunk(board: GameBoard, tried_list: GameBoard) -> bool:
    for part in ship_types:
        if not ship_type_is_sunk(part, board, tried_list):
            return False

    return True

def mock_player_turn(board: GameBoard, tried_list: GameBoard) -> Tuple[int, int]:
    def input_attack_position() -> Tuple[int, int]:
        return (randint(0, 9), randint(0, 9))

    hit = input_attack_position()

    # if the player hits twice the same spot, warn and ask them again
    while hit in tried_list.keys():
        hit = input_attack_position()

    return hit


def ask_for_player_turn(board: GameBoard, tried_list: GameBoard) -> Tuple[int, int]:

    print("Where do you want to hit next?")

    def input_attack_position() -> Tuple[int, int]:
        def decode(pos: str) -> Tuple[int, int]:
            return (int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper()))

        output = input("Position (1-10, A-J) : [line] [column]\n\t")

        pos = decode(output)

        while not (len(output.split()) == 2 and 0 <= pos[0] < 10 and 0 <= pos[1] < 10):
            print(format_error('Invalid position'))
            output = input("Position (1-10, A-J) : [line] [column]\n\t")
            pos = decode(output)

        return pos

    hit = input_attack_position()

    # if the player hits twice the same spot, warn and ask them again
    while hit in tried_list.keys():
        print(f"The ship part at {hit} has already been destroyed")
        hit = input_attack_position()

    return hit
