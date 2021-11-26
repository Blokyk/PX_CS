if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

import json
from os import path
from typing import Any, Callable, List
from board_setup_utils import internal_to_setup, print_board, print_board_line, print_side_by_side_boards
from board_utils import board_to_internal, does_attack_hit, hit_result
from game_board import SetupGameBoard, GameBoard


from ships import get_size
from utils import format_error, format_pos_and_angle, letter_to_idx
from main_utils import *
from player_types import ai, base, human, mock

boards = []

def get_player(num: int) -> base.Player:
    print(f"What type of player do you want P{num} to be ?\n\t- [h]uman\n\t- [r]andom/[m]ock\n\t- [a]i")

    is_player_type_valid = False
    output = base.Player()

    while not is_player_type_valid:

        answer = input("h/r/m/a : ").lower()

        # assume it's true, and only loop again if it's not valid (i.e. the else branch)
        is_player_type_valid = True

        if answer == "h" or answer == "human":
            output = human.HumanPlayer()
        elif answer in "rm" or answer == "random" or answer == "mock":
            output = mock.RandomPlayer()
        elif answer == "a" or answer == "ai":
            output = ai.AIPlayer()
        else:
            is_player_type_valid = False

    return output

players = [get_player(1), get_player(2)]

for (i, p) in enumerate(players):
    if p.__class__ == human.HumanPlayer:
        boards.append(init_player_board(10, 10))
    else:
        boards.append(generate_random_board(10, 10))

print_side_by_side_boards(boards, ["P" + str(i+1) for i in range(0, len(boards))])

internal_boards: List[GameBoard] = []

for i in range(len(boards)):
    internal_boards.append(board_to_internal(boards[i]))

# We have to invert the boards, because internal_boards[0] corresponds to the
# board **attacked** by P1, and internal_boards[1] is **attacked** by P2

internal_boards.reverse()

isGameFinished = False

tried_lists: List[GameBoard] = [GameBoard() for _ in range(len(players))]

sunk_types: List[str] = []

round_count = 0

while not isGameFinished:
    round_count += 1
    print(f"ROUND {round_count}")

    def check_player_hit(idx: int, hit: Tuple[int, int], hit_handler: Any, sink_handler: Any) -> bool:
        board_idx = get_enemy_board_idx(idx)
        success = does_attack_hit(internal_boards[board_idx], hit)
        tried_lists[idx][hit] = internal_boards[board_idx][hit] if success else "~"

        if success:
            print(f"P{idx+1} : HIT @ {hit}")
            for part in set(ship_types).difference(sunk_types):
                if internal_boards[board_idx].ship_type_is_sunk(part, tried_lists[idx]):
                    print(f"P{idx+1} sunk a {part} ship on P{(idx+1)*2 % 3}'s board !")
                    sunk_types.append(part)
                    sink_handler(tried_lists[idx], hit, internal_boards[board_idx][hit])
                    return True

            # if we got here, that means that we didn't sink any ship
            hit_handler(tried_lists[idx], hit)
        else:
            print(f"P{idx+1} : Miss @ {hit}")

        return success

    any_success = False

    for (i, player) in enumerate(players):
        print()
        print("—"*8 + f"( P{i+1} )" + "—"*72)
        print()
        print_side_by_side_boards([internal_to_setup(internal_boards[-i]), internal_to_setup(tried_lists[-i])], [f"P{i+1}'s board", f"P{i+1}'s hits"])
        print()
        res = check_player_hit(
            i,
            player.get_next_action(tried_lists[i]),
            player.react_hit_success,
            player.react_hit_sunk
        )

        if res:
            any_success = True

    print()
    print()

    # If any of them hit, check if any of the bords are lost
    if any_success:
        for i in range(len(internal_boards)):
            # Yes, while testing i had a game where both AIs won and lost at the same time... 54 rounds if you're wondering
            if not isGameFinished and internal_boards[get_enemy_board_idx(i)].are_all_ships_sunk(tried_lists[i]):
                print(f"Player {(i+1)*2 % 3} lost !")
                isGameFinished = True

    # print_side_by_side_boards([internal_to_setup(internal_boards[i]) for i in range(len(internal_boards))], [f"P{i+1}" for i in range(len(players))])
    # print()
    # print("—"*41 + " V S " + "—"*41)
    # print()
    # print_side_by_side_boards([internal_to_setup(tried_lists[i]) for i in range(len(tried_lists))], [f"P{i+1}'s POV" for i in range(len(players))])

print(f"Game done in {round_count} rounds !")