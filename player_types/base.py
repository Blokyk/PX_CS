from typing import Tuple
from game_board import GameBoard
from utils import format_error, letter_to_idx

class Player():
    def __init__(self) -> None:
        pass # probably should be NotImplemented() but who cares :shrug:

    def get_next_action(self, tried_list: GameBoard):
        """Ask the player for the next turn/action"""
        raise NotImplementedError()

    def react_hit_success(self, tried_list: GameBoard, hit: Tuple[int, int]):
        return

    def react_hit_sunk(self, tried_list: GameBoard, hit: Tuple[int, int], ship_type: str):
        return