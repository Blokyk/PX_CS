from typing import Tuple
from game_board import GameBoard
from player_types.base import Player

from utils import format_error, letter_to_idx

class HumanPlayer(Player):
    def __input_attack_(self) -> Tuple[int, int]:
        def decode(pos: str) -> Tuple[int, int]:
            return (int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper()))

        output = input("Position (1-10, A-J) : [line] [column]\n\t")

        pos = decode(output)

        while not (len(output.split()) == 2 and 0 <= pos[0] < 10 and 0 <= pos[1] < 10):
            print(format_error('Invalid position'))
            output = input("Position (1-10, A-J) : [line] [column]\n\t")
            pos = decode(output)

        return pos

    def get_next_action(self, tried_list: GameBoard):
        print("Where do you want to hit next?")

        hit = self.__input_attack_()

        # if the player hits twice the same spot, warn and ask them again
        while hit in tried_list.keys():
            print(format_error(f"The ship part at {hit} has already been destroyed"))
            hit = self.__input_attack_()

        return hit