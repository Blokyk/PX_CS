from enum import Enum
from typing import TypeVar, Any, Callable, List, OrderedDict
from ships import get_size

from ships import ShipPart
from utils import letter_to_idx

_T = TypeVar('_T')

class GameBoard(List[List[ShipPart]]):
    lines_count: int

    def __init__(self):
        self.lines_count = 0

    def append(self, __object: List[ShipPart]) -> None:
        self.lines_count += 1
        return super().append(__object)

    def get_columns_count(self):
        return len(self[0])

    def is_on_board(self, line: int, col: int) -> bool:
        #print(line, col, 'for', self.lines_count, self.get_columns_count())
        return line in range(0, self.lines_count) and col in range(0, self.get_columns_count())

    def __do_action_at(self, ship_type: ShipPart, angle: str, line_letter: str, col: int, defaultValue: _T, stopValue: _T, func: Callable[[Any, int, int], _T]) -> _T:
        line = letter_to_idx(line_letter)

        ship_size = get_size(ship_type)

        new_col = col
        new_line = line

        if angle == 'H':
            new_line = line + (ship_size - 1)
        elif angle == 'V':
            new_col = col + (ship_size)

        if not (self.is_on_board(line, col) and self.is_on_board(new_line, new_col)):
            return stopValue

        if (line != new_line):
            for i in range(min(line, new_line), max(line, new_line)+1):
                if func(self, i, col) == stopValue:
                    return func(self, i, col)
        else:
            for j in range(min(col, new_col), max(col, new_col)):
                if func(self, line, j) == stopValue:
                    return func(self, line, j)

        return defaultValue


    def put_at(self, ship_type: ShipPart, angle: str, line_letter: str, col: int) -> None:
        assert(self.ship_can_be_put_at(ship_type, angle, line_letter, col))

        def action(self, line: int, col: int) -> None:
            print("putting", ship_type, "at", "(" + str(line) + "," + str(col) + ")")
            self[line][col] = ShipPart(ship_type.value)

                                                # stopValue has to be different than None
                                                # because our function always returns None
        self.__do_action_at(ship_type, angle, line_letter, col, None, '', action)

    def ship_can_be_put_at(self, ship_type: ShipPart, angle: str, line_letter: str, col: int) -> bool:
        def action(self, line: int, col: int) -> bool:
            return self[line][col].value == ' '

        return self.__do_action_at(ship_type, angle, line_letter, col, True, False, action)