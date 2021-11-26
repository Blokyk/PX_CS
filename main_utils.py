
from typing import Callable, List
from game_board import SetupGameBoard
from hid_utils import input_orientation, input_position
from player_types.ai import AIPlayer
from player_types.base import Player
from player_types.human import HumanPlayer
from player_types.mock import MockPlayer


from ships import get_size, ship_types
from utils import debug, format_error

from random import randint, random

def generate_random_board(lines: int, columns: int) -> SetupGameBoard:
    """Generates a game board with the given dimensions by choosing a random spot for each boat type"""
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
    """Generate game boards with the given dimensions using the `generator` function

    Params :
        - generator ((lines: int, cols: int) -> SetupGameBoard) -- The function used to generate
        the board with dimensions `lines` and `cols`
    """
    return [generator(lines, columns) for _ in range(number_of_boards)]

def init_board_from_user_input(lines: int, columns: int) -> SetupGameBoard:
    """Generate a game board with the given dimensions by asking the user for positions and orientations"""
    board = SetupGameBoard(lines, columns)
    for part in ship_types:
        print(f"Where do you want to put your {part} ({get_size(part)} spaces) ?")

        pos = input_position(board)
        ori = input_orientation()

        while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
            print(format_error("You can't put a ship there !"), end='')

            if (board[pos[0]][pos[1]] != ' '):
                print(format_error(f"There's already a {board[pos[0]][pos[1]]} !"), end='')

            print()

            pos = input_position(board)
            ori = input_orientation()

        board.insert_ship_at(part, ori, pos[0], pos[1])
        #debug("Successfully inserted" + str(part) + "@ " + format_pos_and_angle(pos[0], pos[1], ori))
    return board

def get_enemy_board_idx(player_idx: int) -> int:
    """get the index of the board that this player is attacking"""
    return (player_idx + 1) % 2

def get_player(player_num: int) -> Player:
    """Asks the user for the next player type (human, mock, or ai)
    """
    print(f"What type of player do you want P{player_num} to be ?\n\t- [h]uman\n\t- [r]andom/[m]ock\n\t- [a]i")

    is_player_type_valid = False
    output = Player()

    while not is_player_type_valid:

        answer = input("h/r/m/a : ").lower()

        # assume it's true, and only loop again if it's not valid (i.e. the else branch)
        is_player_type_valid = True

        if answer == "h" or answer == "human":
            output = HumanPlayer()
        elif answer in "rm" or answer == "random" or answer == "mock":
            output = MockPlayer()
        elif answer == "a" or answer == "ai":
            output = AIPlayer()
        else:
            is_player_type_valid = False

    return output