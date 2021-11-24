
from typing import Dict, List, Tuple
from board_utils import print_board, print_side_by_side_boards
from game_board import GameBoard, InternalGameBoard

from ships import ShipPart, get_size
from utils import format_error, format_pos_and_angle, letter_to_idx

from random import randint, random

ship_types = ['P', 'C', 'R', 'S', 'T']

def init_board(column: int, rows: int) -> GameBoard:
    board = GameBoard()

    for line in range(column):
        board.append([]) # create empty line
        for _ in range(rows):
            board[line].append(ShipPart(' ')) # fill line with empty spaces

    return board

def input_position(board: GameBoard) -> List[int]:
    def decode(pos: str) -> List[int]:
        return [int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper())]

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

def mock_player_boards(boards: List[GameBoard]):
    for board in boards:
        for part in map(lambda l: ShipPart(l), ship_types):

            pos = [-1, -1]
            ori = "v"

            while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
                pos = [randint(0, 9), randint(0, 9)]
                ori = "v" if random() < 0.5 else "h"

            board.insert_ship_at(part, ori, pos[0], pos[1])
            print_board(board)

    return boards

def init_player_boards(boards: List[GameBoard]) -> List[GameBoard]:
    for board in boards:
        for part in map(lambda l: ShipPart(l), ship_types):
            print("Where do you want to put your" + str(part) + "(" + str(get_size(part)) + " spaces) ?")

            pos = input_position(board)
            ori = input_orientation()

            while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
                print("You can't put a ship there !", end='')

                if (board[pos[0]][pos[1]] != ' '):
                    print("There's already a" + str(board[pos[0]][pos[1]]) + "!", end='')

                print()

                pos = input_position(board)
                ori = input_orientation()

            board.insert_ship_at(part, ori, pos[0], pos[1])
            print_board(board)
            #print("Successfully inserted" + str(part) + "@ " + format_pos_and_angle(pos[0], pos[1], ori))
    return boards

def ship_type_is_sunk(part: str, board: InternalGameBoard, hitlist: InternalGameBoard) -> bool:
    counter = 0

    for ship in board.values():
        if ship == part and ship in hitlist:
            counter += 1

    print("Ship type " + part + " has been sunk " + str(counter))

    return counter == get_size(ShipPart(part))

def are_all_ships_sunk(board: InternalGameBoard, hitlist: InternalGameBoard) -> bool:
    for part in ship_types:
        if not ship_type_is_sunk(part, board, hitlist):
            return False

    return True

def act_player_turn(board: InternalGameBoard, hitlist: InternalGameBoard):
    print("Where do you want to hit next?")

    def input_position() -> List[int]:
        def decode(pos: str) -> List[int]:
            return [int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper())]

        output = input("Position (1-10, A-J) : [line] [column]\n\t")

        pos = decode(output)

        while not (len(output.split()) == 2 and 0 <= pos[0] < 10 and 0 <= pos[1] < 10):
            print(format_error('Invalid position'))
            output = input("Position (1-10, A-J) : [line] [column]\n\t")
            pos = decode(output)

        return pos

    (hit_line, hit_col) = input_position()

    # if the player hits twice the same spot, warn and ask them again
    while (hit_line, hit_col) in hitlist.keys():
        print(f"The ship part at ({hit_line},{hit_col}) has already been destroyed")

    if (hit_line, hit_col) in board.keys():
        print(f"HIT !")
        hitlist[(hit_line, hit_col)] = board[(hit_line, hit_col)]
    else:
        print(f"Miss... @ ({hit_line}, {hit_col})")
        print(board.keys())
