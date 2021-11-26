from typing import Tuple

from game_board import GameBoard

class Player():
    """Base class for all types of players
    """

    def __init__(self) -> None:
        pass # probably should be NotImplemented() but who cares :shrug:

    def get_next_action(self) -> Tuple[int, int]:
        """Query the player for the next turn/action
        """
        raise NotImplementedError()

    def react_hit_success(self, tried_list: GameBoard, hit: Tuple[int, int]):
        """Notifies the player it hit something
        """
        return

    def react_hit_sunk(self, tried_list: GameBoard, hit: Tuple[int, int], ship_type: str):
        """Notifies the player it sunk a ship

        Params :
            - ship_type (str) -- The type of ship that was sunk

        """
        return

    def react_already_tried(self, hit: Tuple[int, int]):
        """Notifies the player it already tried this spot
        """
        return