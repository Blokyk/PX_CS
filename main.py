if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

import json
from os import path
from typing import List
from board_utils import board_to_internal, print_board, print_board_line, print_side_by_side_boards
from game_board import GameBoard, InternalGameBoard

from ships import ShipPart, get_size
from utils import format_error, format_pos_and_angle, letter_to_idx
from main_utils import *

boards = [init_board(10, 10), init_board(10, 10)]


# if path.exists("./boards.json"):
#     f = open("./boards.json", "r")
#     dic_list: List[InternalGameBoard] = json.loads(f.read())
#     for i in range(len(dic_list)):
#         for (line, col) in dic_list[i]:
#             boards[i][line][col] = ShipPart(dic_list[i][(line, col)])
# else:

boards = mock_player_boards(boards)

print_side_by_side_boards(boards)

dic_boards: List[InternalGameBoard] = []

for i in range(len(boards)):
    dic_boards.append(board_to_internal(boards[i]))

print(dic_boards)

# f = open("./boards.json", "w+")
# f.write(json.dumps(dic_boards))

isGameFinished = False

hitlists: List[InternalGameBoard] = [InternalGameBoard(), InternalGameBoard()]

sunk_types: List[str] = []

while not isGameFinished:
    enemy_board = dic_boards[1]
    enemy_hitlist = hitlists[1]

    act_player_turn(dic_boards[1], hitlists[1])

    print(hitlists)

    for part in set(ship_types).difference(sunk_types):
        if ship_type_is_sunk(part, dic_boards[1], hitlists[1]):
            print(f"Ship {part} has been sunk on P2's board !")
            sunk_types.append(part)
"""
    for i in range(len(dic_boards)):
        if are_all_ships_sunk(dic_boards[i], hitlists[i]):
            print(f"Player {i+1} lost !")
            isGameFinished = True
"""