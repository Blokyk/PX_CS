if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

import json
from os import path
from typing import Any, Callable, List
from board_setup_utils import internal_to_setup, print_board, print_board_line, print_side_by_side_boards
from board_utils import board_to_internal, does_attack_hit
from game_board import SetupGameBoard, GameBoard

from ships import get_size
from utils import format_error, format_pos_and_angle, letter_to_idx
from main_utils import *
import ai

boards = [SetupGameBoard(10, 10), SetupGameBoard(10, 10)]

boards = mock_player_boards(boards)

print_side_by_side_boards(boards, ["P1", "P2"])

internal_boards: List[GameBoard] = []

for i in range(len(boards)):
    internal_boards.append(board_to_internal(boards[i]))

# We have to invert the boards, because internal_boards[0] corresponds to the
# board **attacked** by P1, and internal_boards[1] is **attacked** by P2

internal_boards.reverse()

isGameFinished = False

tried_lists: List[GameBoard] = [GameBoard(), GameBoard()]

sunk_types: List[str] = []

round_count = 0

p1 = ai.AIPlayer()
p2 = ai.AIPlayer()

while not isGameFinished:

    round_count += 1
    print(f"ROUND {round_count}")

    def check_player_hit(idx: int, hit: Tuple[int, int], hit_handler: Any, sink_handler: Any) -> bool:
        success = does_attack_hit(internal_boards[idx], hit)
        tried_lists[idx][hit] = internal_boards[idx][hit] if success else "~"

        if success:
            print(f"P{idx+1} : HIT @ {hit}")
            for part in set(ship_types).difference(sunk_types):
                if ship_type_is_sunk(part, internal_boards[idx], tried_lists[idx]):
                    print(f"Ship {part} has been sunk on P{(idx+1)*2 % 3}'s board !")
                    sunk_types.append(part)
                    sink_handler(internal_boards[idx], tried_lists[idx], hit, internal_boards[idx][hit])
                    return True

            # if we got here, that means that we didn't sink any ship
            hit_handler(internal_boards[idx], tried_lists[idx], hit)
        else:
            print(f"P{idx+1} : Miss @ {hit}")

        return success

    def do_nothing_hit(board: GameBoard, tried_list: GameBoard, hit: Tuple[int, int, int]):
        pass
    def do_nothing_sunk(board: GameBoard, tried_list: GameBoard, hit: Tuple[int, int, int], ship_type: str):
        pass

    p1_success = check_player_hit(0, ask_for_player_turn(internal_boards[0], tried_lists[0]), p1.react_hit_success, p1.react_hit_sunk)
    p2_success = check_player_hit(1, p2.get_next_ai_turn(internal_boards[1], tried_lists[1]), p2.react_hit_success, p2.react_hit_sunk)

    # If any of them hit, check if any of the bords are lost
    if p1_success or p2_success:
        for i in range(len(internal_boards)):
            if are_all_ships_sunk(internal_boards[i], tried_lists[i]):
                print(f"Player {(i+1)*2 % 3} lost !")
                isGameFinished = True

    print_side_by_side_boards([internal_to_setup(internal_boards[0]), internal_to_setup(internal_boards[1])], ["P1", "P2"])
    print()
    print("—"*41 + " V S " + "—"*41)
    print()
    print_side_by_side_boards([internal_to_setup(tried_lists[0]), internal_to_setup(tried_lists[1])], ["P2's pov of P1", "p1's pov of P2"])

print(f"GAME DONE IN {round_count} ROUNDS !")