from enum import Enum
from typing import Dict, Optional, Tuple, TypeVar, Any, Callable, List, OrderedDict
from ships import get_size

from utils import letter_to_idx

_T = TypeVar('_T')

class GameBoard(Dict[Tuple[int, int], str]):
    def __init__(self):
        return

class SetupGameBoard(List[List[str]]):
    lines_count: int
    columns_count: int

    def __init__(self, lines: int, cols: int):
        self.lines_count = lines
        self.columns_count = cols

        for line in range(lines):
            self.append([])
            for col in range(cols):
                self[line].append(' ')

    def is_on_board(self, line: int, col: int) -> bool:
        return (0 <= line < self.lines_count) and (0 <= col < self.columns_count)

    def __do_action_at(self, ship_type: str, angle: str, line: int, col: int, defaultValue: _T, stopValue: _T, func: Callable[[Any, int, int], _T]) -> _T:
        ship_size = get_size(ship_type)
        angle = angle.upper()

        #debug(ship_size)

        new_col = col
        new_line = line

        if angle == 'V':
            new_line = line + (ship_size - 1)
        elif angle == 'H':
            new_col = col + (ship_size - 1)
        else:
            return stopValue

        if not (self.is_on_board(line, col) and self.is_on_board(new_line, new_col)):
            return stopValue

        for i in range(line, new_line+1):
            for j in range(col, new_col+1):
                if (res := func(self, i, j)) == stopValue:
                    return res

        return defaultValue


    def insert_ship_at(self, ship_type: str, angle: str, line: int, col: int) -> None:
        # we don't need an assertion because the check for the stopValue latter makes sure
        # that we'll stop (and raise an exception) if it's not possible (since __do_action_at
        # will stop unexpectedly)

        errorValue = ''

        def action(self, line: int, col: int) -> Optional[str]:
            #debug("putting", ship_type, "at", "(" + str(line) + "," + str(col) + ")")

            if self[line][col] != ' ':
                return errorValue

            self[line][col] = ship_type

                                                # stopValue has to be different than None
                                                #   - because our function always returns None
                                                #   - so that we can detect when there's an error
        if (self.__do_action_at(ship_type, angle, line, col, None, errorValue, action)) == errorValue:
            raise ValueError("Could not put" + str(ship_type) + "at position " + angle + "(" + str(line) + "," + str(col) + ")")

    def can_insert_ship_at(self, ship_type: str, angle: str, line: int, col: int) -> bool:
        def action(self, line: int, col: int) -> bool:
            return self[line][col] == ' '

        return self.__do_action_at(ship_type, angle, line, col, True, False, action)

    def get_hit_result(self, line: int, col: int) -> bool:
        return self[line][col] != ' '