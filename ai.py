from random import Random, randint, random
from typing import Deque, List, Tuple
from board_utils import does_attack_hit, is_on_board, hit_result

from game_board import GameBoard
from ships import get_size
from utils import debug

def gen_diagonal_for_size(min_size: int, board_size: int) -> List[Tuple[int, int]]:
    output = []

    for line in range(board_size):
        for col_multiplier in range(board_size):
            if ((line % min_size) + col_multiplier * min_size >= board_size):
                break
            output.append((line, (line % min_size) + col_multiplier * min_size))

    return output

class AIPlayer():
    # Using only sizes 2 and 4 is a good compromise between accuracy and speed : if it was
    # too high we would probably miss a lot of ships ; if it was too low we'd try more attacks
    # than necessary
    pattern_quadrants: List[List[Tuple[int, int]]]

    max_boat_size: int
    targets_stack: List[Tuple[int, int]]

    def __init__(self) -> None:
        self.pattern_quadrants = [gen_diagonal_for_size(i, 10) for i in [2, 4]]
        self.max_boat_size = 5
        self.targets_stack = []

    def get_next_ai_turn(self, board: GameBoard, tried_list: GameBoard) -> Tuple[int, int]:
        quadrant_idx = 0 if self.max_boat_size < 4 else 1

        def get_next_spot() -> Tuple[int, int]:
            quadrant_idx = 0 if self.max_boat_size < 4 else 1
            if len(self.targets_stack) != 0:
                debug(self.targets_stack)
                return self.targets_stack.pop(-1)
            else:
                # Occasionally, we'll have broken the pattern because of target mode,
                # so we need to scale it down
                if len(self.pattern_quadrants[quadrant_idx]) == 0:
                    self.max_boat_size = 3
                    return get_next_spot()
                rnd = randint(0, len(self.pattern_quadrants[quadrant_idx]) - 1)
                return self.pattern_quadrants[quadrant_idx][rnd]

        next_spot = get_next_spot()

        while next_spot in tried_list:
            if next_spot in self.pattern_quadrants[quadrant_idx]:
                self.pattern_quadrants[quadrant_idx].remove(next_spot)
            next_spot = get_next_spot()

        if next_spot in self.pattern_quadrants[quadrant_idx]:
            self.pattern_quadrants[quadrant_idx].remove(next_spot)

        return next_spot

    def react_hit_success(self, board: GameBoard, tried_list: GameBoard, hit: Tuple[int, int]):
        """Notifies the AI it hit a ship
        """

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

    def react_hit_sunk(self, board: GameBoard, tried_list: GameBoard, hit: Tuple[int, int], ship_type: str):
        """Notifies the AI it sunk a ship
        """

        debug(f"AI actually managed to sink a {ship_type}-type ship !")

        if self.max_boat_size == get_size(ship_type):
            self.max_boat_size -= 1