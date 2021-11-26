if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

from typing import Callable, List, Tuple

from board_setup_utils import print_side_by_side_boards
from board_utils import board_to_internal, does_attack_hit, internal_to_setup
from game_board import GameBoard

from player_types import human

from main_utils import *







boards = []

players = [get_player(1), get_player(2)]

for (i, p) in enumerate(players):
    if p.__class__ == human.HumanPlayer:
        boards.append(init_board_from_user_input(10, 10))
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

    def check_player_hit(idx: int, hit: Tuple[int, int], hit_handler: Callable[[GameBoard, Tuple[int, int]], None], sink_handler: Callable[[GameBoard, Tuple[int, int], str], None]) -> bool:
        """

        Params :
            - idx (int) --
            - hit (Tuple[int, int]) --
            - hit_handler --
            - sink_handler --
        """

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
        print('  ' + '—'*43 + f"( P{i+1} )" + '—'*44) # total width of side-by-side boards is 86
        print_side_by_side_boards([internal_to_setup(internal_boards[-i]), internal_to_setup(tried_lists[-i])], [f"P{i+1}'s board", f"P{i+1}'s hits"])
        print()

        next_spot = player.get_next_action()

        while next_spot in tried_lists[i].keys():
            next_spot = player.get_next_action()
            player.react_already_tried(next_spot)

        res = check_player_hit(
            i,
            next_spot,
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
            if not isGameFinished and internal_boards[get_enemy_board_idx(i)].are_all_ships_sunk(tried_lists[-i]):
                print(f"Player {(i+1)*2 % 3} lost !")
                isGameFinished = True

print(f"Game done in {round_count} rounds !")