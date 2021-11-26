from typing import Tuple
from random import randint

from game_board import GameBoard
from player_types.base import Player

from utils import format_error, letter_to_idx

class RandomPlayer(Player):

    def get_next_action(self, tried_list: GameBoard):
        # If we hit an invalid spot, just try again
        while (hit := (randint(0, 9), randint(0, 9))) in tried_list.keys():
            continue

        return hit