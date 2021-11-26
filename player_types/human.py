from typing import Tuple

from game_board import SetupGameBoard
from hid_utils import input_position
from player_types.base import Player

from utils import format_error

class HumanPlayer(Player):
    """ """

    def get_next_action(self):
        print("Where do you want to hit next?")

        hit = input_position(SetupGameBoard(10, 10))

        return hit

    def react_already_tried(self, hit: Tuple[int, int]):
        print(format_error(f"You already tried {hit}"))