from random import randint
from typing import List, Tuple

from board_utils import is_on_board
from game_board import GameBoard
from ships import get_size
from player_types.base import Player

from utils import debug



def gen_diagonal_for_size(min_boat_size: int, board_size: int) -> List[Tuple[int, int]]:
    """Generates the optimal pattern for a ship of size `min_size` and a board of `board_size`
    """
    output = []

    for line in range(board_size):
        for col_multiplier in range(board_size):
            if ((line % min_boat_size) + col_multiplier * min_boat_size >= board_size):
                break
            output.append((line, (line % min_boat_size) + col_multiplier * min_boat_size))

    return output

class AIPlayer(Player):
    """An player interface for an artificial intelligence"""

    pattern_quadrants: List[List[Tuple[int, int]]]
    """Lists of optimal spots to try, depending on the minimum size"""

    max_boat_size: int
    """The biggest boat left"""

    targets_stack: List[Tuple[int, int]]
    """Stack/list of targets spots to attack"""

    def __init__(self) -> None:
        self.max_boat_size = 5
        self.targets_stack = []

        self.pattern_quadrants = [gen_diagonal_for_size(i, 10) for i in range(1, 6)]

    def get_next_action(self) -> Tuple[int, int]:
        quadrant_idx = self.max_boat_size - 1

        def get_next_spot() -> Tuple[int, int]:
            """Returns the next spot the AI will strike :
                - Normally, it will one of the random optimal spots from pattern_quadrants
                - In 'target mode', it will select one of the four spots right next to it
            """
            quadrant_idx = self.max_boat_size - 1

            if len(self.targets_stack) != 0:
                debug(self.targets_stack)
                return self.targets_stack.pop(-1)
            else:
                # Occasionally, we'll have broken the pattern because of target mode,
                # so we need to scale it down
                if len(self.pattern_quadrants[quadrant_idx]) == 0:
                    self.max_boat_size -= 1
                    return get_next_spot()
                rnd = randint(0, len(self.pattern_quadrants[quadrant_idx]) - 1)
                return self.pattern_quadrants[quadrant_idx][rnd]

        next_spot = get_next_spot()

        # If it comes from pattern_quadrants, we remove it :
        #    a) to avoid picking it again later
        #
        #    b) because that way we can detect when we've exhausted optimal spots and need
        #       to reduce the minimum size for ships
        if next_spot in self.pattern_quadrants[quadrant_idx]:
            self.pattern_quadrants[quadrant_idx].remove(next_spot)

        return next_spot

    # These functions could be integrated directly into get_next_ai_turn by passing it
    # the board, but :
    #   A.  The AI would then have more knowledge than the player, and we might use the info
    #       on the board without realizing it
    #
    #   B.  (kind of) Separation of concerns : We can just use the interface provided instead
    #       and abstract over some of the implementation of the board
    def react_hit_success(self, tried_list: GameBoard, hit: Tuple[int, int]):
        if len(self.targets_stack) == 0:
            debug("Switched to target mode !")

        (hit_line, hit_col) = hit

        temp_targets = [
                                    (hit_line-1, hit_col),
            (hit_line, hit_col-1),                        (hit_line, hit_col+1),
                                    (hit_line+1, hit_col)]

        for target in temp_targets:
            # If this is a valid target, add it to the stack
            if target not in tried_list and target not in self.targets_stack and is_on_board(target):
                self.targets_stack.append(target)

    def react_hit_sunk(self, tried_list: GameBoard, hit: Tuple[int, int], ship_type: str):
        debug(f"AI actually managed to sink a {ship_type}-type ship !")

        if self.max_boat_size == get_size(ship_type):
            self.max_boat_size -= 1
