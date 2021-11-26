# Allow type-hints self-reference
from __future__ import annotations

from enum import Enum
from typing import Dict, Optional, Tuple, TypeVar, Any, Callable, List, OrderedDict

from ships import get_size

from utils import debug, letter_to_idx

ship_types = ['P', 'C', 'R', 'S', 'T']

class GameBoard(Dict[Tuple[int, int], str]):
    """An internal, more useful and more efficient representation of the gameboard.
    It's basically just a type alias for a dictionary of positions mapped to ship parts
    (`Dict[Tuple[int, int], str]`).
    To get the part at line 9 column 2, you'd write board[(8, 1)].
    """

    def __init__(self):
        pass

    def ship_type_is_sunk(self, ship_type: str, tried_list: GameBoard) -> bool:
        """Returns `True` if all parts of type `ship_type` on this board have been hit"""
        counter = 0

        for (coords, ship) in self.items():
            if ship == ship_type and (coords, ship) in tried_list.items():
                counter += 1

        debug(f"Ship type {ship_type} has been sunk {counter} times")

        return counter == get_size(ship_type)

    def are_all_ships_sunk(self, tried_list: GameBoard) -> bool:
        """Returns true f all the ships on this board have been hit and sunken"""
        for part in ship_types:
            if not self.ship_type_is_sunk(part, tried_list):
                return False

        return True

class SetupGameBoard(List[List[str]]):
    """The public, less efficient representation of a board of ship parts.
    It's mostly a shortcut for List[List[str]], with a bit of sugar on top of it.
    To get the element at line 3, column 6, you'd write board[2][5].
    """
    lines_count: int
    columns_count: int

    def __init__(self, lines: int, cols: int):
        self.lines_count = lines
        self.columns_count = cols

        for line in range(lines):
            self.append([' ' for _ in range(cols)])

    def is_on_board(self, line: int, col: int) -> bool:
        """Checks if the position is actually on this board"""
        return (0 <= line < self.lines_count) and (0 <= col < self.columns_count)

    __T = TypeVar("__T")

    def __do_action_at(self, ship_type: str, angle: str, line: int, col: int, defaultValue: __T, stopValue: __T, func: Callable[[Any, int, int], __T]) -> __T:
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
        """Inserts a ship using the config. The config has to be valid (see can_insert_ship_at)

        Raises :
            - ValueError if the ship couldn't be inserted
        """
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
        """Checks if you could insert a ship with given configuration (type, angle/orientation and position)

        Params :
            - ship_type (str) : one of ships.ship_types
            - angle (str) : The orientation of the ship. Either H or V (horizontal or vertical)
        """
        def action(self, line: int, col: int) -> bool:
            return self[line][col] == ' '

        return self.__do_action_at(ship_type, angle, line, col, True, False, action)